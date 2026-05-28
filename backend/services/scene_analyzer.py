import os
from models.video import Video
from models.scene import Scene
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

class SceneAnalyzer:
    def __init__(self):
        pass
    
    def analyze_video(self, video_id: int, db):
        video = db.query(Video).filter(Video.id == video_id).first()
        
        if not video:
            raise ValueError("Video not found")
        
        scenes = self.detect_scenes(video.filepath)
        
        for start_time, end_time in scenes:
            duration = end_time - start_time
            score = self.calculate_score(start_time, end_time, video.duration)
            scene_type = self.classify_scene(start_time, video.duration)
            
            scene = Scene(
                video_id=video.id,
                start_time=start_time,
                end_time=end_time,
                score=score,
                scene_type=scene_type
            )
            db.add(scene)
        
        db.commit()
    
    def detect_scenes(self, filepath: str):
        video_manager = VideoManager([filepath])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector())
        
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
    
    def calculate_score(self, start_time: float, end_time: float, total_duration: float):
        duration_ratio = (end_time - start_time) / total_duration
        
        if duration_ratio < 0.01:
            return 0.1
        
        mid_time = (start_time + end_time) / 2
        position_in_video = mid_time / total_duration
        
        if position_in_video < 0.1 or position_in_video > 0.9:
            return 0.8
        elif 0.4 < position_in_video < 0.6:
            return 0.7
        
        return 0.5
    
    def classify_scene(self, start_time: float, total_duration: float):
        position = start_time / total_duration
        
        if position < 0.05:
            return "intro"
        elif position > 0.9:
            return "ending"
        elif 0.4 < position < 0.6:
            return "climax"
        else:
            return "transition"
