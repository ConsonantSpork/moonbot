import pytest

from moonbot.domain.bot import Bot, Direction


@pytest.fixture
def bot() -> Bot:
    return Bot(1, 2, Direction.WEST)
