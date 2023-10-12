from aiogram.filters.callback_data import CallbackData


class CallbackCategory(CallbackData, prefix='category'):
    action: str
    categoryId: int


class CallbackAdminActions(CallbackData, prefix='admin'):
    action: str


class CallbackSelectSchedule(CallbackData, prefix='schedule'):
    action: str
    scheduleId: int


class CallbackScheduleEvent(CallbackData, prefix='event'):
    action: str
    scheduleId: int
    eventId: int


class CallbackBackTo(CallbackData, prefix='back'):
    to: str
