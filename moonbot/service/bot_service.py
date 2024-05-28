from moonbot.adapters.exceptions import BotNotFound
from moonbot.domain.bot import Bot, Direction, State
from moonbot.service.uow import UnitOfWork

DEFAULT_BOT_STATE = State(x=0, y=0, direction=Direction.NORTH)


class BotService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def _maybe_initialize_bot_state(self):
        try:
            return self._uow.bot.get()
        except BotNotFound:
            bot = Bot(
                DEFAULT_BOT_STATE.x, DEFAULT_BOT_STATE.y, DEFAULT_BOT_STATE.direction
            )
            self._uow.bot.update(bot)
            self._uow.commit()
            return bot

    def get_current_state(self) -> State:
        with self._uow:
            bot = self._maybe_initialize_bot_state()
        return bot.state

    def move(self, command: str) -> State:
        with self._uow:
            bot = self._maybe_initialize_bot_state()
            bot.move(command)
            self._uow.bot.update(bot)
            self._uow.commands.add(command)
            self._uow.commit()
        return bot.state
