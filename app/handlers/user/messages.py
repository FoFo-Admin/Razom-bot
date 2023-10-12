from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType

import phonenumbers

import app.database as db
import app.utils as utils

import app.filters as filters

router = Router(name="user_message_router")


@router.message(CommandStart(), F.chat.type == "private")
async def start_handler(message: Message):
    user = db.getUser(message.from_user.id)
    if not user:
        await utils.messageRegister(message)
        await utils.registration(message, user)
    elif user[0]['role'] is None:
        await utils.registration(message, user)
    else:
        await utils.startMessage(message)


@router.message(F.text, filters.IsState('setFIO'))
async def fio_handler(message: Message):
    if utils.checkFIO(message):
        db.updateFIO(message.from_user.id, message.text)
        await start_handler(message)
    else:
        await utils.messageWrongFIO(message)


@router.message(F.text, filters.IsState('setEmail'))
async def email_handler(message: Message):
    if utils.checkEmail(message):
        if db.updateEmail(message.from_user.id, message.text):
            await start_handler(message)
        else:
            await utils.messageNotUniqueEmail(message)
    else:
        await utils.messageWrongEmail(message)


@router.message(F.text, filters.IsState('setTel'))
async def email_handler(message: Message):
    if utils.checkTel(message):
        if db.updateTel(message.from_user.id, phonenumbers.format_number(phonenumbers.parse(message.text, "UA"),
                                                                      phonenumbers.PhoneNumberFormat.INTERNATIONAL)):
            await start_handler(message)
        else:
            await utils.messageNotUniqueTel(message)
    else:
        await utils.messageWrongTel(message)


@router.message()
async def default_handler(message: Message):
    await utils.defaultMessage(message)
