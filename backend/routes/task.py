from fastapi import APIRouter, HTTPException
from models.task import Task, TaskStatus
from utils.db import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends
from celery_app import celery_app

router = APIRouter()

@router.get("/")
def get_tasks(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    
    tasks = []
    for task in query.all():
        tasks.append({
            "id": task.id,
            "video_id": task.video_id,
            "status": task.status,
            "progress": task.progress,
            "target_duration": task.target_duration,
            "subtitle_option": task.subtitle_option,
            "result_path": task.result_path,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        })
    
    return {"tasks": tasks}

@router.get("/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "video_id": task.video_id,
        "status": task.status,
        "progress": task.progress,
        "target_duration": task.target_duration,
        "subtitle_option": task.subtitle_option,
        "result_path": task.result_path,
        "error_message": task.error_message,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }

@router.delete("/{task_id}")
def cancel_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
        raise HTTPException(status_code=400, detail="Cannot cancel completed or failed task")
    
    celery_app.control.revoke(task_id, terminate=True)
    task.status = TaskStatus.FAILED
    task.error_message = "Task cancelled by user"
    db.commit()
    
    return {"success": True, "message": "Task cancelled"}

@router.post("/batch")
def create_batch_tasks(videos: dict, db: Session = Depends(get_db)):
    task_ids = []
    
    for video_data in videos.get("videos", []):
        pass
    
    return {"task_ids": task_ids}
