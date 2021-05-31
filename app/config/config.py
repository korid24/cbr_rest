from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api_v1'
    PROJECT_NAME: str = 'CBR currency conversion REST'

    class Config:
        case_sensitive = True


settings = Settings()
