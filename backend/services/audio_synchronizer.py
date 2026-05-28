import os
import uuid
import ffmpeg
from dotenv import load_dotenv

load_dotenv()

class AudioSynchronizer:
    def __init__(self):
        self.output_dir = os.getenv("OUTPUT_DIR", "/workspace/outputs")
    
    def sync_audio_video(self, video_path: str, scenes, audio_path: str, subtitle_option: str):
        output_path = os.path.join(self.output_dir, f"output_{uuid.uuid4()}.mp4")
        
        scene_clips = []
        for i, scene in enumerate(scenes):
            clip = ffmpeg.input(video_path).trim(
                start=scene.start_time,
                end=scene.end_time
            )
            
            if i > 0:
                clip = clip.fadein(duration=0.2)
            
            if i < len(scenes) - 1:
                clip = clip.fadeout(duration=0.2)
            
            scene_clips.append(clip)
        
        if scene_clips:
            concatenated = ffmpeg.concat(*scene_clips, v=1, a=0)
        else:
            concatenated = ffmpeg.input(video_path).trim(start=0, end=1)
        
        audio_input = ffmpeg.input(audio_path)
        
        output = ffmpeg.output(
            concatenated,
            audio_input,
            output_path,
            vcodec="libx264",
            acodec="aac",
            strict="experimental"
        )
        
        ffmpeg.run(output, overwrite_output=True)
        
        return output_path
    
    def add_subtitles(self, video_path: str, subtitles: str, output_path: str = None):
        if not output_path:
            output_path = os.path.join(self.output_dir, f"subtitled_{uuid.uuid4()}.mp4")
        
        subtitles_path = os.path.join(self.output_dir, f"subtitles_{uuid.uuid4()}.srt")
        
        with open(subtitles_path, "w") as f:
            f.write(subtitles)
        
        ffmpeg.input(video_path).output(
            output_path,
            vf=f"subtitles={subtitles_path}",
            c="copy"
        ).run(overwrite_output=True)
        
        os.remove(subtitles_path)
        
        return output_path
    
    def add_background_music(self, video_path: str, music_path: str, output_path: str = None):
        if not output_path:
            output_path = os.path.join(self.output_dir, f"with_music_{uuid.uuid4()}.mp4")
        
        video = ffmpeg.input(video_path)
        music = ffmpeg.input(music_path).audio.volume(0.1)
        
        ffmpeg.output(
            video,
            music,
            output_path,
            vcodec="copy",
            acodec="aac"
        ).run(overwrite_output=True)
        
        return output_path
