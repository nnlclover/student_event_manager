import datetime
import mysql.connector

host = "127.0.0.1"
port = 3306
db = "univer"

def gc():
    return mysql.connector.connect(
            host = host,
            port = port,
            user="root",
            password="rootNodeJS",
            database=db
    )
    
def getEventsToday():
    with gc() as conn:
        cur = conn.cursor()
        current_day = datetime.date.today().isoweekday()
        current_day = 1
        events = []
        cur.execute(f"SELECT message FROM events WHERE week = (SELECT type FROM week_type) AND day = {current_day}")
        res = cur.fetchall()
        for row in res:
            events.append({"time": 0.0, "message": row})

        cur.execute(f"SELECT time_start FROM times")
        res = cur.fetchall()

        event_len = len(events)
        for a in range(event_len):
            events[a]["time"] = res[a]

        print(events)
       

getEventsToday()
