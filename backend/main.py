from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import video, task, export

app = FastAPI(title="CineSynopsis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/api/videos", tags=["videos"])
app.include_router(task.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(export.router, prefix="/api/export", tags=["export"])

@app.get("/")
def read_root():
    return {"message": "CineSynopsis API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
