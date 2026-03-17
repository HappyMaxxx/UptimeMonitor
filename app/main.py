from fastapi import FastAPI

from app.routers import targets, auth, users 

app = FastAPI()

app.include_router(targets.router, tags=["Targets"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(users.router, tags=["Users"])

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}