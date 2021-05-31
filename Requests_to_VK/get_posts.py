import requests
from pprint import pprint

from work_with_text.correction_text_of_post import correction_text_of_post

domains = ['bu_truba_zovet', 'translom_pererabotka', 'prodam_trubu', 'transfer1tube', 'tryba_by_vosstanovlenay',
           'public116166768', 'club17083336', 'metalopt', 'nelikvid', 'onamazov2014', 'id324213859', 'neewtruba']


def get_post(domain_of_group: str, data_of_last_post: int, count_of_posts: int) -> list:
    token = '1c7c90141c7c90141c7c9014d11c0b69d811c7c1c7c90147cd753b4ab6c4777f6d7df33',
    api_version = '5.131'
    All_Posts = []
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': api_version,
                                'domain': domain_of_group,
                                'count': count_of_posts
                            }
                            )
    pprint(response.json())
    All_Posts.extend(response.json()['response']['items'])
    new_posts = []
    image_url = []
    for post in All_Posts:
        if post['date'] > data_of_last_post:
            try:
                for image in post['attachments']:
                    if image['type']:
                        image_url.append(image['photo']['sizes'][-1]['url'])
            except KeyError:
                pass
                # print(e)
            new_posts.append({
                'post_id': post['id'],
                'date': post['date'],
                'text': correction_text_of_post(post['text']),
                'image_irl': image_url
            })
    return new_posts


if __name__ == '__main__':
    pprint(get_post(domains[0], 1622448000, 50))
