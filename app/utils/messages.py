import os
from datetime import datetime

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Bot

import app.keyboards as keyboards
import app.database as db

import app.utils.tables as table

# Обережно говнокод нижче
# Прошу вибачення перед тим кому прийдеться розбиратись. Я не прийлумав як краще можно це структурувати


# Start
def getUserStartText(qm):
    def lenToStr(events) -> str:
        value = len(events)
        str = f"Ви зареєстровані на {len(events)} "

        if all((value % 10 == 1, value % 100 != 11)):
            return str+'захід'+os.linesep +os.linesep +os.linesep
        elif all((2 <= value % 10 <= 4,
                  any((value % 100 < 10, value % 100 >= 20)))):
            return str+'заходи'+os.linesep +os.linesep +os.linesep
        return str+'заходів'+os.linesep +os.linesep +os.linesep

    events = db.getUserEventsByUserId(qm.from_user.id)
    return f"""{'Ви ще не зареєстровані ні на один захід'+os.linesep if not events
    else lenToStr(events)+"".join(f"{i+1}) {event['name']} о {event['datetime'][:-3]}"+os.linesep+os.linesep for i, event in enumerate(events))}

Для того, щоб переглянути, на які заходи можна зареєструватись оберіть розклад нижче 
"""


async def startMessage(message: Message):
    db.updateState(message.from_user.id, "main")
    await message.answer(text=getUserStartText(message), reply_markup=keyboards.keyboardUser())


async def startQuery(query: CallbackQuery):
    db.updateState(query.from_user.id, "main")
    await query.message.answer(text=getUserStartText(query), reply_markup=keyboards.keyboardUser())


async def startQueryEdit(query: CallbackQuery):
    db.updateState(query.from_user.id, "main")
    await query.message.edit_text(text=getUserStartText(query), reply_markup=keyboards.keyboardUser())


async def startAdminMessage(message: Message):
    db.updateState(message.from_user.id, "main")
    await message.answer(f"Час серверу: {datetime.now()}", reply_markup=keyboards.keyboardAdmin())


async def startAdminQuery(query: CallbackQuery):
    db.updateState(query.from_user.id, "main")
    await query.message.answer(f"Час серверу: {datetime.now()}", reply_markup=keyboards.keyboardAdmin())


async def startAdminQueryEdit(query: CallbackQuery):
    db.updateState(query.from_user.id, "main")
    await query.message.edit_text(f"Час серверу: {datetime.now()}", reply_markup=keyboards.keyboardAdmin())

# User Register

async def messageRegister(message: Message):
    await message.answer("Для того, щоб мати можливість користуватись ботом та реєструватись на заходи вам треба пройти невелике опитування.")


async def messageSetFIO(message: Message):
    await message.answer("Ваше прізвище, ім'я, по-батькові")


async def messageWrongFIO(message: Message):
    await message.answer("Некоректне ім'я")


async def messageSetEmail(message: Message):
    await message.answer("Ваша адреса електроної пошти")


async def messageNotUniqueEmail(message: Message):
    await message.answer("Ця адреса електроної пошти вже зареєстрована в системі")


async def messageWrongEmail(message: Message):
    await message.answer("Некоректна адреса електроної пошти")


async def messageSetTel(message: Message):
    await message.answer("Ваш мобільний номер телефону")


async def messageNotUniqueTel(message: Message):
    await message.answer("Цей мобільний номер телефону вже зареєстрований в системі")


async def messageWrongTel(message: Message):
    await message.answer("Некоректний мобільний номер телефону")


async def messageSetUserCategories(message: Message):
    await message.answer("""
        Чи є ви представником нижче приведених груп населення? 
        
        Можна обрати декілька варіантів. Після того, як оберете, нажміть кнопку "Готово"
    """, reply_markup=keyboards.keyboardUserCategories(message.from_user.id))


async def messageWrongUserCategories(messageorquery):
    await messageorquery.answer("Повинно бути обрано щонайменше одну категорію")


async def editSetUserCategories(query: CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=keyboards.keyboardUserCategories(query.from_user.id))


# User Events

async def messageScheduleUser(query: CallbackQuery, schedule):
    await query.message.answer_photo(photo=schedule[0]['image'],
                                     reply_markup=keyboards.keyboardEvents(query.from_user.id, schedule))


async def messageErrorEventDate(query: CallbackQuery):
    await query.message.answer("Дата реєстрації на захід пройшла")


async def messageErrorEventPeople(query: CallbackQuery):
    await query.message.answer("На захід вже зареєстрована максимальна кількість учасників")


async def messageConfirmRegistration(query: CallbackQuery, scheduleId, eventId):
    await query.message.answer("Підтвердіть реєстрацію", reply_markup=keyboards.keyboardConfirm(scheduleId, eventId))


async def messageConfirmUnregistration(query: CallbackQuery, scheduleId, eventId):
    await query.message.answer("Підтвердіть відміну реєстрації", reply_markup=keyboards.keyboardConfirm(scheduleId, eventId))



# Reminds

async def sendDaildyRemind(bot: Bot, eventId, userId):
    event = db.getEventById(eventId)
    await bot.send_message(userId, text=f"""Нагадуємо, ви зреєстровані сьогодні на захід "{event[0]['name']}", що відбудеться о {event[0]['datetime'][-9:-3]}""")


async def sendIfUserOnEvent(bot: Bot, eventId, userId):
    event = db.getEventById(eventId)
    await bot.send_message(userId, text=f"""Чи приймаєте ви участь у заході "{event[0]['name']}"?""", reply_markup=keyboards.keyboardIsOnEvent(event))


async def updateWasUserOnEvent(query: CallbackQuery):
    await query.message.edit_text(text=f"""Дякую за відповідь""", reply_markup=keyboards.keyboardToMenu())


async def updateErrorWasUserOnEvent(query: CallbackQuery):
    await query.message.edit_text(text=f"""Час голосування пройшов""", reply_markup=keyboards.keyboardToMenu())


async def sendAdminStat(bot: Bot, eventId):
        event = db.getEventById(eventId)
        allUserEvents = db.getUserEventsByEventId(eventId)
        usersYes = db.getUsersByUserEventsStatus(eventId, 'yes')
        usersNo = db.getUsersByUserEventsStatus(eventId, 'no')
        usersAsked = db.getUsersByUserEventsStatus(eventId, 'asked')

        src = f"""Статистика до заходу {event[0]['name']}
Всього було зареєстровано: {len(allUserEvents)}


Відмітило свою присутність: {len(usersYes)}
{'-' if not usersYes else "".join(f"{i+1}) {uy['FIO']} | {uy['email']}{os.linesep}" for i, uy in enumerate(usersYes))}

Відмітило свою відсутність: {len(usersNo)}
{'-' if not usersNo else "".join(f"{i+1}) {uy['FIO']} | {uy['email']}{os.linesep}" for i, uy in enumerate(usersNo))}

Не взяло участь у голосуванні: {len(usersAsked)}
{'-' if not usersAsked else "".join(f"{i+1}) {uy['FIO']} | {uy['email']}{os.linesep}" for i, uy in enumerate(usersAsked))}


Для більш конкретної інформації скачайте EXCEL документ"""
        admins = db.getAdmins()
        for admin in admins:
            await bot.send_message(admin['id'], text=src)


# Admin excel

async def messageUsersExcel(query: CallbackQuery):
    table.getUsersTable()
    file = FSInputFile("users.xlsx", filename="користувачі.xlsx")
    await query.message.answer_document(document=file)
    os.remove("users.xlsx")


async def messageScheduleExcel(query: CallbackQuery, scheduleId):
    schedule = db.getScheduleById(scheduleId)
    table.getScheduleTable(scheduleId)
    file = FSInputFile(f"{scheduleId}.xlsx", filename=f"{schedule[0]['name']}.xlsx")
    await query.message.answer_document(document=file)
    os.remove(f"{scheduleId}.xlsx")


# Admin Schedule

async def messageAddSchedule(query: CallbackQuery):
    await query.message.edit_text("Відправте фотографію розкладу разом з підписом як він буде називатись",
                         reply_markup=keyboards.keyboardBack('main'))


async def messageNewLetter(query: CallbackQuery):
    await query.message.edit_text("Напишіть повідомлення та/або відправте фото, відео, документ",
                         reply_markup=keyboards.keyboardBack('main'))


def timeText():
    dayRemind = db.getTimeConfiguration('dayRemind')
    endEvent = db.getTimeConfiguration('endEvent')
    startEvent = db.getTimeConfiguration('startEvent')
    return f"""Нагадування в день заходу о {dayRemind[0]['timeInt']} годині

    Повідомлення про присутність на заході через {startEvent[0]['timeInt']} хвилин після початку заходу

    Повідомлення з статистикою у адміністраторів через {endEvent[0]['timeInt']} хвилин після початку заходу
    """


async def messageEditTime(query: CallbackQuery):

    await query.message.edit_text(timeText(),
                         reply_markup=keyboards.keyboardTime())


async def messageEditTimeMessage(message: Message):
    await message.answer(timeText(),
                                  reply_markup=keyboards.keyboardTime())


async def messageDayRemind(query: CallbackQuery):
    await query.message.edit_text("Напишіть о котрій годині з 1 до 23 робити нагадування про захід",
                            reply_markup=keyboards.keyboardBack('editTime'))


async def messageStartEndEvent(query: CallbackQuery):
    await query.message.edit_text("Напишіть кількість хвилин від -120 до 120",
                            reply_markup=keyboards.keyboardBack('editTime'))




async def messageEditNameSchedule(query: CallbackQuery):
    await query.message.answer("Напишіть нову назву для розкладу",
                         reply_markup=keyboards.keyboardBack('lookAtSchedule'))


async def messageEditImageSchedule(query: CallbackQuery):
    await query.message.answer("Відправте нове фото для розкладу",
                         reply_markup=keyboards.keyboardBack('lookAtSchedule'))


async def messageDeleteSchedule(query: CallbackQuery):
    await query.message.answer("Щоб видалити розклад напишіть 'Видалити'",
                         reply_markup=keyboards.keyboardBack('lookAtSchedule'))


async def messageMakePublicSchedule(query: CallbackQuery):
    await query.message.answer("""Напишіть текст повідомлення з яким прийде розклад до кожного учасника.
    

Якщо бажаєте опублікувати розклад без повідомлення напишіть 'Опублікувати'""",
                         reply_markup=keyboards.keyboardBack('lookAtSchedule'))


async def messageMakePrivateSchedule(query: CallbackQuery):
    await query.message.answer("Якщо ви зробите розклад приватним, то всі реєстрації учасників на заходи будуть неактивні. Щоб підтвердити напишіть 'Видалити'",
                               reply_markup=keyboards.keyboardBack('lookAtSchedule'))


def scheduleText(qm, schedule):
    db.updateState(qm.from_user.id, f"lookAtSchedule:{schedule[0]['id']}")
    events = db.getEventsByScheduleId(schedule[0]['id'])

    src = f"""Назва розкладу: {schedule[0]['name']}
Статус: {'Опубліковано' if schedule[0]['status'] == 'public' else 'Не опубліковано'}

{'Ще нема створених заходів' if not events else ''.join(f"🔘{event['name']} / {event['datetime'][:-3]} / максимально {event['maxPeople']} учасників / зареєстровано {len(db.getUserEventsByEventId(event['id']))}{os.linesep}" for event in events)}

Для того редактувати/видалити захід нажміть на кнопку з його назвою"""

    return {'text': src, 'events': events}


async def messageSchedule(query: CallbackQuery, schedule):
    txt = scheduleText(query, schedule)

    await query.message.answer_photo(photo=schedule[0]['image'], caption=txt['text'], reply_markup=keyboards.keyboardSchedule(schedule, txt['events']))


async def messageScheduleMessage(message: Message, schedule):
    txt = scheduleText(message, schedule)

    await message.answer_photo(photo=schedule[0]['image'], caption=txt['text'], reply_markup=keyboards.keyboardSchedule(schedule, txt['events']))


async def messageAddEvent(query: CallbackQuery):
    await query.message.answer(text="""Напишіть відповідь в форматі:

Назва
Час в форматі "YYYY-MM-DD hh:mm"
Максимальну кількість учасників

Кожну строчку писати через перехід на нову строку
    """, reply_markup=keyboards.keyboardBack('lookAtSchedule'))


async def messageEditEvent(query: CallbackQuery, event):
    await query.message.answer(text=f"{event[0]['name']}{os.linesep}"
                                    f"{event[0]['datetime'][:-3]}{os.linesep}"
                                    f"{event[0]['maxPeople']}{os.linesep}",
                               reply_markup=keyboards.keyboardBack('lookAtSchedule'))


# Events Admin

async def messageWrongEventPeople(message: Message):
    await message.answer("Некоректна максимальна кількість учасників")


async def messageWrongEventParts(message: Message):
    await message.answer("Некоректна кількість строк")


async def messageWrongEventDate(message: Message):
    await message.answer("Некоректна дата")

# Errors / Default

async def defaultMessage(message: Message):
    await message.answer("Нема такого варіанту відповіді")


async def defaultMessageQuery(query: CallbackQuery):
    await query.answer("Нема такого варіанту відповіді")


async def messageError(message: Message):
    await message.answer("Нема такого варіанту відповіді")


async def messageErrorQuery(query: CallbackQuery):
    await query.answer("Нема такого варіанту відповіді")
