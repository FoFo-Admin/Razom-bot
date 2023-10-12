import typing

from app.database.connect import put


def insertUser(id: int):
    sql = """
        INSERT INTO users(id, state) VALUES (:id, 'setFIO')
    """
    return put(sql, {'id': id})


def insertUserCategory(userId: int, socialId: int):
    sql = """
        INSERT INTO user_categories(userId, socialId) VALUES (:userId, :socialId)
    """
    return put(sql, {'userId': userId, 'socialId': socialId})


def insertSchedule(name: str, image):
    sql = """
        INSERT INTO schedules(name, image, status) VALUES (:name, :image, 'private')
    """
    return put(sql, {'name': name, 'image': image})


def insertScheduleEvent(name: str, maxPeople: int, datetime: str, ScheduleId: int):
    sql = """
        INSERT INTO events(name, maxPeople, datetime, status, ScheduleId) 
        VALUES (:name, :maxPeople, datetime(:datetime), 'ongoing', :ScheduleId)
    """
    return put(sql, {'name': name, 'maxPeople': maxPeople, 'datetime': datetime, 'ScheduleId': ScheduleId})


def insertUserEvent(userId: int, eventId: int):
    sql = """
        INSERT INTO user_events(userId, eventId, status)
        VALUES (:userId, :eventId, 'registered')
    """
    return put(sql, {'userId': userId, 'eventId': eventId})
