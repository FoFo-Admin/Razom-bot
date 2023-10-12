from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery, ContentType

import app.database as db
import app.utils as utils
import app.callbacks as cb

import app.filters as filters

router = Router(name="admin_callbacks_router")


@router.callback_query(filters.IsAdmin(), filters.IsState('main'), cb.CallbackAdminActions.filter(F.action == 'newSchedule'))
async def new_schedule_handler(query: CallbackQuery):
    db.updateState(query.from_user.id, 'setSchedule')
    await utils.messageAddSchedule(query)


@router.callback_query(filters.IsAdmin(), filters.IsState('main'), cb.CallbackAdminActions.filter(F.action == 'usersExcel'))
async def new_schedule_handler(query: CallbackQuery):
    await utils.messageUsersExcel(query)


@router.callback_query(filters.IsAdmin(), filters.IsState('main'), cb.CallbackAdminActions.filter(F.action == 'editTime'))
async def new_letter_handler(query: CallbackQuery):
    db.updateState(query.from_user.id, 'editTime')
    await utils.messageEditTime(query)


@router.callback_query(filters.IsAdmin(), filters.IsState('editTime'), cb.CallbackAdminActions.filter(F.action == 'dayRemind'))
async def day_remind_handler(query: CallbackQuery):
    db.updateState(query.from_user.id, 'dayRemind')
    await utils.messageDayRemind(query)


@router.callback_query(filters.IsAdmin(), filters.IsState('editTime'), cb.CallbackAdminActions.filter(F.action == 'startEvent'))
@router.callback_query(filters.IsAdmin(), filters.IsState('editTime'), cb.CallbackAdminActions.filter(F.action == 'endEvent'))
async def start_end_handler(query: CallbackQuery, callback_data: cb.CallbackAdminActions):
    db.updateState(query.from_user.id, f'{callback_data.action}')
    await utils.messageStartEndEvent(query)


@router.callback_query(filters.IsAdmin(), filters.IsState('main'), cb.CallbackAdminActions.filter(F.action == 'newLetter'))
async def new_letter_handler(query: CallbackQuery):
    db.updateState(query.from_user.id, 'newLetter')
    await utils.messageNewLetter(query)


@router.callback_query(filters.IsAdmin(), filters.IsState('main'), cb.CallbackSelectSchedule.filter(F.action == 'select'))
async def select_schedule_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    schedule = db.getScheduleById(callback_data.scheduleId)
    if schedule:
        await utils.messageSchedule(query, schedule)
    else:
        await utils.messageErrorQuery(query)


async def checkIfSchedule(query: CallbackQuery, callback_data):
    schedule = db.getScheduleById(callback_data.scheduleId)
    if schedule and db.getUser(query.from_user.id)[0]['state'].split(":")[1] == str(callback_data.scheduleId):
        return True
    else:
        await utils.messageErrorQuery(query)
        return False


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackSelectSchedule.filter(F.action == 'newEvent'))
async def select_schedule_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    if await checkIfSchedule(query, callback_data):
        db.updateState(query.from_user.id, f"{callback_data.action}:{callback_data.scheduleId}")
        await utils.messageAddEvent(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackSelectSchedule.filter(F.action == 'editName'))
async def edit_schedule_name_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    if await checkIfSchedule(query, callback_data):
        db.updateState(query.from_user.id, f"{callback_data.action}:{callback_data.scheduleId}")
        await utils.messageEditNameSchedule(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackSelectSchedule.filter(F.action == 'editImage'))
async def edit_schedule_image_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    if await checkIfSchedule(query, callback_data):
        db.updateState(query.from_user.id, f"{callback_data.action}:{callback_data.scheduleId}")
        await utils.messageEditImageSchedule(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackSelectSchedule.filter(F.action == 'deleteSchedule'))
async def delete_schedule_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    if await checkIfSchedule(query, callback_data):
        db.updateState(query.from_user.id, f"{callback_data.action}:{callback_data.scheduleId}")
        await utils.messageDeleteSchedule(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackSelectSchedule.filter(F.action == 'usersExcel'))
async def schedule_excel_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    if await checkIfSchedule(query, callback_data):
        await utils.messageScheduleExcel(query, callback_data.scheduleId)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackSelectSchedule.filter(F.action == 'makePublic'))
async def delete_schedule_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    if await checkIfSchedule(query, callback_data):
        db.updateState(query.from_user.id, f"{callback_data.action}:{callback_data.scheduleId}")
        await utils.messageMakePublicSchedule(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackSelectSchedule.filter(F.action == 'makePrivate'))
async def delete_schedule_handler(query: CallbackQuery, callback_data: cb.CallbackSelectSchedule):
    if await checkIfSchedule(query, callback_data):
        db.updateState(query.from_user.id, f"{callback_data.action}:{callback_data.scheduleId}")
        await utils.messageMakePrivateSchedule(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackScheduleEvent.filter(F.action == 'edit'))
async def edit_event_handler(query: CallbackQuery, callback_data: cb.CallbackScheduleEvent):
    if await checkIfSchedule(query, callback_data):
        event = db.getEventById(callback_data.eventId)
        if event:
            db.updateState(query.from_user.id, f"editEvent:{callback_data.scheduleId}:{callback_data.eventId}")
            await utils.messageEditEvent(query, event)


@router.callback_query(filters.IsAdmin(), filters.IsState('setSchedule'), cb.CallbackBackTo.filter(F.to == 'main'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('newLetter'), cb.CallbackBackTo.filter(F.to == 'main'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('editTime'), cb.CallbackBackTo.filter(F.to == 'main'))
async def back_to_main_handler(query: CallbackQuery):
    await utils.startAdminQueryEdit(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('lookAtSchedule'), cb.CallbackBackTo.filter(F.to == 'main'))
async def back_to_main_handler(query: CallbackQuery):
    await utils.startAdminQuery(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('dayRemind'), cb.CallbackBackTo.filter(F.to == 'editTime'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('startEvent'), cb.CallbackBackTo.filter(F.to == 'editTime'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('endEvent'), cb.CallbackBackTo.filter(F.to == 'editTime'))
async def back_to_edit_time_handler(query: CallbackQuery):
    db.updateState(query.from_user.id, 'editTime')
    await utils.messageEditTime(query)


@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('newEvent'), cb.CallbackBackTo.filter(F.to == 'lookAtSchedule'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('editEvent'), cb.CallbackBackTo.filter(F.to == 'lookAtSchedule'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('editName'), cb.CallbackBackTo.filter(F.to == 'lookAtSchedule'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('editImage'), cb.CallbackBackTo.filter(F.to == 'lookAtSchedule'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('deleteSchedule'), cb.CallbackBackTo.filter(F.to == 'lookAtSchedule'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('makePublic'), cb.CallbackBackTo.filter(F.to == 'lookAtSchedule'))
@router.callback_query(filters.IsAdmin(), filters.IsPartOfState('makePrivate'), cb.CallbackBackTo.filter(F.to == 'lookAtSchedule'))
async def back_to_look_At_Schedule_handler(query: CallbackQuery):
    schedule = db.getScheduleById(db.getUser(query.from_user.id)[0]['state'].split(":")[1])
    if schedule:
        await utils.messageSchedule(query, schedule)
    else:
        await utils.messageErrorQuery(query)
