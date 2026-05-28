import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class NarrationEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("API_KEY"))
        self.output_dir = os.getenv("OUTPUT_DIR", "/workspace/outputs")
    
    def generate_script(self, scenes, db):
        if not scenes:
            return "This is a summary of the video content."
        
        scene_descriptions = []
        for scene in scenes:
            scene_descriptions.append({
                "time": f"{scene.start_time:.2f}-{scene.end_time:.2f}",
                "type": scene.scene_type,
                "score": scene.score,
                "description": scene.description or "Scene content"
            })
        
        prompt = f"""
        You are a professional video narrator. Based on the following scene analysis, 
        write a coherent, engaging narration script for a video summary:
        
        Scenes: {scene_descriptions}
        
        Requirements:
        - The script should flow naturally from one scene to the next
        - Highlight the most important events (high-score scenes)
        - Keep the language conversational and engaging
        - Make sure the story makes sense without watching the video
        - Do not mention scene times or technical details
        
        Please provide only the narration text.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional video narrator."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()
    
    def synthesize_speech(self, script: str):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=script
        )
        
        audio_path = os.path.join(self.output_dir, f"narration_{uuid.uuid4()}.mp3")
        response.stream_to_file(audio_path)
        
        return audio_path
    
    def calculate_speech_duration(self, script: str):
        words_per_minute = 150
        word_count = len(script.split())
        return (word_count / words_per_minute) * 60
