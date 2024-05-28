from abc import ABC, abstractmethod

from moonbot.adapters.orm import Command as CommandDAO


class CommandRepository(ABC):
    @abstractmethod
    def add(self, command: str):
        raise NotImplementedError


class SQLAlchemyCommandRepository(CommandRepository):
    def __init__(self, session):
        self._session = session

    def add(self, command: str):
        self._session.add(CommandDAO(instructions=command))
