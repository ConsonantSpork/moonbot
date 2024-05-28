import pytest

from moonbot.adapters.bot_repository import SQLAlchemyBotRepository
from moonbot.adapters.exceptions import BotNotFound
from moonbot.domain.bot import Bot


@pytest.fixture
def empty_respository(session) -> SQLAlchemyBotRepository:
    return SQLAlchemyBotRepository(session)


@pytest.fixture
def repository(session, bot) -> SQLAlchemyBotRepository:
    repo = SQLAlchemyBotRepository(session)
    repo.update(bot)
    return repo


def test_updating_bot_when_repository_empty_adds_it(empty_respository, bot):
    empty_respository.update(bot)
    empty_respository._session.commit()


def test_can_get_bot(repository, bot):
    new_bot = repository.get()
    new_bot.state == bot.state


def test_trying_to_get_bot_when_repository_empty_raises_exception(empty_respository):
    with pytest.raises(BotNotFound):
        empty_respository.get()


def test_can_update_bot(repository):
    bot = repository.get()
    bot_with_new_state = Bot(
        x=bot.state.x + 1, y=bot.state.y - 1, direction=bot.state.direction
    )
    repository.update(bot_with_new_state)
    saved_bot = repository.get()
    assert saved_bot.state == bot_with_new_state.state
