from app.database.connect import put


def updateState(id: int, newState: str):
    sql = """
        UPDATE users SET state = :newState 
        WHERE id = :id
    """
    return put(sql, {'newState': newState, 'id':id})


def updateRole(id: int, newRole: str):
    sql = """
        UPDATE users SET role = :newRole 
        WHERE id = :id
    """
    return put(sql, {'newRole': newRole, 'id':id})


def updateFIO(id: int, newFIO: str):
    sql = """
        UPDATE users SET FIO = :newFIO 
        WHERE id = :id
    """
    return put(sql, {'newFIO': newFIO, 'id': id})


def updateEmail(id: int, newEmail: str):
    sql = """
        UPDATE users SET email = :newEmail 
        WHERE id = :id
    """
    return put(sql, {'newEmail': newEmail, 'id': id})


def updateTel(id: int, newTel: str):
    sql = """
        UPDATE users SET tel = :newTel 
        WHERE id = :id
    """
    return put(sql, {'newTel': newTel, 'id': id})


def updateScheduleName(id: int, name: str):
    sql = """
        UPDATE schedules
        SET name = :name
        WHERE id = :id
    """
    return put(sql, {'name': name, 'id': id})


def updateScheduleImage(id: int, image: str):
    sql = """
        UPDATE schedules
        SET image = :image
        WHERE id = :id
    """
    return put(sql, {'image': image, 'id': id})


def updateScheduleStatus(id: int, status: str):
    sql = """
        UPDATE schedules
        SET status = :status
        WHERE id = :id
    """
    return put(sql, {'status': status, 'id': id})


def updateEvent(id: int, name: str, maxPeople: int, datetime: str):
    sql = """
        UPDATE events
        SET name = :name, maxPeople = :maxPeople, datetime = datetime(:datetime), status = 'ongoing'
        WHERE id = :id
    """
    return put(sql, {'name': name, 'id': id, 'maxPeople': maxPeople, 'datetime': datetime})


def updateEventStatus(id: int, status: str):
    sql = """
        UPDATE events
        SET status = :status
        WHERE id = :id
    """
    return put(sql, {'id': id, 'status': status})


def updateUserEventStatus(userId: int, eventId: int, status: str):
    sql = """
        UPDATE user_events
        SET status = :status 
        WHERE userId = :userId AND eventId = :eventId
    """
    return put(sql, {'userId': userId, 'eventId': eventId, 'status': status})


def updateTime(timeName: str, timeInt: int):
    sql = """
        UPDATE time_configuration
        SET timeInt = :timeInt 
        WHERE name = :timeName
    """
    return put(sql, {'timeName': timeName, 'timeInt': timeInt})
