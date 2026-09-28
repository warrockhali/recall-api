from fastapi import FastAPI

app = FastAPI(title="Recall API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
