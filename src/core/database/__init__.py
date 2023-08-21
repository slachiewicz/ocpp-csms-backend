from contextlib import asynccontextmanager
from uuid import uuid4

import arrow
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core import settings

engine = create_async_engine(settings.DATABASE_ASYNC_URL, echo=True)
asession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with asession() as session:
        yield session


@asynccontextmanager
async def get_contextual_session():
    async with asession() as session:
        yield session


Base = declarative_base()


class Model(Base):
    __abstract__ = True

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()), unique=True)
    created_at = Column(DateTime, default=lambda: arrow.utcnow().datetime.replace(tzinfo=None))
    updated_at = Column(DateTime, onupdate=lambda: arrow.utcnow().datetime.replace(tzinfo=None), nullable=True)
    is_active = Column(Boolean, default=True)
