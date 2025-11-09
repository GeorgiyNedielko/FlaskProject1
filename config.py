from pathlib import Path
from typing import Any
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Community Pulse"
    debug: bool = True
    secret_key: SecretStr

    mysql_host: str
    mysql_port: int = 3306
    mysql_user: str
    mysql_password: SecretStr
    mysql_database: str
    mysql_pool_size: int = 5
    mysql_pool_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",
        case_sensitive=False,
        extra="allow"
    )

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password.get_secret_value()}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

    def get_flask_config(self) -> dict[str, Any]:
        return {
            "SECRET_KEY": self.secret_key.get_secret_value(),
            "DEBUG": self.debug,
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_POOL_SIZE": self.mysql_pool_size,
            "SQLALCHEMY_POOL_TIMEOUT": self.mysql_pool_timeout
        }

settings = Settings()

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'


class DevelopmentConfig(Config):
    DEBUG =True

class TestingConfig(Config):
    TESTING = True