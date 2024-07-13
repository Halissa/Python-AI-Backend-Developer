from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    DATABASE_URL: str = "mongodb://localhost:27017/store?uuidRepresentation=standard"


settings = Settings()
