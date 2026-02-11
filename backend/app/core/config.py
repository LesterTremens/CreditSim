from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "CreditSim API"
    app_env: str = "local"
    cors_origins: str = "*"
    database_url: str
    secret_key: str
    refresh_secret_key: str | None = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str | None = None
    allowed_email_domains: str | None = None
    
    model_config = ConfigDict(
        env_file = ".env"
    )

settings = Settings()
