from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from utils.db import Base
from pydantic import BaseModel
from datetime import datetime

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    fps = Column(Float)
    width = Column(Integer)
    height = Column(Integer)
    format = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    scenes = relationship("Scene", back_populates="video")
    tasks = relationship("Task", back_populates="video")

class VideoCreate(BaseModel):
    filename: str
    filepath: str
    duration: float
    fps: float = None
    width: int = None
    height: int = None
    format: str = None

class VideoInfo(BaseModel):
    id: int
    filename: str
    duration: float
    fps: float = None
    width: int = None
    height: int = None
    format: str = None
