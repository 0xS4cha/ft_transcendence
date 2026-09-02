from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "First FastAPI app"}

@app.head("/")
def index():
    return {"message": "Healthy"}