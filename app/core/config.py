from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    # API配置
    API_BASE_URL: str
    API_USERNAME: str
    API_PASSWORD: str

    # 数据库配置
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # 应用配置
    DEBUG: bool = False
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
