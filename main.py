import sqlite3
import telebot
import threading

bot = telebot.TeleBot('1742929878:AAExqh7JcRATPAFr7iVc5pv9OE8B8eebDYQ')
db = sqlite3.connect('data.sqlite', check_same_thread=False)
cursor = db.cursor()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Как тебя зовут?')
    print(message.chat.id)


def async_function():
    threading.Timer(5.0, async_function).start()  # Перезапуск через 5 секунд
    print("Hello, world!")
    bot.send_message(813672369, 'Я пишу это каждые 5 секунд')


async_function()

bot.polling()
