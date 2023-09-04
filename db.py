import sqlite3 
import datetime

db_name = 'database.db'

def setDbPath(path) -> None:
    global db_name
    db_name = path

def getCon():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return {conn, cursor}

def updateNumeric() -> None:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE temp_table SET id = id - (SELECT MIN(id) - 1 FROM temp_table)")
    


def createNewTables() -> None:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute('''CREATE TABLE chats(id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER UNIQUE, reg_time INTEGER);''')
        conn.commit()
    except sqlite3.OperationalError as e:
        pass

    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            week_type INTEGER NOT NULL,
                            day INTEGER NOT NULL,
                            hour INTEGER NOT NULL,
                            minute INTEGER NOT NULL,
                            message TEXT NOT NULL
                        );''')
        conn.commit()
    except sqlite3.OperationalError as e:
        pass
    try:
        cursor.execute('''CREATE TABLE week_type(type INTEGER PRIMARY KEY);''')
        conn.commit()
    except sqlite3.OperationalError as e:
        pass
    conn.close()


def getChats():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chats")

        return cursor.fetchall()


def getEvents():
    day_num = getWeekType()
    current_day = datetime.date.today().isoweekday()

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM events WHERE day={current_day} AND week_type={day_num}')
    events = cursor.fetchall()
    
    events_book = []
    for event in events:
        events_book.append({"hour":event[3],"minute":event[4], "message":event[5]})
    conn.close()
    return events_book


def getWeekType():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM week_type')
    table = cursor.fetchall()
    week_type = -1
    if len(table) > 0:
        week_type = table[0][0]
    conn.close()
    return week_type


def add_chat(chat_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO chats (chat_id) VALUES (?)', (chat_id,))
            conn.commit()
            updateNumeric()
            return True
        except(sqlite3.IntegrityError):
            updateNumeric()
            return False


def rm_chat(chat_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM chats WHERE chat_id = ?', (chat_id,))
        existing_row = cursor.fetchone()
    
        if existing_row:
            cursor.execute('DELETE FROM chats WHERE chat_id = ?', (chat_id,))
            conn.commit()
            print(f"Chat ID {chat_id} успешно удален.")
            updateNumeric()
            return True
        else:
            print(f"Chat ID {chat_id} не найден в базе данных.")
            updateNumeric()
            return False

 
