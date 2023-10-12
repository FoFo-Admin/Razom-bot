from aiogram import Router, Bot
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.database as db
import app.utils as utils

import app.filters as filters
import app.keyboards as keyboard

import app.scheduler as scheduler
from init import scheduler as s


router = Router(name="admin_message_router")


@router.message(CommandStart(), filters.IsAdmin())
async def start_admin_handler(message: Message):
    await utils.startAdminMessage(message)


@router.message(F.photo, filters.IsAdmin(), filters.IsState('setSchedule'))
async def add_schedule_handler(message: Message):
    if message.caption:
        db.insertSchedule(message.caption, message.photo[-1].file_id)
        await utils.startAdminMessage(message)


@router.message(F.text, filters.IsAdmin(), filters.IsState('newLetter'))
@router.message(F.video, filters.IsAdmin(), filters.IsState('newLetter'))
@router.message(F.document, filters.IsAdmin(), filters.IsState('newLetter'))
@router.message(F.photo, filters.IsAdmin(), filters.IsState('newLetter'))
@router.message(F.poll, filters.IsAdmin(), filters.IsState('newLetter'))
async def send_letter_handler(message: Message, bot: Bot):
    users = db.getUsers()
    if message.text:
        for user in users:
            await bot.send_message(chat_id=user['id'], text=message.text)
        await utils.startAdminMessage(message)
    elif message.photo and message.caption:
        for user in users:
            await bot.send_photo(chat_id=user['id'], photo=message.photo[-1].file_id, caption=message.caption)
        await utils.startAdminMessage(message)
    elif message.video and message.caption:
        for user in users:
            await bot.send_video(chat_id=user['id'], video=message.video.file_id, caption=message.caption)
        await utils.startAdminMessage(message)
    elif message.document and message.caption:
        for user in users:
            await bot.send_document(chat_id=user['id'], document=message.document.file_id, caption=message.caption)
        await utils.startAdminMessage(message)
    elif message.poll:
        for user in users:
            await bot.forward_message(chat_id=user['id'], from_chat_id=message.from_user.id, message_id=message.message_id)
        await utils.startAdminMessage(message)
    else:
        await utils.messageError(message)


@router.message(F.text, filters.IsAdmin(), filters.IsState('dayRemind'))
async def edit_day_remind_handler(message: Message, bot: Bot):
    if await utils.checkTime(message, 'dayRemind'):
        db.updateTime('dayRemind', int(message.text))
        scheduler.editRemindJob(s, bot)
        db.updateState(message.from_user.id, 'editTime')
        await utils.messageEditTimeMessage(message)


@router.message(F.text, filters.IsAdmin(), filters.IsState('startEvent'))
async def edit_start_remind_handler(message: Message):
    if await utils.checkTime(message, 'startEvent'):
        db.updateTime('startEvent', int(message.text))
        db.updateState(message.from_user.id, 'editTime')
        await utils.messageEditTimeMessage(message)


@router.message(F.text, filters.IsAdmin(), filters.IsState('endEvent'))
async def edit_end_remind_handler(message: Message):
    if await utils.checkTime(message, 'endEvent'):
        db.updateTime('endEvent', int(message.text))
        db.updateState(message.from_user.id, 'editTime')
        await utils.messageEditTimeMessage(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('editName'))
async def edit_schedule_name_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    schedule = db.getScheduleById(ScheduleId)
    if schedule:
        if db.updateScheduleName(id=ScheduleId, name=message.text):
            await utils.messageScheduleMessage(message, db.getScheduleById(ScheduleId))
        else:
            await utils.messageError(message)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('editImage'), F.photo)
async def edit_schedule_image_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    schedule = db.getScheduleById(ScheduleId)
    if schedule:
        if db.updateScheduleImage(id=ScheduleId, image=message.photo[-1].file_id):
            await utils.messageScheduleMessage(message, db.getScheduleById(ScheduleId))
        else:
            await utils.messageError(message)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('newEvent'))
async def add_event_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    schedule = db.getScheduleById(ScheduleId)
    if schedule:
        if await utils.checkEvent(message):
            parts = message.text.split("\n")
            if db.insertScheduleEvent(name=parts[0], maxPeople=int(parts[2]), datetime=parts[1], ScheduleId=ScheduleId):
                await utils.messageScheduleMessage(message, schedule)
            else:
                await utils.messageError(message)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('deleteSchedule'), F.text == "Видалити")
async def delete_schedule_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    schedule = db.getScheduleById(ScheduleId)
    if schedule:
        db.deleteUserEventsByScheduleId(ScheduleId)
        db.deleteEventByScheduleId(ScheduleId)
        db.deleteScheduleById(ScheduleId)
        await utils.startAdminMessage(message)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('makePublic'), F.text == "Опублікувати")
async def publish_schedule_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    schedule = db.getScheduleById(ScheduleId)
    if schedule:
        db.updateScheduleStatus(ScheduleId, 'public')
        await utils.startAdminMessage(message)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('makePublic'))
async def publish_schedule_handler(message: Message, bot: Bot):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    schedule = db.getScheduleById(ScheduleId)
    if schedule:
        users = db.getUsers()
        db.updateScheduleStatus(ScheduleId, 'public')
        for user in users:
            await bot.send_photo(chat_id=user['id'], photo=schedule[0]['image'], caption=message.text, reply_markup=keyboard.keyboardGoTo(schedule[0]['id']))
        await utils.startAdminMessage(message)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('makePrivate'), F.text == "Видалити")
async def close_schedule_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    schedule = db.getScheduleById(ScheduleId)
    if schedule:
        db.updateScheduleStatus(ScheduleId, 'private')
        await utils.startAdminMessage(message)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('editEvent'), F.text == "Видалити")
async def delete_event_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    eventId = db.getUser(message.from_user.id)[0]['state'].split(":")[2]

    schedule = db.getScheduleById(ScheduleId)
    event = db.getEventById(eventId)

    if schedule and event:
        db.deleteUserEventsByEventId(eventId)
        db.deleteEventById(eventId)
        await utils.messageScheduleMessage(message, schedule)
    else:
        await utils.messageError(message)


@router.message(filters.IsAdmin(), filters.IsPartOfState('editEvent'))
async def editevent_handler(message: Message):
    ScheduleId = db.getUser(message.from_user.id)[0]['state'].split(":")[1]
    eventId = db.getUser(message.from_user.id)[0]['state'].split(":")[2]

    schedule = db.getScheduleById(ScheduleId)
    event = db.getEventById(eventId)

    if schedule and event:
        if await utils.checkEvent(message):
            parts = message.text.split("\n")
            if db.updateEvent(id=eventId, name=parts[0], maxPeople=int(parts[2]), datetime=parts[1]):
                await utils.messageScheduleMessage(message, schedule)
            else:
                await utils.messageError(message)
    else:
        await utils.messageError(message)
