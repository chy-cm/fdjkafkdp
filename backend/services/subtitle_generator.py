import os
import uuid

class SubtitleGenerator:
    def __init__(self):
        self.output_dir = "/workspace/outputs"
    
    def generate_srt(self, narration_script: str, duration: float) -> str:
        words = narration_script.split()
        total_words = len(words)
        
        if total_words == 0:
            return ""
        
        words_per_second = total_words / duration if duration > 0 else 1
        
        srt_content = []
        current_word_index = 0
        current_time = 0.0
        
        segment_duration = 3.0
        
        while current_word_index < total_words:
            end_time = min(current_time + segment_duration, duration)
            
            segment_words = []
            segment_end_time = current_time
            
            while current_word_index < total_words and segment_end_time < end_time:
                word = words[current_word_index]
                segment_words.append(word)
                current_word_index += 1
                segment_end_time += 1.0 / words_per_second
            
            if segment_words:
                text = " ".join(segment_words)
                start_timestamp = self.format_timestamp(current_time)
                end_timestamp = self.format_timestamp(segment_end_time)
                
                subtitle_index = len(srt_content) + 1
                srt_content.append(f"{subtitle_index}\n{start_timestamp} --> {end_timestamp}\n{text}\n")
            
            current_time = segment_end_time
        
        return "\n".join(srt_content)
    
    def format_timestamp(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def save_subtitle(self, srt_content: str) -> str:
        if not srt_content:
            return None
        
        subtitle_path = os.path.join(self.output_dir, f"subtitle_{uuid.uuid4()}.srt")
        
        with open(subtitle_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        return subtitle_path
    
    def sync_with_audio(self, subtitle_path: str, audio_path: str, output_path: str) -> str:
        try:
            import subprocess
            
            cmd = [
                "ffmpeg",
                "-i", subtitle_path,
                "-i", audio_path,
                "-c:s", "mov_text",
                "-c:v", "copy",
                "-c:a", "copy",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return output_path
            else:
                return None
        except Exception as e:
            print(f"Error syncing subtitles: {e}")
            return None
