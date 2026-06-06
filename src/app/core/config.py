from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    API_HOST: str = '127.0.0.1'
    API_PORT: int = 8000

    DOCS_URL: str = '/api/docs'
    OPENAPI_URL: str = '/api/docs.json'
    REDOC_URL: str = '/api/redoc'

    DEBUG: bool = True


config = Config()
