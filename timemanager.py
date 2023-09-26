import schedule
import threading 
import time
import db
import datetime
import bot

eventsl = []

#------------------------------------------------------------------------------
# send mail for all
#------------------------------------------------------------------------------

def make_malling(message) -> None:
    print(f"Send message: '{message}'")
    users = db.getUsers()

    for user in users:
        if user["state"] == 200 or user["state"] == 400: 
            try:
                print(user["second_name"])
                text = f"Уважаемый камрад! Через 5 минут {message}."
                bot.sendSimpleMessage(user["chat_id"], text)
            except:
                print("error send")
        
#------------------------------------------------------------------------------
# time loop period 1 second
#------------------------------------------------------------------------------

def eclipse() -> None:
    
    import datetime
    current_time = datetime.datetime.now()
    new_time = current_time + datetime.timedelta(minutes=5)
    formatted_time = new_time.strftime("%H:%M")
    print("Время через 5 минут:", formatted_time)

    event = db.getEvent(formatted_time)
    print(event)

    if(event != None):
        make_malling(event)
    

#------------------------------------------------------------------------------
# polling timer
#------------------------------------------------------------------------------

def thread_worker() -> None:
    schedule.every(1).minutes.do(eclipse)
    eclipse()

    while True:
        schedule.run_pending()
        time.sleep(1)

#------------------------------------------------------------------------------
# run second thread for timer
#------------------------------------------------------------------------------

def runTimedPolling() -> None:
    thread = threading.Thread(target=thread_worker)
    thread.start() 
    
