from abc import ABC, abstractmethod

from sqlalchemy import exc, select

from moonbot.adapters.exceptions import BotNotFound
from moonbot.adapters.orm import Bot as BotDAO
from moonbot.domain.bot import Bot


class BotRepository(ABC):
    @abstractmethod
    def get(self) -> Bot:
        raise NotImplementedError

    @abstractmethod
    def update(self, bot: Bot) -> None:
        raise NotImplementedError


BOT_ID = "1"


class SQLAlchemyBotRepository(BotRepository):
    def __init__(self, session):
        self._session = session

    def _get_existing_dao(self) -> BotDAO | None:
        try:
            stmt = select(BotDAO).where(BotDAO.id == BOT_ID)
            return self._session.scalars(stmt).one()
        except exc.NoResultFound:
            return None

    def get(self) -> Bot:
        bot_dao = self._get_existing_dao()
        if bot_dao is None:
            raise BotNotFound
        return Bot(bot_dao.x, bot_dao.y, bot_dao.direction)

    def update(self, bot: Bot) -> None:
        bot_dao = self._get_existing_dao()
        if bot_dao is None:
            bot_dao = BotDAO(id=BOT_ID)
        for k, v in bot.state.model_dump().items():
            setattr(bot_dao, k, v)
        self._session.add(bot_dao)
