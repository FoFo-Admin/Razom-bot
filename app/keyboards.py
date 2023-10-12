from datetime import datetime, timedelta

from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

import app.database as db
import app.callbacks as cb


def keyboardUserCategories(id: int):
    categories = db.getCategories()
    user_categories = db.getUserCategories(id)

    STR = """for category in categories:
        isUser = False
        for user_category in user_categories:
            if category['name'] == user_categories["name"]:
                isUser = True
        if(isUser):
            InlineKeyboardButton(text=f"✅{category['name']}✅", callback_data=f"delete_category={category['name']}")
        else:
            InlineKeyboardButton(text=f"{category['name']}", callback_data=f"add_category={category['name']}")
"""
    buttons = [[
        InlineKeyboardButton(
            text=f"✅{category['name']}✅",
            callback_data=cb.CallbackCategory(action="delete_category", categoryId=category['id']).pack()
        ) if category['id'] in {user_category['socialId'] for user_category in user_categories} else
        InlineKeyboardButton(
            text=f"{category['name']}",
            callback_data=cb.CallbackCategory(action="add_category", categoryId=category['id']).pack()
        )]
        for category in categories
    ]

    if len(user_categories) > 0:
        buttons.append([InlineKeyboardButton(text='Готово',
                                             callback_data=cb.CallbackCategory(action="ready", categoryId="-1").pack()
                                             )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def keyboardAdmin():
    schedules = db.getAllSchedules()

    schedulesButtons = [[
        InlineKeyboardButton(
            text=f"{'👥' if schedule['status'] == 'public' else '🔒'} {schedule['name']}",
            callback_data=cb.CallbackSelectSchedule(action="select", scheduleId=schedule['id']).pack()
        )]
        for schedule in schedules
    ]
    basicButtons = [
        [InlineKeyboardButton(text='➕ Додати новий розклад',
                              callback_data=cb.CallbackAdminActions(action="newSchedule").pack())],
        [InlineKeyboardButton(text='🕒 Змінити час нагадувань',
                              callback_data=cb.CallbackAdminActions(action="editTime").pack())],
        [InlineKeyboardButton(text='✍️Допис для всіх користувачей',
                              callback_data=cb.CallbackAdminActions(action="newLetter").pack())],
        [InlineKeyboardButton(text='📊 Інформація про всіх користувачей (Excel)',
                              callback_data=cb.CallbackAdminActions(action="usersExcel").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=(schedulesButtons + basicButtons))


def keyboardUser():
    schedules = db.getPublicSchedules()

    schedulesButtons = [[
        InlineKeyboardButton(
            text=schedule['name'],
            callback_data=cb.CallbackSelectSchedule(action="select", scheduleId=schedule['id']).pack()
        )]
        for schedule in schedules
    ]

    return InlineKeyboardMarkup(inline_keyboard=schedulesButtons)


def keyboardTime():

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Змінити час щоденного нагадування',
                                 callback_data=cb.CallbackAdminActions(action="dayRemind").pack())
        ],
        [
            InlineKeyboardButton(text='Змінити час повідомлення про присутність',
                                 callback_data=cb.CallbackAdminActions(action="startEvent").pack())
        ],
        [
            InlineKeyboardButton(text='Змінити час повідомлення адміністраторам',
                                 callback_data=cb.CallbackAdminActions(action="endEvent").pack())
        ],
        [
            InlineKeyboardButton(text='Назад',
                                 callback_data=cb.CallbackBackTo(to=f"main").pack())
        ]
    ])


def keyboardEvents(id, schedule):
    events = db.getEventsByScheduleId(schedule[0]['id'])
    userEvents = db.getUserEventsByUserId(id)

    schedulesButtons = [[
                            InlineKeyboardButton(
                                text=f"✅{event['name']}",
                                callback_data=cb.CallbackScheduleEvent(action="unregister",
                                                                       scheduleId=schedule[0]['id'],
                                                                       eventId=event['id']).pack()
                            )] if event['id'] in {userEvent['eventId'] for userEvent in userEvents} else [
        InlineKeyboardButton(
            text=f"""{"🚫" if len(db.getUserEventsByEventId(event['id'])) >= event['maxPeople']
                              or datetime.now() > datetime.strptime(event['datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=db.getTimeConfiguration('startEvent')[0]['timeInt']) else
            "🟡"}{event['name']}""",
            callback_data=cb.CallbackScheduleEvent(action="register", scheduleId=schedule[0]['id'],
                                                   eventId=event['id']).pack()
        )]

                        for event in events
                        ]

    backButton = [[
        InlineKeyboardButton(text='Назад',
                             callback_data=cb.CallbackBackTo(to=f"main").pack())
    ]]

    return InlineKeyboardMarkup(inline_keyboard=(schedulesButtons + backButton))


def keyboardIsOnEvent(event):
    eventButtons = [[
        InlineKeyboardButton(
            text=f"Так, я на заході",
            callback_data=cb.CallbackScheduleEvent(action="onEvent",
                                                   scheduleId=event[0]['scheduleId'],
                                                   eventId=event[0]['id']).pack()
        )],[
        InlineKeyboardButton(
            text=f"Ні, не зміг прийти",
            callback_data=cb.CallbackScheduleEvent(action="onEventNot",
                                                   scheduleId=event[0]['scheduleId'],
                                                   eventId=event[0]['id']).pack()
    )]]

    return InlineKeyboardMarkup(inline_keyboard=eventButtons)


def keyboardSchedule(schedule, events):
    eventsButtons = [[
        InlineKeyboardButton(
            text=f"{event['name']}",
            callback_data=cb.CallbackScheduleEvent(action="edit", scheduleId=schedule[0]['id'],
                                                   eventId=event['id']).pack()
        )]
        for event in events
    ]

    basicButtons = [
        [InlineKeyboardButton(text='➕ Додати новий захід',
                              callback_data=cb.CallbackSelectSchedule(action="newEvent",
                                                                      scheduleId=schedule[0]['id']).pack())],
        [InlineKeyboardButton(text='📝️Змінити назву',
                              callback_data=cb.CallbackSelectSchedule(action="editName",
                                                                      scheduleId=schedule[0]['id']).pack()),
         InlineKeyboardButton(text='🖼️Змінити фото',
                              callback_data=cb.CallbackSelectSchedule(action="editImage",
                                                                      scheduleId=schedule[0]['id']).pack())
         ],
        [InlineKeyboardButton(text='📊 Статистика розкладу',
                              callback_data=cb.CallbackSelectSchedule(action="usersExcel",
                                                                      scheduleId=schedule[0]['id']).pack())],
        [InlineKeyboardButton(
            text=f"{'🔒 Сховати розклад' if schedule[0]['status'] == 'public' else '👥 Опублікувати розклад'}",
            callback_data=cb.CallbackSelectSchedule
            (action=f"{'makePrivate' if schedule[0]['status'] == 'public' else 'makePublic'}",
             scheduleId=schedule[0]['id']).pack()),
         InlineKeyboardButton(text='🗑️Видалити розклад',
                              callback_data=cb.CallbackSelectSchedule(action="deleteSchedule",
                                                                      scheduleId=schedule[0]['id']).pack())
         ],
        [InlineKeyboardButton(text='Назад',
                              callback_data=cb.CallbackBackTo(to="main").pack())
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=(eventsButtons + basicButtons))


def keyboardConfirm(scheduleId, eventId):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Підтвердити",
                                 callback_data=cb.CallbackScheduleEvent(action="confirm", scheduleId=f"{scheduleId}",
                                                                        eventId=f"{eventId}").pack())
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data=cb.CallbackBackTo(to=f"lookAtSchedule").pack())
        ]
    ])


def keyboardGoTo(to):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="До розкладу",
            callback_data=cb.CallbackSelectSchedule(action="select", scheduleId=f"{to}").pack()
        )], [
        InlineKeyboardButton(text='До головного меню',
                             callback_data=cb.CallbackBackTo(to=f"main").pack())
    ]])


def keyboardToMenu():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='До головного меню',
                             callback_data=cb.CallbackBackTo(to=f"main").pack())
    ]])


def keyboardBack(to):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад',
                             callback_data=cb.CallbackBackTo(to=f"{to}").pack())
    ]])
