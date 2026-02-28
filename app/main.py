from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.tasks import router as tasks_router

app = FastAPI(title="Task Secure API", version="1.0.0")

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["Tasks"])
@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"name": "Task Secure API", "docs": "/docs", "health": "/health"}