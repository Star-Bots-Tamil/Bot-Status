from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from aiohttp import web
from route import web_server
import asyncio
import datetime
import pytz
import os

app = Client(
    name = "botstatus",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    session_string = os.environ["SESSION_STRING"]
)
TIME_ZONE = os.environ["TIME_ZONE"]
BOT_LIST = [i.strip() for i in os.environ.get("BOT_LIST").split(' ')]
CHANNEL_OR_GROUP_ID = int(os.environ["CHANNEL_OR_GROUP_ID"])
MESSAGE_ID = int(os.environ["MESSAGE_ID"])
BOT_ADMIN_IDS = [int(i.strip()) for i in os.environ.get("BOT_ADMIN_IDS").split(' ')]
WEBHOOK = bool(os.environ.get("WEBHOOK", True))

async def main_teletips():
    async with app:
            while True:
                print("Checking...")
                xxx_teletips = f"📈 **Real Time Bot Status**"
                for bot in BOT_LIST:
                    bot_entity = await app.get_users(bot)
                    bot_name = bot_entity.first_name
                    try:
                        yyy_teletips = await app.send_message(bot, "/start")
                        aaa = yyy_teletips.id
                        await asyncio.sleep(10)
                        zzz_teletips = app.get_chat_history(bot, limit = 1)
                        async for ccc in zzz_teletips:
                            bbb = ccc.id
                        if aaa == bbb:
                            xxx_teletips += f"\n\n🤖 **[{bot_name}](https://t.me/{bot})\n        └ Down** ❌"
                            for bot_admin_id in BOT_ADMIN_IDS:
                                try:
                                    await app.send_message(int(bot_admin_id), f"🚨 **Alert!! [{bot_name}](https://t.me/{bot}) is Down** ❌", disable_web_page_preview=True)
                                except Exception:
                                    pass
                            await app.read_chat_history(bot)
                        else:
                            xxx_teletips += f"\n\n🤖 **[{bot_name}](https://t.me/{bot})\n        └ Alive** ✅"
                            await app.read_chat_history(bot)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)            
                time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
                last_update = time.strftime(f"%d %b %Y at %I:%M %p")
                xxx_teletips += f"**\n\n👨🏻‍💻 --Developers :---\n         • [Karthik](https://t.me/U_Karthik)\n         • [Dhinesh](https://t.me/Mersal_Dhinesh)\n\n✓ Last Checked on :- {last_update} ({TIME_ZONE})\n\n♻️ Refreshes Automatically\n\n© Managed By :- [DP Botz](https://t.me/DP_BOTZ)**"
                await app.edit_message_text(int(CHANNEL_OR_GROUP_ID), MESSAGE_ID, xxx_teletips, disable_web_page_preview=True)
                print(f"Last Checked on :- {last_update}")                
                await asyncio.sleep(3600)

async def init():
    if WEBHOOK:
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()       
        await web.TCPSite(app_runner, "0.0.0.0", 8080).start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main_teletips())
    loop.create_task(init())
    loop.run_forever()
