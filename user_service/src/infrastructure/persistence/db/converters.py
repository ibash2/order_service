from domain.user import entities
from infrastructure.persistence.db import models


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id,
        login=user.login,
        password=user.password,
    )


def convert_db_model_to_user_entity(user: models.User) -> entities.User:
    return entities.User(
        id=user.id,
        login=user.login,
        password=user.password,
    )
