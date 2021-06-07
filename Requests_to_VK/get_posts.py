import requests
import telebot

from work_with_text.correction_text_of_post import correction_text_of_post

owners_id = ['-115081032', '-203046727', '-28483397', '-89513171', '-152238835', '-66234848', '-116166768', '-17083336',
             '-80026197', '-40447148', '324213859', '530570695']


def get_post(owner_id_of_group: str, data_of_last_post: int, count_of_posts: int):
    token = '1c7c90141c7c90141c7c9014d11c0b69d811c7c1c7c90147cd753b4ab6c4777f6d7df33',
    api_version = '5.131'
    All_Posts = []
    offset = 0
    while offset < count_of_posts:
        try:
            response = requests.get('https://api.vk.com/method/wall.get',
                                    params={
                                        'access_token': token,
                                        'owner_id': owner_id_of_group,
                                        'v': api_version,
                                        'count': 1,
                                        'offset': offset
                                    }
                                    )
            All_Posts.extend(response.json()['response']['items'])
        except ValueError:
            pass
        offset += 1
    new_posts = []
    post_text = ' '
    for post in All_Posts:
        image_url = []
        if post['date'] > data_of_last_post:
            try:
                for image in post['attachments']:
                    if image['type']:
                        image_url.append(image['photo']['sizes'][-1]['url'])
            except KeyError:
                pass
            try:
                post_text = correction_text_of_post(post['text'])
            except ValueError:
                pass
            if post_text != ' ' and image_url != []:
                new_posts.append({
                    'post_id': post['id'],
                    'date': post['date'],
                    'text': post_text,
                    'image_irl': image_url
                })
    return new_posts


if __name__ == '__main__':
    bot = telebot.TeleBot('1742929878:AAExqh7JcRATPAFr7iVc5pv9OE8B8eebDYQ')
    posts = get_post('-28483397', 1, 25)
    for post in posts:
        if post['text'] != '':
            text = post['text']
            if len(text) > 4096:
                for x in range(0, len(text), 4096):
                    bot.send_message(813672369, text[x:x + 4096])
            else:
                bot.send_message(813672369, text)
