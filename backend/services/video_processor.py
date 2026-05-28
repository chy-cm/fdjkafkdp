import os
import uuid
from fastapi import UploadFile
from models.video import Video, VideoCreate
from models.task import Task, TaskStatus
from utils.db import get_db
from celery_app import celery_app
from dotenv import load_dotenv

load_dotenv()

class VideoProcessor:
    def __init__(self):
        self.upload_dir = os.getenv("UPLOAD_DIR", "/workspace/uploads")
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE", 5242880000))
    
    async def process_upload(self, file: UploadFile, target_duration: int, subtitle_option: str, db):
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > self.max_file_size:
            raise ValueError("File size exceeds maximum limit")
        
        file_extension = file.filename.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(self.upload_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(content)
        
        video_info = self.get_video_info(filepath)
        
        video = Video(
            filename=file.filename,
            filepath=filepath,
            duration=video_info["duration"],
            fps=video_info.get("fps"),
            width=video_info.get("width"),
            height=video_info.get("height"),
            format=file_extension
        )
        
        db.add(video)
        db.commit()
        db.refresh(video)
        
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            video_id=video.id,
            status=TaskStatus.PENDING,
            target_duration=target_duration,
            subtitle_option=subtitle_option
        )
        
        db.add(task)
        db.commit()
        
        self.start_processing.delay(task_id)
        
        return {
            "task_id": task_id,
            "video_id": video.id,
            "video_info": video_info,
            "message": "Upload successful. Processing started."
        }
    
    def get_video_info(self, filepath: str):
        import ffmpeg
        
        try:
            probe = ffmpeg.probe(filepath)
            video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
            
            info = {
                "duration": float(probe["format"]["duration"]),
            }
            
            if video_stream:
                info["fps"] = eval(video_stream["r_frame_rate"])
                info["width"] = video_stream["width"]
                info["height"] = video_stream["height"]
            
            return info
        except Exception as e:
            return {"duration": 0.0}
    
    @celery_app.task(bind=True, name="video_processing")
    def start_processing(self, task_id: str):
        from services.scene_analyzer import SceneAnalyzer
        from services.clip_optimizer import ClipOptimizer
        from services.narration_engine import NarrationEngine
        from services.audio_synchronizer import AudioSynchronizer
        
        db = next(get_db())
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return
        
        task.status = TaskStatus.PROCESSING
        db.commit()
        
        try:
            video = task.video
            
            scene_analyzer = SceneAnalyzer()
            scene_analyzer.analyze_video(video.id, db)
            task.progress = 20
            db.commit()
            
            clip_optimizer = ClipOptimizer()
            selected_scenes = clip_optimizer.optimize(video.id, task.target_duration, db)
            task.progress = 40
            db.commit()
            
            narration_engine = NarrationEngine()
            narration_script = narration_engine.generate_script(selected_scenes, db)
            audio_path = narration_engine.synthesize_speech(narration_script)
            task.progress = 60
            db.commit()
            
            audio_synchronizer = AudioSynchronizer()
            output_path = audio_synchronizer.sync_audio_video(
                video.filepath, 
                selected_scenes, 
                audio_path,
                task.subtitle_option
            )
            task.progress = 80
            db.commit()
            
            task.result_path = output_path
            task.status = TaskStatus.COMPLETED
            task.progress = 100
            db.commit()
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            db.commit()
