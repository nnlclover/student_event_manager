import db
import bot
import timemanager
import threading

def main() -> None:
    TOKEN = "6440862149:AAGHpeE9Y9bWRQ6URNrF7n5JbW0q3xi0QN8"
    db.setDbPath("database.db")

    db.createNewTables()

    timemanager.runTimedPolling()
    
    bot.bot_begin(TOKEN)
    

if __name__ == "__main__":
    main()
