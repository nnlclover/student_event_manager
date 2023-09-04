import db
import bot
import timemanager
import threading
import configparser

def main() -> None:
    TOKEN = ""

    config = configparser.ConfigParser()
    config.read('token')
    TOKEN = config['Telegram']['token']



    if len(TOKEN) == 0:
        print("not found token file")
        exit()

    db.setDbPath("database.db")

    db.createNewTables()

    timemanager.runTimedPolling()
    
    bot.bot_begin(TOKEN)
    

if __name__ == "__main__":
    main()
