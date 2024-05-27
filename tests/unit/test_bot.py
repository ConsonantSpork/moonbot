import pytest
from pydantic import ValidationError

from moonbot.domain.bot import Bot, Direction, State
from moonbot.domain.exceptions import InvalidCommand


@pytest.fixture
def bot():
    return Bot(1, 2, Direction.WEST)


def test_bot_returns_current_state(bot: Bot):
    assert bot.state == State(x=1, y=2, direction=Direction.WEST)


def test_bot_can_move_and_returns_new_state_after_moving(bot: Bot):
    state = bot.move("FLFFFRFLB")
    assert state == bot.state
    assert state == State(x=-1, y=0, direction=Direction.SOUTH)


@pytest.mark.parametrize(
    "args",
    [
        (1, 2, "west"),
        (0.5, 3, Direction.WEST),
    ],
)
def test_validation_error_is_raised_on_invalid_constructor_arguments(args):
    with pytest.raises(ValidationError):
        Bot(*args)


def test_validation_error_is_raised_on_invalid_move_command(bot):
    with pytest.raises(InvalidCommand):
        bot.move("FLFINVALID")
