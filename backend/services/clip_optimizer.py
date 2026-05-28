from models.video import Video
from models.scene import Scene

class ClipOptimizer:
    def __init__(self):
        pass
    
    def optimize(self, video_id: int, target_duration: int, db):
        video = db.query(Video).filter(Video.id == video_id).first()
        
        if not video:
            raise ValueError("Video not found")
        
        scenes = db.query(Scene).filter(Scene.video_id == video_id).order_by(Scene.start_time).all()
        
        mandatory_scenes = [s for s in scenes if s.score >= 0.8]
        optional_scenes = [s for s in scenes if s.score < 0.8]
        
        mandatory_duration = sum(s.end_time - s.start_time for s in mandatory_scenes)
        
        if mandatory_duration > target_duration:
            raise ValueError("Mandatory scenes exceed target duration")
        
        remaining_duration = target_duration - mandatory_duration
        
        optional_scenes.sort(key=lambda s: s.score, reverse=True)
        
        selected_scenes = mandatory_scenes.copy()
        current_duration = mandatory_duration
        
        for scene in optional_scenes:
            scene_duration = scene.end_time - scene.start_time
            if current_duration + scene_duration <= target_duration:
                selected_scenes.append(scene)
                current_duration += scene_duration
        
        selected_scenes.sort(key=lambda s: s.start_time)
        
        return selected_scenes
    
    def apply_transitions(self, scenes):
        transitions = []
        
        for i in range(len(scenes) - 1):
            current_end = scenes[i].end_time
            next_start = scenes[i + 1].start_time
            
            if next_start - current_end > 0.5:
                transitions.append({
                    "type": "fade",
                    "start_time": current_end - 0.25,
                    "end_time": next_start + 0.25
                })
            else:
                transitions.append({
                    "type": "cut",
                    "time": current_end
                })
        
        return transitions
