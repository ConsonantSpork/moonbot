import pytest

from moonbot.adapters.bot_repository import BotRepository
from moonbot.adapters.command_repository import CommandRepository
from moonbot.adapters.exceptions import BotNotFound
from moonbot.domain.bot import Bot, Direction
from moonbot.service.bot_service import DEFAULT_BOT_STATE, BotService
from moonbot.service.uow import UnitOfWork


class FakeBotRepository(BotRepository):
    def __init__(self):
        self._bot = None

    def get(self) -> Bot:
        if self._bot is None:
            raise BotNotFound
        return self._bot

    def update(self, bot: Bot) -> None:
        self._bot = bot


class FakeCommandRepository(CommandRepository):
    def __init__(self):
        self._commands = []

    def add(self, command: str):
        self._commands.append(command)


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.bot = FakeBotRepository()
        self.commands = FakeCommandRepository()
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


@pytest.fixture
def uow():
    uow = FakeUnitOfWork()
    uow.bot.update(Bot(1, 2, Direction.WEST))
    return uow


@pytest.fixture
def uow_no_bot_state():
    return FakeUnitOfWork()


def test_get_current_state(uow):
    bot_service = BotService(uow)
    state = bot_service.get_current_state()
    assert state
    assert state == uow.bot.get().state


def test_move_returns_new_state(uow):
    bot_service = BotService(uow)
    old_state = bot_service.get_current_state()
    command = "FFRFLB"
    new_state = bot_service.move(command)
    bot = Bot(old_state.x, old_state.y, old_state.direction)
    bot.move(command)
    expected_state = bot.state
    assert new_state == expected_state


def test_move_commits(uow):
    bot_service = BotService(uow)
    bot_service.move("FRFBLF")
    assert uow.commited


def test_move_saves_command(uow):
    bot_service = BotService(uow)
    command = "FRFBLF"
    bot_service.move(command)
    assert uow.commands._commands == [command]


def test_move_updates_bot_state(uow):
    bot_service = BotService(uow)
    command = "FFFFFF"
    bot_service.move(command)
    assert uow.commands._commands == [command]


def test_get_current_state_initializes_bot_state(uow_no_bot_state):
    bot_service = BotService(uow_no_bot_state)
    bot_service.get_current_state()
    state = uow_no_bot_state.bot.get().state
    assert state == DEFAULT_BOT_STATE


def test_move_initializes_bot_state(uow_no_bot_state):
    bot_service = BotService(uow_no_bot_state)
    bot_service.move("BBFLRL")
    state = uow_no_bot_state.bot.get().state
    assert state
