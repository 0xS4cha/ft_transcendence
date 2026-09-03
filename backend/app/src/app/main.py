from    fastapi             import  FastAPI
from    app.database        import  lifespan
from    app.authenticate    import  router  as  authenticate_router

app = FastAPI(lifespan=lifespan)

app.include_router(authenticate_router)

@app.head("/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def home():
    return {"message": "First FastAPI app"}
