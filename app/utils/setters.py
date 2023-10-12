from aiogram.types import Message

import app.database as db
import app.utils as utils


async def registration(message: Message, user: list):
    isError = False

    if not user:
        if db.insertUser(message.from_user.id):
            await registration(message, db.getUser(message.from_user.id))
        else:
            isError = True
    elif user[0]['FIO'] is None:
        if db.updateState(message.from_user.id, "setFIO"):
            await utils.messageSetFIO(message)
        else:
            isError = True
    elif user[0]['email'] is None:
        if db.updateState(message.from_user.id, "setEmail"):
            await utils.messageSetEmail(message)
        else:
            isError = True
    elif user[0]['tel'] is None:
        if db.updateState(message.from_user.id, "setTel"):
            await utils.messageSetTel(message)
        else:
            isError = True
    elif len(db.getUserCategories(message.from_user.id)) < 1:
        if db.updateState(message.from_user.id, "setUserCategories"):
            await utils.messageSetUserCategories(message)
        else:
            isError = True


    if isError:
        await utils.messageError(message)


