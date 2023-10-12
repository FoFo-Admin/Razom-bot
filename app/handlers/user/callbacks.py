from datetime import datetime, timedelta

from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery, ContentType

import app.database as db
import app.utils as utils
import app.callbacks as cb

import app.filters as filters

router = Router(name="user_callbacks_router")


@router.callback_query(cb.CallbackCategory.filter(F.action == 'add_category'), filters.IsState('setUserCategories'))
async def addcategory_handler(query: CallbackQuery, callback_data: cb.CallbackCategory):
    if db.getCategoryById(callback_data.categoryId)[0]['name'] == "Не відношусь до жодної з зазначених категорій":
        db.deleteUserCategoriesNotCategory(query.from_user.id, callback_data.categoryId)
        db.insertUserCategory(query.from_user.id, callback_data.categoryId)
    else:
        db.deleteUserCategoriesCategory(query.from_user.id, callback_data.categoryId)
        db.insertUserCategory(query.from_user.id, callback_data.categoryId)
    await utils.editSetUserCategories(query)


@router.callback_query(cb.CallbackCategory.filter(F.action == 'delete_category'), filters.IsState('setUserCategories'))
async def deletecategory_handler(query: CallbackQuery, callback_data: cb.CallbackCategory):
    if len(db.getUserCategories(query.from_user.id)) == 1:
        await utils.messageWrongUserCategories(query)
    else:
        db.deleteUserCategoriesById(query.from_user.id, callback_data.categoryId)
        await utils.editSetUserCategories(query)


@router.callback_query(cb.CallbackCategory.filter(F.action == 'ready'), filters.IsState('setUserCategories'))
async def readycategory_handler(query: CallbackQuery, callback_data: cb.CallbackCategory):
    if len(db.getUserCategories(query.from_user.id)) < 0:
        await utils.messageWrongUserCategories(query)
    else:
        db.updateRole(query.from_user.id, "user")
        await utils.startQuery(query)


def checkIfUserSchedule(query: CallbackQuery, callback_data):
    schedule = db.getScheduleById(callback_data.scheduleId)
    if schedule:
        if schedule[0]['status'] == 'public':
            return True
    return False


def checkIfScheduleCallback(query: CallbackQuery, callback_data):
    if str(callback_data.scheduleId) == db.getUser(query.from_user.id)[0]['state'].split(":")[1]:
        return True
    return False


def checkIfEventCallback(query: CallbackQuery, callback_data):
    if str(callback_data.eventId) == db.getUser(query.from_user.id)[0]['state'].split(":")[2]:
        return True
    return False


@router.callback_query(~filters.IsAdmin(), cb.CallbackSelectSchedule.filter(F.action == 'select'))
async def select_schedule_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    schedule = db.getScheduleById(callback_data.scheduleId)
    if checkIfUserSchedule(query, callback_data):
        db.updateState(query.from_user.id, f"lookAtSchedule:{callback_data.scheduleId}")
        await utils.messageScheduleUser(query, schedule)
    else:
        await utils.messageErrorQuery(query)


@router.callback_query(~filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackScheduleEvent.filter(F.action == 'register'))
async def register_event_handler(query: CallbackQuery, callback_data: cb.CallbackScheduleEvent):
    if checkIfUserSchedule(query, callback_data) and checkIfScheduleCallback(query, callback_data):
        event = db.getEventById(callback_data.eventId)
        if event:
            if datetime.now() > datetime.strptime(event[0]['datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=db.getTimeConfiguration('startEvent')[0]['timeInt']):
                await utils.messageErrorEventDate(query)
            elif len(db.getUserEventsByEventId(callback_data.eventId)) >= event[0]['maxPeople']:
                await utils.messageErrorEventPeople(query)
            else:
                db.updateState(query.from_user.id, f"register:{callback_data.scheduleId}:{callback_data.eventId}")
                await utils.messageConfirmRegistration(query, callback_data.scheduleId, callback_data.eventId)
    else:
        await utils.messageErrorQuery(query)


@router.callback_query(~filters.IsAdmin(), filters.IsPartOfState("register"), cb.CallbackScheduleEvent.filter(F.action == 'confirm'))
async def confirm_register_event_handler(query: CallbackQuery, callback_data: cb.CallbackScheduleEvent):
    if checkIfUserSchedule(query, callback_data) and checkIfScheduleCallback(query, callback_data):
        event = db.getEventById(callback_data.eventId)
        if event and checkIfEventCallback(query, callback_data):
            if datetime.now() > datetime.strptime(event[0]['datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=db.getTimeConfiguration('startEvent')[0]['timeInt']):
                await utils.messageErrorEventDate(query)
            elif len(db.getUserEventsByEventId(callback_data.eventId)) >= event[0]['maxPeople']:
                await utils.messageErrorEventPeople(query)
            else:
                db.insertUserEvent(query.from_user.id, callback_data.eventId)
                db.updateState(query.from_user.id,
                               f"lookAtSchedule:{db.getScheduleById(callback_data.scheduleId)[0]['id']}")
                await utils.messageScheduleUser(query, db.getScheduleById(callback_data.scheduleId))
        else:
            await utils.messageErrorQuery(query)
    else:
        await utils.messageErrorQuery(query)


@router.callback_query(~filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackScheduleEvent.filter(F.action == 'unregister'))
async def unregister_event_handler(query: CallbackQuery, callback_data: cb.CallbackScheduleEvent):
    if checkIfUserSchedule(query, callback_data) and checkIfScheduleCallback(query, callback_data):
        event = db.getEventById(callback_data.eventId)
        if event:
            db.updateState(query.from_user.id, f"unregister:{callback_data.scheduleId}:{callback_data.eventId}")
            await utils.messageConfirmUnregistration(query, callback_data.scheduleId, callback_data.eventId)
    else:
        await utils.messageErrorQuery(query)


@router.callback_query(~filters.IsAdmin(), filters.IsPartOfState("unregister"), cb.CallbackScheduleEvent.filter(F.action == 'confirm'))
async def confirm_unregister_event_handler(query: CallbackQuery, callback_data: cb.CallbackScheduleEvent):
    if checkIfUserSchedule(query, callback_data) and checkIfScheduleCallback(query, callback_data):
        event = db.getEventById(callback_data.eventId)
        if event and checkIfEventCallback(query, callback_data):
            db.deleteUserEvent(query.from_user.id, callback_data.eventId)
            db.updateState(query.from_user.id, f"lookAtSchedule:{db.getScheduleById(callback_data.scheduleId)[0]['id']}")
            await utils.messageScheduleUser(query, db.getScheduleById(callback_data.scheduleId))
        else:
            await utils.messageErrorQuery(query)
    else:
        await utils.messageErrorQuery(query)


@router.callback_query(~filters.IsAdmin(), cb.CallbackScheduleEvent.filter(F.action == 'onEvent'))
@router.callback_query(~filters.IsAdmin(), cb.CallbackScheduleEvent.filter(F.action == 'onEventNot'))
async def on_event_handler(query: CallbackQuery, callback_data: cb.CallbackScheduleEvent):
    if checkIfUserSchedule(query, callback_data):
        event = db.getEventById(callback_data.eventId)
        if event:
            if event[0]['status'] == 'started':
                if callback_data.action == 'onEvent':
                    db.updateUserEventStatus(query.from_user.id, callback_data.eventId, 'yes')
                else:
                    db.updateUserEventStatus(query.from_user.id, callback_data.eventId, 'no')
                await utils.updateWasUserOnEvent(query)
            else:
                await utils.updateErrorWasUserOnEvent(query)
        else:
            await utils.messageErrorQuery(query)
    else:
        await utils.messageErrorQuery(query)


@router.callback_query(~filters.IsAdmin(), cb.CallbackBackTo.filter(F.to == 'main'))
async def back_to_main_handler(query: CallbackQuery):
    await utils.startQuery(query)


@router.callback_query(~filters.IsAdmin(), filters.IsPartOfState("register"), cb.CallbackBackTo.filter(F.to == "lookAtSchedule"))
@router.callback_query(~filters.IsAdmin(), filters.IsPartOfState("unregister"), cb.CallbackBackTo.filter(F.to == "lookAtSchedule"))
async def back_to_look_at_schedule_handler(query: CallbackQuery):
    schedule = db.getScheduleById(db.getUser(query.from_user.id)[0]['state'].split(":")[1])
    if schedule:
        db.updateState(query.from_user.id, f"lookAtSchedule:{schedule[0]['id']}")
        await utils.messageScheduleUser(query, schedule)
    else:
        await utils.messageErrorQuery(query)


@router.callback_query()
async def default_handler(query: CallbackQuery):
    await utils.defaultMessageQuery(query)

