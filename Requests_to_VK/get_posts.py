import requests
from pprint import pprint

from work_with_text.correction_text_of_post import correction_text_of_post

domains = ['bu_truba_zovet', 'translom_pererabotka', 'truba24club', 'prodam_trubu', 'transfer1tube',
           'tryba_by_vosstanovlenay',
           'neewtruba', 'metalopt', 'nelikvid', '-116166768', '-17083336', '324213859']

owners_id = ['-115081032', '-203046727', '-28483397', '-89513171', '-152238835', '-66234848', '-116166768', '-17083336',
             '-80026197', '-40447148', '324213859', '530570695']


def get_post(owner_id_of_group: str, data_of_last_post: int, count_of_posts: int):
    token = '1c7c90141c7c90141c7c9014d11c0b69d811c7c1c7c90147cd753b4ab6c4777f6d7df33',
    api_version = '5.131'
    All_Posts = []
    offset = 0
    response = ''
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
    counter = 1
    for owner in owners_id:
        print("-----", owner, "----- номер: ", counter)
        pprint(get_post(owner, 1622522606, 10))   # 2021-06-01 07:43:26
        counter += 1
# pprint(get_post('165745216', 1622522606, 10))
