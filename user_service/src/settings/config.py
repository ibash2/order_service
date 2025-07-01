from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/test")
    MQ_URL: str = Field(default="amqp://guest:guest@localhost:5672")

    user_created_topic: str = Field(alias='USER_CREATED_TOPIC', default="user_created")



def load_config() -> Config:
    return Config()  # type: ignore