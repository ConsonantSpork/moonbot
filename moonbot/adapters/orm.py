from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from moonbot.domain.bot import Direction


class Base(DeclarativeBase):
    pass


class Bot(Base):
    __tablename__ = "bot"

    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[int]
    y: Mapped[int]
    direction: Mapped[Direction]


class Command(Base):
    __tablename__ = "command"

    id: Mapped[int] = mapped_column(primary_key=True)
    instructions: Mapped[str]
