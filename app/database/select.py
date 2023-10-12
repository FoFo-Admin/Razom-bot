from app.database.connect import get


def getUser(id: int):
    sql = """
        SELECT * FROM users WHERE id = :id
    """
    return get(sql, {'id': id})


def getUsers():
    sql = """
        SELECT * FROM users WHERE role = 'user'
    """
    return get(sql)


def getAdmins():
    sql = """
        SELECT * FROM users WHERE role = 'admin'
    """
    return get(sql)


def getUserCategories(id: int):
    sql = """
        SELECT * FROM user_categories WHERE userId = :id
    """
    return get(sql, {'id': id})


def getCategories():
    sql = """
        SELECT * FROM social_categories
    """
    return get(sql)


def getCategoryById(id: int):
    sql = """
        SELECT * FROM social_categories WHERE id = :id
    """
    return get(sql, {'id': id})


def getAllSchedules():
    sql = """
            SELECT * FROM schedules
        """
    return get(sql)


def getPublicSchedules():
    sql = """
            SELECT * FROM schedules
WHERE status = 'public'
        """
    return get(sql)


def getScheduleById(scheduleId: int):
    sql = """
            SELECT * FROM schedules WHERE id = :scheduleId
        """
    return get(sql, {'scheduleId': scheduleId})


def getEventsByScheduleId(scheduleId: int):
    sql = """
            SELECT * FROM events WHERE ScheduleId = :scheduleId
            ORDER BY datetime ASC
        """
    return get(sql, {'scheduleId': scheduleId})


def getEventById(eventId: int):
    sql = """
            SELECT * FROM events WHERE id = :eventId
        """
    return get(sql, {'eventId': eventId})


def getEventsPublic():
    sql = """  
SELECT * FROM events
INNER JOIN schedules ON events.ScheduleId = schedules.id
WHERE events.status = 'ongoing' AND schedules.status = 'public';
            """
    return get(sql)


def getEventsStarted():
    sql = """  
SELECT * FROM events
INNER JOIN schedules ON events.ScheduleId = schedules.id
WHERE events.status = 'started' AND schedules.status = 'public';
            """
    return get(sql)


def getUserEventsByUserId(userId: int):
    sql = """
        SELECT * FROM user_events 
INNER JOIN events ON events.id = user_events.eventId
INNER JOIN schedules ON schedules.id = events.ScheduleId
WHERE user_events.userId = :userId AND events.status = 'ongoing' AND schedules.status = 'public'
    """
    return get(sql, {'userId': userId})


def getUsersByUserEventsStatus(eventId: int, userEventStatus: str):
    sql = """
        SELECT * FROM users
INNER JOIN user_events ON user_events.userId = users.id
INNER JOIN events on user_events.eventId = events.id
WHERE events.id = :eventId AND user_events.status = :userEventStatus
    """
    return get(sql, {'eventId': eventId, 'userEventStatus': userEventStatus})


def getUniqueUsersByScheduleId(scheduleId: int):
    sql = """
    SELECT DISTINCT users.id, users.FIO, users.email FROM users
INNER JOIN user_events ON user_events.userId = users.id
INNER JOIN events on user_events.eventId = events.id
INNER JOIN schedules ON schedules.id = events.ScheduleId
WHERE schedules.id = :scheduleId;
    """
    return get(sql, {'scheduleId': scheduleId})


def getUserEventsByStatus():
    sql = """
        SELECT * FROM user_events 
INNER JOIN events ON events.id = user_events.eventId
INNER JOIN schedules ON schedules.id = events.ScheduleId
WHERE events.status = 'ongoing' AND schedules.status = 'public'
    """
    return get(sql)


def getUserEventsByEventId(eventId: int):
    sql = """
    SELECT * FROM user_events
WHERE eventId = :eventId
    """
    return get(sql, {'eventId': eventId})


def getUserEventsByEventIdAndUserId(eventId: int, userId: int):
    sql = """
    SELECT * FROM user_events
WHERE eventId = :eventId AND userId = :userId
    """
    return get(sql, {'eventId': eventId, 'userId': userId})


def getTimeConfiguration(name: str):
    sql = """
    SELECT * FROM time_configuration
WHERE name = :name
    """
    return get(sql, {'name': name})



