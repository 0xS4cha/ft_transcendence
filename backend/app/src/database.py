from    sqlalchemy.ext.asyncio  import  create_async_engine, async_sessionmaker
from    sqlalchemy.engine   import  URL
from    pydantic_settings   import  BaseSettings

class   Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

settings = Settings()

url = URL.create(
    drivername = "postgresql+asyncpg",
    username = settings.POSTGRES_USER,
    password = settings.POSTGRES_PASSWORD,
    host = "postgres",
    port = 5432,
    database = settings.POSTGRES_DB
)

engine = create_async_engine(url)
Session = async_sessionmaker(bind=engine)
