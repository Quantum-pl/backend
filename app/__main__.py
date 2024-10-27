import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.server:create_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )