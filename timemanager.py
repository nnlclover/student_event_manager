import schedule
import threading 
import time
import db
import datetime
import bot

eventsl = []

def make_malling(message):
    print(f"Send message: '{message}'")
    chats = db.getChats()
    for chat in chats:
        try:
            bot.sendSimpleMessage(chat[1], message)
        except:
            print("error send")
        

def eclipse():
    
    current_datetime = datetime.datetime.now()

    print(f"[{current_datetime}]minute")
    events = db.getEvents()
    
    current_datetime = datetime.datetime.now()
    
    hour = current_datetime.hour
    minute = current_datetime.minute

    for event in events:
        print(event)
        if event['hour'] == hour and event['minute'] == minute:
            make_malling(event['message'])



def timer():
    schedule.every(1).minutes.do(eclipse)

    while True:
        # Проверяем и выполняем запланированные задачи
        schedule.run_pending()
        time.sleep(1)

def runTimedPolling():
    thread = threading.Thread(target=timer)
    thread.start()  # Запуск потока
    