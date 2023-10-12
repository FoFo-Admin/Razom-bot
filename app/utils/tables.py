import xlsxwriter

import app.database as db

def getUsersTable():
    users = db.getUsers()

    wb = xlsxwriter.Workbook('users.xlsx')
    ws = wb.add_worksheet()

    ws.set_column(1, 4, 30)

    head = wb.add_format({'bold': True, 'bg_color': 'gray', 'border': 1})
    border = wb.add_format({'border': 1})

    ws.write(1, 1, 'ПІБ', head)
    ws.write(1, 2, 'email', head)
    ws.write(1, 3, 'Номер телефону', head)
    ws.write(1, 4, 'Соціальні категорії', head)

    row = 2

    for user in users:
        user_catergories = db.getUserCategories(user['id'])
        txt = "".join(f"{db.getCategoryById(uc['socialId'])[0]['name']}"+",  " for uc in user_catergories)

        ws.write(row, 1, user['FIO'], border)
        ws.write(row, 2, user['email'], border)
        ws.write(row, 3, user['tel'], border)
        ws.write(row, 4, txt, border)

        row += 1
    wb.close()


def getScheduleTable(scheduleId):
    users = db.getUniqueUsersByScheduleId(scheduleId)
    events = db.getEventsByScheduleId(scheduleId)

    wb = xlsxwriter.Workbook(f'{scheduleId}.xlsx')
    ws = wb.add_worksheet()

    ws.set_column(1, len(events)+2, 30)

    head = wb.add_format({'bold': True, 'bg_color': 'gray', 'border': 1})
    border = wb.add_format({'border': 1})

    yes = wb.add_format({'border': 1, 'bg_color': 'green'})
    no = wb.add_format({'border': 1, 'bg_color': 'red'})
    answer = wb.add_format({'border': 1, 'bg_color': 'yellow'})
    register = wb.add_format({'border': 1, 'bg_color': 'black'})

    ws.write(1, 1, 'ПІБ', head)
    ws.write(1, 2, 'email', head)
    column = 3
    for event in events:
        ws.write(1, column, event['name'], head)
        column += 1

    row = 2

    for user in users:
        column = 3
        ws.write(row, 1, user['FIO'], border)
        ws.write(row, 2, user['email'], border)
        for event in events:
            user_event = db.getUserEventsByEventIdAndUserId(event['id'], user['id'])
            if not user_event:
                ws.write(row, column, '', register)
            else:
                if user_event[0]['status'] == 'yes':
                    ws.write(row, column, '', yes)
                elif user_event[0]['status'] == 'no':
                    ws.write(row, column, '', no)
                else:
                    ws.write(row, column, '', answer)
            column += 1
        row += 1
    wb.close()
