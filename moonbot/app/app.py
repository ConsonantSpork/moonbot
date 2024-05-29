from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status

from moonbot.domain.exceptions import InvalidCommand
from moonbot.service.bot_service import BotService
from moonbot.service.uow import SqlAlchemyUnitOfWork

app = FastAPI()


@app.get("/state")
def get_state():
    bot_service = BotService(SqlAlchemyUnitOfWork())
    state = bot_service.get_current_state()
    return JSONResponse(str(state))


@app.post("/move")
def move(command: str):
    bot_service = BotService(SqlAlchemyUnitOfWork())
    try:
        state = bot_service.move(command)
        return JSONResponse(str(state))
    except InvalidCommand as e:
        return JSONResponse(str(e), status.HTTP_400_BAD_REQUEST)
