from    sqlalchemy.ext.asyncio  import  create_async_engine, async_sessionmaker, AsyncSession
from    sqlalchemy.engine       import  URL
from    sqlalchemy.orm          import  DeclarativeBase
from    pydantic_settings       import  BaseSettings
from    contextlib              import  asynccontextmanager
from    typing                  import  Annotated
from    fastapi                 import  Depends, FastAPI


# store env variables
class   Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

settings = Settings()
debug = True

# create db url
url = URL.create(
    drivername = "postgresql+asyncpg",
    username = settings.POSTGRES_USER,
    password = settings.POSTGRES_PASSWORD,
    host = "localhost" if debug else "postgres",
    port = 5432,
    database = settings.POSTGRES_DB
)

# create the engine that connects to the db via the url
engine = create_async_engine(url)
print(f"\n\033[1;35mDATABASE_URL: \033[0;35m{url}\033[0m\n")

# declare sqlalchemy base class
class   Base(DeclarativeBase):
    pass

@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# session factory
async_session_factory = async_sessionmaker(bind=engine)

# session yielder dependency
async def get_async_session():
    async with async_session_factory() as async_session:
        yield async_session

# store dependency in an annotated dependency
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


