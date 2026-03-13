from fastapi import FastAPI

from app.routers.targets import router

app = FastAPI()

app.include_router(router, tags=["Targets"])

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}