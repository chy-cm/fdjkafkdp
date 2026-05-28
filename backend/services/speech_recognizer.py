import os
import uuid
from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

class SpeechRecognizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("API_KEY"))
    
    def extract_audio(self, video_path: str) -> str:
        audio_path = os.path.join("/workspace/outputs", f"audio_{uuid.uuid4()}.wav")
        
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(video_path)
            audio = audio.set_channels(1)
            audio.export(audio_path, format="wav")
            return audio_path
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return None
    
    def transcribe(self, audio_path: str) -> list:
        if not audio_path or not os.path.exists(audio_path):
            return []
        
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
            
            segments = []
            for segment in transcript.segments:
                segments.append({
                    "id": segment.get("id", 0),
                    "start": segment.get("start", 0),
                    "end": segment.get("end", 0),
                    "text": segment.get("text", "").strip()
                })
            
            return segments
        except Exception as e:
            print(f"Transcription error: {e}")
            return []
    
    def process_video(self, video_path: str) -> dict:
        audio_path = self.extract_audio(video_path)
        
        if not audio_path:
            return {"segments": [], "full_text": ""}
        
        try:
            segments = self.transcribe(audio_path)
            full_text = " ".join([seg["text"] for seg in segments])
            
            os.remove(audio_path)
            
            return {
                "segments": segments,
                "full_text": full_text
            }
        except Exception as e:
            print(f"Error processing video: {e}")
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return {"segments": [], "full_text": ""}
