import logging
import sqlite3
import requests
import schedule
import time
import threading
import db
import asyncio

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)










#--------------------------------------------
#
#   telegram bot
#
#--------------------------------------------
CONTEXT_TOKEN = ""

# Send text to chat_id
def sendSimpleMessage(chat_id, text):
    r = requests.get(f'https://api.telegram.org/bot{CONTEXT_TOKEN}/sendmessage?chat_id={chat_id}&text={text}')
    if r.status_code != 200:
        body = r.json()
        if body['ok'] != True:
            sas = f'Error sendMessage: " {str(body)} chat_id="{chat_id}" text="{text}"'
            print(sas)
            with open("error.log", "a") as f:
                f.write(f"{sas}\r\n")
            return False
    return True

# handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if db.add_chat(update.message.chat_id):
        await update.message.reply_html(
            rf"Товарищ, вы подписались на рассылку событий!",
            reply_markup=ForceReply(selective=True),
        )
    else:
         await update.message.reply_html(
            rf"Товарищ, вы уже подписаны на рассылку событий!",
            reply_markup=ForceReply(selective=True),
         )


# handler /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if db.rm_chat(update.message.chat_id):
        await update.message.reply_html(
          rf"Товарищ, вы отписались от рассылки событий!",
            reply_markup=ForceReply(selective=True),
        )
    else:
        await update.message.reply_html(
          rf"Товарищ, вы не зарегистрированы чтобы выполнить данную команду",
            reply_markup=ForceReply(selective=True),
        )


# handler /today
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    events = db.getEvents()
    lines = "\n"
    for event in events:
        lines += f"{event['hour']}:{event['minute']} {event['message']}\n";

    await update.message.reply_html(
            rf"Товарищ, вот график работы на сегодня {lines}",
        reply_markup=ForceReply(selective=True),
    )
 

async def week_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    wtype = db.getWeekType()

    await update.message.reply_html(
            rf"Товарищ! Сейчас {wtype} профиль недели",
            reply_markup=ForceReply(selective=True),
            )


# handler /week
async def week_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    wtype = db.getWeekType()

    await update.message.reply_html(
            rf"Товарищ! Сейчас {wtype} профиль недели",
            reply_markup=ForceReply(selective=True),
            )

def bot_begin(token) -> None:

    global CONTEXT_TOKEN
    CONTEXT_TOKEN = token

    application = Application.builder().token(CONTEXT_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("week", week_type))

    # run polling 
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        # Обработка прерывания по Ctrl+C
        pass
