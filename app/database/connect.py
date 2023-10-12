import sqlite3 as sq


def sqlite():
    db = sq.connect('database.sql')
    cur = db.cursor()
    db.close()


def initialDB():
    db = sq.connect('database.sql')
    cur = db.cursor()


    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users(
	id INTEGER PRIMARY KEY,
    role TEXT(0,50),
    state TEXT(0,50),
    FIO TEXT(3,100), 
    email TEXT(3,50),
    tel TEXT(3,20),
    
    CONSTRAINT users_email_unique UNIQUE(email),
    CONSTRAINT users_tel_unique UNIQUE(tel)
    );

    CREATE TABLE IF NOT EXISTS social_categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
	    name TEXT(0,200) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS user_categories(
	    userId INTEGER NOT NULL,
        socialId INTEGER NOT NULL,
    
        CONSTRAINT userId_categories_pk PRIMARY KEY(userId, socailId),
        CONSTRAINT userId_fk FOREIGN KEY(userId) REFERENCES users(id),
        CONSTRAINT socailId_fk FOREIGN KEY(socailId) REFERENCES social_categories(id)
    );
    
    CREATE TABLE IF NOT EXISTS schedules(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT(0,200) NOT NULL,
        image TEXT NOT NULL,
        status TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        maxPeople INTEGER NOT NULL,
        datetime TEXT NOT NULL,
        status TEXT NOT NULL,
        ScheduleId INTEGER NOT NULL,
        
        CONSTRAINT ScheduleId_fk FOREIGN KEY(ScheduleId) REFERENCES Schedules(id)
    );
    
    CREATE TABLE IF NOT EXISTS user_events(
	    userId INTEGER NOT NULL,
        eventId INTEGER NOT NULL,
        status TEXT NOT NULL,
    
        CONSTRAINT userId_categories_pk PRIMARY KEY(userId, eventId),
        CONSTRAINT userId_fk FOREIGN KEY(userId) REFERENCES users(id),
        CONSTRAINT eventId_fk FOREIGN KEY(eventId) REFERENCES events(id)
    );
    
    CREATE TABLE IF NOT EXISTS time_configuration(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT(0,200) NOT NULL,
        timeString TEXT,
        timeInt INTEGER
    );
    """)
    db.commit()
    db.close()


def put(sql, data={}):
    result = True
    try:
        db = sq.connect('database.sql')
        db.row_factory = sq.Row
        cur = db.cursor()

        cur.execute(sql, data)
        db.commit()
    except Exception as e:
        if db:
            db.rollback()
        result = False
        print(e)
    finally:
        if db:
            db.close()
        return result


def get(sql, data={}):
    result = True
    try:
        db = sq.connect('database.sql')
        db.row_factory = sq.Row
        cur = db.cursor()

        cur.execute(sql, data)
        result = cur.fetchall()
    except Exception as e:
        if db:
            db.rollback()
        result = False
        print(e)
    finally:
        if db:
            db.close()
        return result
