from aiogram.filters import Filter
from aiogram.types import Message

import app.database as db


class IsState(Filter):
    def __init__(self, state: str) -> None:
        self.state = state

    async def __call__(self, message: Message) -> bool:
        return self.state == db.getUser(message.from_user.id)[0]['state']


class IsPartOfState(Filter):
    def __init__(self, state: str) -> None:
        self.state = state

    async def __call__(self, message: Message) -> bool:
        return self.state == db.getUser(message.from_user.id)[0]['state'].split(":")[0]


class IsAdmin(Filter):
    async def __call__(self, message: Message):
        user = db.getUser(message.from_user.id)
        if user:
            return "admin" == user[0]['role']
        return False
