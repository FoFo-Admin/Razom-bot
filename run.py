import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.database.connect import initialDB

from app.handlers.admin.messages import router as router_message_admin
from app.handlers.admin.callbacks import router as router_callback_admin
from app.handlers.user.messages import router as router_message_user
from app.handlers.user.callbacks import router as router_callback_user

import app.scheduler as sch
from init import scheduler


load_dotenv()
bot = Bot(getenv('TOKEN'))


async def main() -> None:

    dp = Dispatcher()

    dp.include_router(router_message_admin)
    dp.include_router(router_callback_admin)
    dp.include_router(router_message_user)
    dp.include_router(router_callback_user)

    print("bot started")

    try:
        # tim = time.time()
        # for i in range(1, 10000):
        #    sqlite()
        # print(time.time() - tim)
        initialDB()
       # raise RuntimeError("Error")
        sch.addRemindJob(scheduler, bot)
        sch.addEventStartJob(scheduler, bot)
        sch.addEventEndJob(scheduler, bot)
        scheduler.start()
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
    finally:
        print("bot finished")


if __name__ == "__main__":
    asyncio.run(main())
