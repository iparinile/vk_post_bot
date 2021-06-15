import psycopg2
import telebot
from telebot.types import InputMediaPhoto
import threading

from DataBase.commands import add_user, add_post, get_last_post_date, is_user_already_recorded, get_all_users
from Requests_to_VK.get_posts import get_post, edit_post_to_correct

bot = telebot.TeleBot('1742929878:AAExqh7JcRATPAFr7iVc5pv9OE8B8eebDYQ')
db = psycopg2.connect(dbname='data', user='postgres', password='1', host='localhost')
cursor = db.cursor()

owners_id = {'-115081032': 'bu_truba_zovet', '-203046727': 'translom_pererabotka', '-28483397': 'truba24club',
             '-89513171': 'prodam_trubu', '-152238835': 'transfer1tube', '-66234848': 'tryba_by_vosstanovlenay',
             '-116166768': 'public116166768', '-17083336': 'club17083336', '-80026197': 'metalopt',
             '-40447148': 'nelikvid', '324213859': 'id324213859', '530570695': 'neewtruba',
             '-161503615': 'club161503615', '-177235715': 'truba.bu_ot159_1420'}


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

    for owner in owners_id.items():
        last_post_date = get_last_post_date(owner[0], cursor)
        users = get_all_users(cursor)
        if len(users) > 0:
            posts = get_post(owner_id_of_group=owner, data_of_last_post=last_post_date, count_of_posts=10)
            for post in posts:
                add_post(
                    group_domain=owner[0],
                    post_id=post['post_id'],
                    post_date=post['date'],
                    cursor=cursor,
                    db=db
                )

                post_text = edit_post_to_correct(post)['text']
                images_array = post['image_url']

                for user_id in users:

                    if len(images_array) == 1:
                        if (post_text[0] == '') and (len(post_text) == 1):
                            bot.send_photo(chat_id=user_id, photo=images_array[0])
                        else:
                            bot.send_photo(chat_id=user_id, photo=images_array[0], caption=post_text[0])
                            if len(post_text) > 1:
                                for text in post_text[1:]:
                                    if text != '':
                                        bot.send_message(chat_id=user_id, text=text)

                    elif len(images_array) > 1:
                        if (post_text[0] == '') and (len(post_text) == 1):
                            media = []
                            for image in images_array:
                                media.append(InputMediaPhoto(image))
                            bot.send_media_group(chat_id=user_id, media=media)
                        else:
                            media = [InputMediaPhoto(images_array[0], caption=post_text[0])]
                            for image in images_array[1:]:
                                media.append(InputMediaPhoto(image))
                            bot.send_media_group(chat_id=user_id, media=media)
                            if len(post_text) > 1:
                                for text in post_text[1:]:
                                    if text != '':
                                        bot.send_message(chat_id=user_id, text=text)
                    elif len(images_array) == 0:
                        for text in post_text:
                            if text != '':
                                bot.send_message(chat_id=user_id, text=text)


search_new_posts()

bot.polling(none_stop=True)
