from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

import app.database as db
import app.utils as utils


async def dayRemind(bot: Bot):
    print(f'Day remind at {datetime.now()}')
    events = db.getUserEventsByStatus()
    if events:
        for event in events:
            e = db.getEventById(event['eventId'])
            if datetime.now().strftime('%Y-%m-%d') == datetime.strptime(e[0]['datetime'][:-9], '%Y-%m-%d').strftime('%Y-%m-%d'):
                await utils.sendDaildyRemind(bot, event['eventId'], event['userId'])


async def eventStart(bot: Bot):
    #print("EventStartCheck")
    events = db.getEventsPublic()
    if events:
        for event in events:
            e = db.getUserEventsByEventId(event['id'])
            if datetime.now() >= datetime.strptime(event['datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=db.getTimeConfiguration('startEvent')[0]['timeInt']):
                db.updateEventStatus(event['id'], 'started')
                for i in e:
                    db.updateUserEventStatus(i['userId'], i['eventId'], 'asked')
                    await utils.sendIfUserOnEvent(bot, i['eventId'], i['userId'])


async def eventEnd(bot: Bot):
    events = db.getEventsStarted()
    if events:
        for event in events:
            if datetime.now() >= datetime.strptime(event['datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=db.getTimeConfiguration('endEvent')[0]['timeInt']):
                db.updateEventStatus(event['id'], 'ended')
                await utils.sendAdminStat(bot, event['id'])


def addRemindJob(scheduler: AsyncIOScheduler, bot: Bot):
    #scheduler.remove_job(job_id="dayRemind")
    scheduler.add_job(dayRemind, 'cron', hour=db.getTimeConfiguration('dayRemind')[0]['timeInt'], id='dayRemind', args=[bot])


def addEventStartJob(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.add_job(eventStart, 'interval', minutes=1, args=[bot])


def addEventEndJob(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.add_job(eventEnd, 'interval', minutes=1, args=[bot])


def editRemindJob(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.remove_job(job_id="dayRemind")
    scheduler.add_job(dayRemind, 'cron', hour=db.getTimeConfiguration('dayRemind')[0]['timeInt'], id='dayRemind', args=[bot])

