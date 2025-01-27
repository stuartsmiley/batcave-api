from pydantic import field_validator, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_mode: str
    auth0_audience: str
    auth0_domain: str
    client_origin_url: str

    @classmethod
    @field_validator("app_mode", "client_origin_url", "auth0_audience", "auth0_domain")
    def check_not_empty(cls, v):
        assert v != "", f"{v} is not defined"
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
