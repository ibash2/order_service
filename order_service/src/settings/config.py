from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/test"
    )
    MQ_URL: str = Field(default="amqp://guest:guest@localhost:5672")

    order_created_topic: str = Field(
        alias="ORDER_CREATED_TOPIC", default="order_created"
    )
    order_updated_topic: str = Field(
        alias="ORDER_UPDATED_TOPIC", default="order_updated"
    )


def load_config() -> Config:
    return Config()  # type: ignore
