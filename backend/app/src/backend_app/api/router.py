from    fastapi                                 import  APIRouter
from    backend_app.api.endpoints.authenticate  import  router  as  authenticate_router

api_router = APIRouter(prefix="/api")

api_router.include_router(
    authenticate_router,
    tags=["Authentication"],
    prefix="/auth"
)

