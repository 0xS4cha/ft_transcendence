from    fastapi     import  FastAPI
from    .database    import  lifespan

app = FastAPI(lifespan=lifespan)

@app.head("/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def home():
    return {"message": "First FastAPI app"}