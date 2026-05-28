from fastapi import APIRouter, HTTPException, Response
from models.task import Task, TaskStatus
from utils.db import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends
import os

router = APIRouter()

@router.post("/{task_id}")
def export_video(
    task_id: str,
    format: str = "mp4",
    resolution: str = "1080p",
    bitrate: str = "5000k",
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Task not completed")
    
    if not task.result_path or not os.path.exists(task.result_path):
        raise HTTPException(status_code=404, detail="Result file not found")
    
    return {"download_url": f"/api/export/{task_id}/download"}

@router.get("/{task_id}/download")
def download_video(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task.result_path or not os.path.exists(task.result_path):
        raise HTTPException(status_code=404, detail="Result file not found")
    
    with open(task.result_path, "rb") as f:
        content = f.read()
    
    filename = os.path.basename(task.result_path)
    return Response(content, media_type="video/mp4", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })

@router.get("/{task_id}/project")
def download_project(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    project_data = {
        "task_id": task.id,
        "video_id": task.video_id,
        "target_duration": task.target_duration,
        "subtitle_option": task.subtitle_option,
        "result_path": task.result_path,
        "created_at": task.created_at.isoformat()
    }
    
    import json
    content = json.dumps(project_data, indent=2)
    
    return Response(content, media_type="application/json", headers={
        "Content-Disposition": f"attachment; filename=project_{task_id}.json"
    })
