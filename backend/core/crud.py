from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import TypeVar, Optional
from core.models import Base


ModelType = TypeVar("ModelType", bound=Base)


async def get_list(
    session: AsyncSession,
    model: ModelType,
) -> list[ModelType]:
    stmt = select(model).options(selectinload("*")).order_by(model.id)
    models: Result = await session.execute(stmt)
    return list(models.scalars().all())


async def get_by_id(
    session: AsyncSession, model: ModelType, id: int
) -> Optional[ModelType]:
    return await session.get(entity=model, ident=id)


async def create(session: AsyncSession, model: ModelType, data: BaseModel) -> ModelType:
    model: ModelType = model(**data.model_dump())
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model


async def update(
    session: AsyncSession,
    model: ModelType,
    id: int,
    data: BaseModel,
) -> Optional[ModelType]:
    essence: ModelType = await session.get(model, ident=id)
    if essence is None:
        return None
    for name, value in data.model_dump(exclude_unset=True).items():
        setattr(essence, name, value)
    await session.commit()
    return essence


async def delete(session: AsyncSession, model: ModelType, id: int) -> bool:
    model: Optional[ModelType] = await session.get(entity=model, ident=id)
    if model is None:
        return False
    await session.delete(model)
    await session.commit()
    return True
