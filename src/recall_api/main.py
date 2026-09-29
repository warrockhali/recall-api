from fastapi import FastAPI

from recall_api.auth.router import router as auth_router

app = FastAPI(title="Recall API")
app.include_router(auth_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
