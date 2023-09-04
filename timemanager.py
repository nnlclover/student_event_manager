import schedule
import threading 
import time
import db
import datetime
import bot

eventsl = []

def make_malling(message) -> None:
    print(f"Send message: '{message}'")
    chats = db.getChats()
    for chat in chats:
        try:
            bot.sendSimpleMessage(chat[1], message)
        except:
            print("error send")
        

def eclipse() -> None:
    current_datetime = datetime.datetime.now()

    print(f"[{current_datetime}] minute")
    events = db.getEvents()
    
    current_datetime = datetime.datetime.now()
    
    hour = current_datetime.hour
    minute = current_datetime.minute

    for event in events:
        print(event)
        if event['hour'] == hour and event['minute'] == minute:
            make_malling(event['message'])


def thread_worker() -> None:
    schedule.every(1).minutes.do(eclipse)

    while True:
        schedule.run_pending()
        time.sleep(1)

def runTimedPolling() -> None:
    thread = threading.Thread(target=thread_worker)
    thread.start() 
    