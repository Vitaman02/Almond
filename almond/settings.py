from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    almond_token: str
    host_url: str
    vps_name: str = "Main"
    cpu_threshold: int = 80
    mem_threshold: int = 80


@lru_cache
def get_settings() -> Settings:
    return Settings()
