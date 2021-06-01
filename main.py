import sqlite3
import telebot
import threading

from DataBase.commands import add_user, add_post, get_last_post_date
from Requests_to_VK.get_posts import get_post

bot = telebot.TeleBot('1742929878:AAExqh7JcRATPAFr7iVc5pv9OE8B8eebDYQ')
db = sqlite3.connect('DataBase/data.sqlite', check_same_thread=False)
cursor = db.cursor()

owners_id = ['-115081032', '-203046727', '-28483397', '-89513171', '-152238835', '-66234848', '-116166768', '-17083336',
             '-80026197', '-40447148', '324213859', '530570695']


@bot.message_handler(commands=["start"])
def start(message):
    try:
        add_user(message.chat.id, cursor, db)
    except ValueError:
        print('Что-то пошло не так')
    bot.send_message(message.chat.id, 'Привет! Я записал тебя в свой список. Теперь я буду твоим рабом')


def search_new_posts():
    threading.Timer(10.0, search_new_posts).start()  # Перезапуск через 10 секунд

    for owner in owners_id:
        last_post_date = get_last_post_date(owner, cursor)
        posts = get_post(owner_id_of_group=owner, data_of_last_post=last_post_date, count_of_posts=10)
        print(owner)
        for post in posts:
            add_post(
                group_domain=owner,
                post_id=post['post_id'],
                post_text=post['text'],
                post_date=post['date'],
                cursor=cursor,
                db=db
            )

            bot.send_message(813672369, post['text'])


search_new_posts()

bot.polling()
