from app.database.connect import put


def deleteUserCategoriesNotCategory(userId: int, socialId: int):
    sql = """
        DELETE FROM user_categories WHERE userId = :userid AND socialId IS NOT :socialId
    """
    return put(sql, {'userid': userId, 'socialId': socialId})


def deleteUserCategoriesCategory(userId: int, socialId: int):
    sql = """
        DELETE FROM user_categories 
        WHERE userId = :userid AND socialId = 5
    """
    return put(sql, {'userid': userId, 'socialId': socialId})


def deleteUserCategoriesById(userId: int, socialId: int):
    sql = """
        DELETE FROM user_categories 
        WHERE userId = :userid AND socialId = :socialId
    """
    return put(sql, {'userid': userId, 'socialId': socialId})


def deleteScheduleById(id: int):
    sql = """
        DELETE FROM schedules 
        WHERE id = :id
    """
    return put(sql, {'id': id})


def deleteUserEvent(userId: int, eventId: int):
    sql = """
        DELETE FROM user_events
        WHERE userId = :userId AND eventId = :eventId
    """
    return put(sql, {'userId': userId, 'eventId': eventId})


def deleteUserEventsByEventId(eventId: int):
    sql = """
        DELETE FROM user_events 
        WHERE eventId = :eventId
    """
    return put(sql, {'eventId': eventId})


def deleteUserEventsByScheduleId(id: int):
    sql = """
        DELETE FROM user_events 
        WHERE eventId in (SELECT id FROM events
        WHERE scheduleId = :id)
    """
    return put(sql, {'id': id})


def deleteEventById(id: int):
    sql = """
        DELETE FROM events 
        WHERE id = :id
    """
    return put(sql, {'id': id})


def deleteEventByScheduleId(id: int):
    sql = """
        DELETE FROM events 
        WHERE ScheduleId = :id
    """
    return put(sql, {'id': id})
