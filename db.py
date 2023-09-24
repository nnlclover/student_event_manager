import sqlite3 
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
        current_day = 1#datetime.date.today().isoweekday()
        events = []
        cur.execute(f"SELECT message FROM events WHERE week = (SELECT type FROM week_type) AND day = {current_day};")
        res = cur.fetchall()

        for row in res:
            events.append({"message": row})

        cur.execute(f"SELECT time_start FROM times")
        res = cur.fetchall()

        event_len = len(events)
        for a in range(event_len):
            events[a]["time"] = res[a]

        return events



def getUsers():
    users = []
    try:
        db_connection = gc()

        cursor = db_connection.cursor()
        sql_query = "SELECT * FROM users"
        cursor.execute(sql_query)
        result = cursor.fetchall()
    
        for row in result:
            obj = {
                "id": row[0],
                "chat_id": row[1],
                "name": row[2],
                "second_name": row[3],
                "state": row[4],
                "date": row[5],
                "city": row[6],
            }
            users.append(obj)
        db_connection.close()
        return users
    except e:
        print(e)


# for update
#cursor.execute("UPDATE temp_table SET id = id - (SELECT MIN(id) - 1 FROM temp_table)")

# get only one event for setted time
def getEvent(time):
    current_day = datetime.date.today().isoweekday()
    try: 
        conn = gc()
        cursor = conn.cursor()
        cursor.execute(f"SELECT message FROM events WHERE week = (SELECT type FROM week_type) AND list_num = (SELECT number FROM times WHERE time_start = '{time}') AND day = {current_day};")
        event = cursor.fetchone()
        conn.close()
    except e:
        print(e) 
    return event


def getWeekType():
    conn = gc()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM week_type')
    table = cursor.fetchall()
    week_type = -1
    if len(table) > 0:
        week_type = table[0][0]
    conn.close()
    return week_type

def logging(message, chat_id):
    with gc() as conn:
        cursor = conn.cursor()
        # Используйте параметризованный запрос с %s для вставки значений
        query = "INSERT INTO logging(message, chat_id) VALUES(%s, %s)"
        values = (message, chat_id)
        cursor.execute(query, values)
        conn.commit()


def add_chat(chat_id):
    with gc() as conn:
        cursor = conn.cursor()
    
        cursor.execute(f'SELECT * FROM users WHERE chat_id = {chat_id} LIMIT 1')

        res = cursor.fetchone()
        if(not res):
            cursor.execute(f'INSERT INTO users (chat_id) VALUES({chat_id})')
            conn.commit()
            return True
        else:
            return False


def rm_chat(chat_id):
    with gc() as conn:
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM users WHERE chat_id = {chat_id} LIMIT 1')
        existing_row = cursor.fetchone()
    
        if existing_row:
            cursor.execute(f'DELETE FROM users WHERE chat_id = {chat_id}')
            conn.commit()
            print(f"Chat ID {chat_id} успешно удален.")
            return True
        else:
            print(f"Chat ID {chat_id} не найден в базе данных.")
            return False

 
