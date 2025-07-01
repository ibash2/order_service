from typing import Iterable
from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert

from domain.common.constants import Empty
from infrastructure.persistence.db.repositories.base import SQLAlchemyRepo

@dataclass
class SqlAlchemyPairRepository(SQLAlchemyRepo):
   pass