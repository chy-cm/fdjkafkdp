from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from models.video import Video, VideoCreate, VideoInfo
from services.video_processor import VideoProcessor
from utils.db import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends

router = APIRouter()

@router.post("/", response_model=dict)
async def upload_video(
    file: UploadFile = File(...),
    target_duration: int = Form(...),
    subtitle_option: str = Form("new"),
    db: Session = Depends(get_db)
):
    allowed_extensions = {"mp4", "mov", "mkv", "avi"}
    file_extension = file.filename.split(".")[-1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    processor = VideoProcessor()
    result = await processor.process_upload(file, target_duration, subtitle_option, db)
    
    return result

@router.get("/{video_id}/info", response_model=VideoInfo)
def get_video_info(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return VideoInfo(
        id=video.id,
        filename=video.filename,
        duration=video.duration,
        fps=video.fps,
        width=video.width,
        height=video.height,
        format=video.format
    )

@router.get("/{video_id}/scenes")
def get_video_scenes(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    scenes = []
    for scene in video.scenes:
        scenes.append({
            "id": scene.id,
            "start_time": scene.start_time,
            "end_time": scene.end_time,
            "score": scene.score,
            "scene_type": scene.scene_type,
            "description": scene.description
        })
    
    return {"scenes": scenes}
