from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "Cookbook Server"
    debug: bool = False
    db_host: str
    db_port: int = 5432
    db_user: str
    db_password: str
    db_name: str
    api_secret_key: str
    api_algorithm: str = "HS256"
    api_access_token_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:5173"]  # override via CORS_ORIGINS env var in prod

    @property
    def db_url(self):
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


config = Config()
