import re
import phonenumbers

from datetime import datetime

from email_validate import validate
from aiogram.types import Message

import app.utils as utils


def checkFIO(message: Message):
    return 3 < len(re.sub(' +', ' ', message.text.strip())) < 100


def checkEmail(message: Message):
    return validate(message.text)


def checkTel(message: Message):
    try:
        return phonenumbers.is_valid_number(phonenumbers.parse(message.text, "UA"))
    except Exception as e:
        print(e)
        return False


async def checkEvent(message: Message):
    parts = message.text.split("\n")

    if len(parts) == 3:
        try:
            dt = datetime.strptime(parts[1], "%Y-%m-%d %H:%M")
            if datetime.now() >= dt:
                await utils.messageWrongEventDate(message)
                return False
        except ValueError:
            await utils.messageWrongEventDate(message)
            return False
        try:
            people = int(parts[2])
            if people <= 0:
                await utils.messageWrongEventPeople(message)
                return False
        except ValueError:
            await utils.messageWrongEventPeople(message)
            return False
        return True
    else:
        await utils.messageWrongEventParts(message)
        return False


async def checkTime(message: Message, time: str):
    try:
        timeInt = int(message.text)
        if time == 'dayRemind':
            if 1 <= timeInt <= 23:
                return True
            else:
                await utils.messageError(message)
                return False
        elif -120 <= timeInt <= 120:
            return True
        else:
            await utils.messageError(message)
            return False
    except ValueError:
        await utils.messageError(message)
        return False