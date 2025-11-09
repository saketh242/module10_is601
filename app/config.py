from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/fastapi_db"
    SECRET_KEY: str = "saketh-secret-key"
    
    class Config:
        env_file = ".env"

settings = Settings()