from fastapi import Depends

from presentation.api.controllers.auth.schemas import InitDataModel
from presentation.api.controllers.auth.exceptions import InitDataNotValid
from presentation.api.controllers.auth.security import validate_init_data


def valid_init_data(user: InitDataModel | None = Depends(validate_init_data)):
    if user is None:
        raise InitDataNotValid()

    return user
