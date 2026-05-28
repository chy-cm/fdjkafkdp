import os
import random
import uuid

class BackgroundMusic:
    DEFAULT_MUSIC_DIR = "/workspace/assets/music"
    
    MUSIC_STYLES = {
        "epic": ["epic_adventure.mp3", "heroic_journey.mp3", "triumphant.mp3"],
        "calm": ["peaceful_morning.mp3", "gentle_flow.mp3", "serene_moment.mp3"],
        "dramatic": ["tension_builds.mp3", "dark_mystery.mp3", "suspense.mp3"],
        "emotional": ["heart_touching.mp3", "melancholy.mp3", "nostalgic.mp3"],
        "neutral": ["ambient_scape.mp3", "soft_background.mp3", "minimal_beat.mp3"]
    }
    
    def __init__(self, music_dir: str = None):
        self.music_dir = music_dir or self.DEFAULT_MUSIC_DIR
    
    def get_available_music(self) -> list:
        available = []
        
        if os.path.exists(self.music_dir):
            for filename in os.listdir(self.music_dir):
                if filename.endswith(('.mp3', '.wav', '.ogg')):
                    available.append(os.path.join(self.music_dir, filename))
        
        return available
    
    def select_music_for_video(self, video_duration: float, style: str = "neutral") -> str:
        available = self.get_available_music()
        
        if available:
            selected = random.choice(available)
            return self.adjust_music_length(selected, video_duration)
        
        return self.generate_placeholder_music(video_duration)
    
    def adjust_music_length(self, music_path: str, target_duration: float) -> str:
        try:
            from pydub import AudioSegment
            
            audio = AudioSegment.from_file(music_path)
            audio_duration = len(audio) / 1000.0
            
            if audio_duration < target_duration:
                repeats_needed = int(target_duration / audio_duration) + 1
                extended = audio * repeats_needed
                adjusted = extended[:int(target_duration * 1000)]
            else:
                start = random.randint(0, int((audio_duration - target_duration) * 1000))
                adjusted = audio[start:start + int(target_duration * 1000)]
            
            output_path = os.path.join("/workspace/outputs", f"bg_music_{uuid.uuid4()}.mp3")
            adjusted.export(output_path, format="mp3")
            
            return output_path
        except Exception as e:
            print(f"Error adjusting music: {e}")
            return music_path
    
    def generate_placeholder_music(self, duration: float) -> str:
        try:
            from pydub import AudioSegment
            import numpy as np
            
            sample_rate = 44100
            num_samples = int(duration * sample_rate)
            
            t = np.linspace(0, duration, num_samples)
            
            freq = random.choice([220, 330, 440])
            audio_data = 0.1 * np.sin(2 * np.pi * freq * t)
            
            audio_data = audio_data.astype(np.float32)
            
            from pydub import AudioSegment
            import io
            
            buffer = io.BytesIO()
            import wave
            with wave.open(buffer, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes((audio_data * 32767).astype(np.int16).tobytes())
            
            buffer.seek(0)
            audio = AudioSegment.from_wav(buffer)
            
            output_path = os.path.join("/workspace/outputs", f"bg_music_{uuid.uuid4()}.mp3")
            audio.export(output_path, format="mp3")
            
            return output_path
        except Exception as e:
            print(f"Error generating placeholder music: {e}")
            return None
    
    def mix_with_narration(self, bg_music_path: str, narration_path: str, output_path: str, music_volume: float = 0.2) -> str:
        try:
            from pydub import AudioSegment
            
            if not bg_music_path or not os.path.exists(bg_music_path):
                return narration_path
            
            bg_music = AudioSegment.from_file(bg_music_path)
            narration = AudioSegment.from_file(narration_path)
            
            bg_music = bg_music[:len(narration)]
            bg_music = bg_music - 10 + (music_volume * 10)
            
            mixed = bg_music.overlay(narration)
            
            mixed.export(output_path, format="mp3")
            
            return output_path
        except Exception as e:
            print(f"Error mixing audio: {e}")
            return narration_path
