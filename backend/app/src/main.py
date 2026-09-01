from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from uv + Docker"}

@app.head("/")
def index():
    return {"message": "Hello from uv + Docker, its healthy"}

@app.get("/health")
def health():
    return {"status": "ok"}