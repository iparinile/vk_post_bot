import psycopg2
import telebot
from telebot.types import InputMediaPhoto
import threading

from DataBase.commands import add_user, add_post, get_last_post_date, is_user_already_recorded
from Requests_to_VK.get_posts import get_post, edit_post_to_correct

bot = telebot.TeleBot('1742929878:AAExqh7JcRATPAFr7iVc5pv9OE8B8eebDYQ')
db = psycopg2.connect(dbname='data', user='postgres', password='1', host='localhost')
cursor = db.cursor()

owners_id = ['-115081032', '-203046727', '-28483397', '-89513171', '-152238835', '-66234848', '-116166768', '-17083336',
             '-80026197', '-40447148', '324213859', '530570695']


@bot.message_handler(commands=["start"])
def start(message):
    try:
        if is_user_already_recorded(message.chat.id, cursor):
            bot.send_message(message.chat.id, 'Я уже запомнил тебя')
        else:
            add_user(message.chat.id, cursor, db)
            bot.send_message(message.chat.id, 'Привет! Я записал тебя в свой список. Теперь я буду твоим рабом')
    except psycopg2.Error:
        print('прилетела ошибка')
        cursor.execute('END TRANSACTION;')


def search_new_posts():
    threading.Timer(1 * 60.0, search_new_posts).start()  # Перезапуск через 10 секунд

    for owner in owners_id:
        last_post_date = get_last_post_date(owner, cursor)
        posts = get_post(owner_id_of_group=owner, data_of_last_post=last_post_date, count_of_posts=10)
        print(owner)
        for post in posts:
            add_post(
                group_domain=owner,
                post_id=post['post_id'],
                post_date=post['date'],
                cursor=cursor,
                db=db
            )

            post_text = edit_post_to_correct(post)['text']
            images_array = post['image_url']

            if len(images_array) == 1:
                if (post_text[0] == '') and (len(post_text) == 1):
                    bot.send_photo(chat_id=813672369, photo=images_array[0])
                else:
                    bot.send_photo(chat_id=813672369, photo=images_array[0], caption=post_text[0])
                    if len(post_text) > 1:
                        for text in post_text[1:]:
                            if text != '':
                                bot.send_message(chat_id=813672369, text=text)

            elif len(images_array) > 1:
                if (post_text[0] == '') and (len(post_text) == 1):
                    media = []
                    for image in images_array:
                        media.append(InputMediaPhoto(image))
                    bot.send_media_group(chat_id=813672369, media=media)
                else:
                    media = [InputMediaPhoto(images_array[0], caption=post_text[0])]
                    for image in images_array:
                        media.append(InputMediaPhoto(image))
                    bot.send_media_group(chat_id=813672369, media=media)
                    if len(post_text) > 1:
                        for text in post_text[1:]:
                            if text != '':
                                bot.send_message(chat_id=813672369, text=text)
            elif len(images_array) == 0:
                for text in post_text:
                    if text != '':
                        bot.send_message(chat_id=813672369, text=text)


search_new_posts()

bot.polling(none_stop=True)
