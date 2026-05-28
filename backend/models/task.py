from sqlalchemy import Column, String, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from utils.db import Base
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    status = Column(String, nullable=False, default=TaskStatus.PENDING)
    progress = Column(Integer, default=0)
    target_duration = Column(Integer, nullable=False)
    subtitle_option = Column(String)
    result_path = Column(String)
    error_message = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    video = relationship("Video", back_populates="tasks")
