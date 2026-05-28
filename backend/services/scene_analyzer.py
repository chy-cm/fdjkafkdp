import os
import cv2
import numpy as np
from models.video import Video
from models.scene import Scene
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

class SceneAnalyzer:
    SCENE_WEIGHTS = {
        "key_event": 1.0,
        "climax": 1.0,
        "ending": 1.0,
        "intro": 0.9,
        "character_intro": 0.8,
        "dialogue": 0.6,
        "action": 0.5,
        "transition": 0.3,
        "atmosphere": 0.1
    }
    
    def __init__(self):
        pass
    
    def analyze_video(self, video_id: int, db):
        video = db.query(Video).filter(Video.id == video_id).first()
        
        if not video:
            raise ValueError("Video not found")
        
        scenes = self.detect_scenes(video.filepath)
        
        total_duration = video.duration
        
        for i, (start_time, end_time) in enumerate(scenes):
            duration = end_time - start_time
            score = self.calculate_score(start_time, end_time, total_duration, i, len(scenes))
            scene_type = self.classify_scene(start_time, end_time, total_duration, i, len(scenes))
            description = self.generate_scene_description(start_time, end_time, duration)
            
            scene = Scene(
                video_id=video.id,
                start_time=start_time,
                end_time=end_time,
                score=score,
                scene_type=scene_type,
                description=description
            )
            db.add(scene)
        
        db.commit()
    
    def detect_scenes(self, filepath: str):
        video_manager = VideoManager([filepath])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=30.0))
        
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scenes = scene_manager.get_scene_list()
        
        scene_times = []
        for scene in scenes:
            start_time = scene[0].get_seconds()
            end_time = scene[1].get_seconds()
            scene_times.append((start_time, end_time))
        
        video_manager.release()
        return scene_times
    
    def calculate_score(self, start_time: float, end_time: float, total_duration: float, scene_index: int, total_scenes: int):
        duration_ratio = (end_time - start_time) / total_duration
        
        if duration_ratio < 0.005:
            return 0.1
        elif duration_ratio > 0.2:
            return 0.9
        
        mid_time = (start_time + end_time) / 2
        position_ratio = mid_time / total_duration
        
        position_score = 0.5
        if position_ratio < 0.05:
            position_score = 0.9
        elif position_ratio > 0.95:
            position_score = 0.9
        elif 0.3 < position_ratio < 0.7:
            position_score = 0.8
        
        duration_score = min(0.9, duration_ratio * 5)
        
        total_score = (position_score * 0.6 + duration_score * 0.4)
        
        return round(total_score, 2)
    
    def classify_scene(self, start_time: float, end_time: float, total_duration: float, scene_index: int, total_scenes: int):
        position_start = start_time / total_duration
        position_end = end_time / total_duration
        position_mid = (position_start + position_end) / 2
        
        if position_start < 0.03:
            return "intro"
        elif position_end > 0.97:
            return "ending"
        elif 0.35 < position_mid < 0.65:
            if total_scenes > 5:
                climax_index = int(total_scenes * 0.6)
                if abs(scene_index - climax_index) < 2:
                    return "climax"
            else:
                return "climax"
        elif position_mid < 0.15:
            return "character_intro"
        
        return "transition"
    
    def generate_scene_description(self, start_time: float, end_time: float, duration: float) -> str:
        scene_type = self.classify_scene(start_time, end_time, 1.0, 0, 1)
        
        descriptions = {
            "intro": f"开场场景，时长 {duration:.1f} 秒",
            "ending": f"结尾场景，时长 {duration:.1f} 秒",
            "climax": f"高潮场景，时长 {duration:.1f} 秒",
            "character_intro": f"人物介绍场景，时长 {duration:.1f} 秒",
            "transition": f"过渡场景，时长 {duration:.1f} 秒"
        }
        
        return descriptions.get(scene_type, f"场景时长 {duration:.1f} 秒")
    
    def extract_keyframe(self, video_path: str, timestamp: float) -> str:
        try:
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                keyframe_path = os.path.join("/workspace/outputs", f"keyframe_{uuid.uuid4()}.jpg")
                cv2.imwrite(keyframe_path, frame)
                return keyframe_path
            
            return None
        except Exception as e:
            print(f"Error extracting keyframe: {e}")
            return None
