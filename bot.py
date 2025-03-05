import time
import random, string
import telebot
import sqlite3


API_TOKEN = 'PLACE BOT TOKEN HERE'  # GET BOT TOKEN FROM BOTFAHTER
CONTENT_CHANNEL_ID = "PLACE CONTENT CHANNEL ID HERE" # GENERATE A PRIVATE CHANNEL FOR THIS, POST SOMETHING, THEN COLPY LINK ADDRESS, IS SOMETHING LIKE : https://t.me/c/1234567/2 , CONTENT_CHANNEL_ID is 1234567
BOT_LINK = "PLACE BOT LINK HERE" # LINK TO BOT IS SOMETHING LIKE: https://t.me/XYZ_bot
DELETE_TIMOUT = 15 # IN SECONDS. BOT DELETES CONTENT AFTER THIS TIME.

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text.startswith('/start'):
        content_id = message.text[7:]
        content_id.strip()
        
        try:
            cursor = conn.execute("SELECT CONTENT_ID from CONTENTS WHERE BANNER_ID=?", (content_id,))
            content = list(cursor)[-1]
            content_id = content[0]
            bot.copy_message(chat_id=message.chat.id, from_chat_id=f'-100{CONTENT_CHANNEL_ID}', message_id=content_id)
            bot.reply_to(message, "Copy message, it will be deleted after 15 seconds")
            time.sleep(DELETE_TIMOUT)
            bot.delete_message(message.chat.id, message.message_id + 1)
            bot.delete_message(message.chat.id, message.message_id + 2)
        except Exception as e:
            bot.reply_to(message, "content does not exit")
            print(e)

    else:
        bot.reply_to(message, "start again another way ")

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.startswith(f'https://t.me/c/{CONTENT_CHANNEL_ID}'):
        try:
            text = message.text
            content_id = text.split('/')[-1]
            banner_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            cur = conn.cursor()
            cur.execute("INSERT INTO CONTENTS (BANNER_ID,CONTENT_ID) VALUES (?, ?)", (banner_id,content_id));
            conn.commit()
            link = f"{BOT_LINK}?start={banner_id}"
            bot.send_message(message.chat.id,'use this link:')
            bot.send_message(message.chat.id, link)
        except Excetion as e:
            print(e)
            bot.send_message(message.chat.id, "error happened:")
            bot.send_message(message.chat.id, e)
    
if __name__ == "__main__":
         bot = telebot.TeleBot(API_TOKEN)
         conn = sqlite3.connect('bot.db', check_same_thread=False)
         conn.execute('''CREATE TABLE IF NOT EXISTS CONTENTS 
             (ID INTEGER PRIMARY KEY     ,
             BANNER_ID           TEXT    NOT NULL,
             CONTENT_ID            TEXT     NOT NULL);''')
         bot.polling()
