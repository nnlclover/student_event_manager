import logging
import requests
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

#------------------------------------------------------------------------------
# Send text to chat_id
#------------------------------------------------------------------------------

def sendSimpleMessage(chat_id, text):
    r = requests.get(f"""https://api.telegram.org/bot{CONTEXT_TOKEN}/sendmessage
    ?chat_id={chat_id}&text={text}""")
    if r.status_code != 200:
        body = r.json()
        if body['ok'] != True:
            sas = f"""Error sendMessage: \" {str(body)} chat_id=\"{chat_id}\" 
            text="{text}"""
            print(sas)
            db.logging(f"sendSimpleMessage('{text}') failed! {sas}", chat_id)
            return False
    db.logging(f"sendSimpleMessage('{text}')", chat_id)
    return True


#------------------------------------------------------------------------------
# handler /start
#------------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if db.add_chat(update.message.chat_id):
        await update.message.reply_html(
            rf"Товарищ, вы подписались на рассылку событий!",
        )
        db.logging(f"/start Товарищ, вы подписались на рассылку событий!",
                  update.message.chat_id)
    else:
         await update.message.reply_html(
            rf"Товарищ, вы уже подписаны на рассылку событий!",
         )
         db.logging(f"/start Товарищ, вы уже подписаны на рассылку событий!", 
                   update.message.chat_id)

#------------------------------------------------------------------------------
# handler /stop
#------------------------------------------------------------------------------

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if db.rm_chat(update.message.chat_id):
        await update.message.reply_html(
          rf"Товарищ, вы отписались от рассылки событий!",
            reply_markup=ForceReply(selective=True),
        )
        db.logging(f"/stop Товарищ, вы отписались от рассылки событий!",
                   update.message.chat_id)
    else:
        await update.message.reply_html(
          rf"Товарищ, вы не зарегистрированы чтобы выполнить данную команду",
            reply_markup=ForceReply(selective=True),
        )
        db.logging(f"""/stop Товарищ, вы не зарегистрированы чтобы 
        выполнить данную команду""", update.message.chat_id)

#------------------------------------------------------------------------------
# Log all messages 
#------------------------------------------------------------------------------

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.logging(update.message.text, update.message.chat_id)

#------------------------------------------------------------------------------
# Sending a custom message from the admin 
#------------------------------------------------------------------------------

async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.logging(update.message.text, update.message.chat_id)

    users = db.getUsers()
    
    admin = None
    for user in users:
        if user["state"] == 400 and user["chat_id"] == update.message.chat_id:
            admin = user

    if admin == None:
        db.logging("/msg unauthorized user", update.message.chat_id)
        return

    usss = []
    for user in users:
        if user["state"] == 200:
            sendSimpleMessage(user["chat_id"], " ".join(context.args))
            usss.append(user["second_name"])

    await update.message.reply_html(
          rf"Сообщения были отправлены {usss}",
        )
    db.logging(f"/msg Сообщения были откправлены {usss}",
              update.message.chat_id)

#------------------------------------------------------------------------------
# begin function
#------------------------------------------------------------------------------

def bot_begin(token) -> None:

    global CONTEXT_TOKEN
    CONTEXT_TOKEN = token

    application = Application.builder().token(CONTEXT_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("msg", msg))
    #application.add_handler(CommandHandler("today", today))
    #application.add_handler(CommandHandler("week", week_type))
    #application.add_handler(CommandHandler("reg", reg))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # run polling 
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        # Обработка прерывания по Ctrl+C
        pass




""""

# handler /today
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return 
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



async def reg():
    users = db.getUsers()
    for user in users:
        if(user["state"] == 0 and user["can"] == 0):
            bot.SendSempleMessage(user["chat_id"], "Dear comrade, in order to prevent data leakage, I ask you to complete a simple registration. Write the command “/reg Ivanov Ivan, 01/01/2005, your city” and enter your data in this command. After you provide your data, the bot admin will check you (this will take approximately 24 hours). If you provide invalid data, you will be blocked.")
    pass


"""