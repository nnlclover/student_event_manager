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
                text = f"Уважаемый {user['second_name']}! Через 5 минут у вас {message}."
                bot.sendSimpleMessage(user["chat_id"], message)
            except:
                print("error send")
        
#------------------------------------------------------------------------------
# time loop period 1 second
#------------------------------------------------------------------------------

def eclipse() -> None:
    current_datetime = datetime.datetime.now()

    print(f"[{current_datetime}] minute")
    
    now = datetime.datetime.now()
    new_time = now + datetime.timedelta(minutes=5)    
    formatted_time = new_time.strftime("%H:%M")
    
    print(formatted_time)    

    event = db.getEvent(formatted_time)
    print(event)

    if(event != None):
        make_malling(event)
    

#------------------------------------------------------------------------------
# polling timer
#------------------------------------------------------------------------------

def thread_worker() -> None:
    schedule.every(1).minutes.do(eclipse)

    while True:
        schedule.run_pending()
        time.sleep(1)

#------------------------------------------------------------------------------
# run second thread for timer
#------------------------------------------------------------------------------

def runTimedPolling() -> None:
    thread = threading.Thread(target=thread_worker)
    thread.start() 
    
