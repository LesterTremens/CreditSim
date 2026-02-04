from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "CreditSim API"
    app_env: str = "local"
    cors_origins: str = "*"
    database_url: str
    
    model_config = ConfigDict(
        env_file = ".env"
    )

settings = Settings()