from typing import Union

from sqlalchemy import insert as insert_stmt
from sqlalchemy import select as select_stmt
from sqlalchemy import delete as delete_stmt
from sqlalchemy import update as update_stmt
from sqlalchemy.orm import Session

from database import Base


def create(
    db: Session,
    entity: Base,
    data: dict,
) -> int:
    stmt = insert_stmt(entity).values(**data).returning(entity.id)
    result = db.execute(stmt)
    db.commit()
    return result.scalars().first()


def read(
    db: Session,
    entity: Base,
    filter_: list,
) -> Base:
    stmt = select_stmt(entity).filter(*filter_)
    result = db.execute(stmt)
    return result.scalars().first()


def update(
    db: Session,
    entity: Base,
    entry_id: Union[int, str],
    data: dict,
) -> None:
    stmt = update_stmt(entity).where(entity.id == entry_id).values(**data)
    db.execute(stmt)
    db.commit()


def delete(
    db: Session,
    entity: Base,
    filter_: list,
) -> None:
    stmt = delete_stmt(entity).where(*filter_)
    db.execute(stmt)
    db.commit()
