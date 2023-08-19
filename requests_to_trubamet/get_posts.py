import psycopg2
import requests
from bs4 import BeautifulSoup

from DataBase.commands import is_advert_id_not_in_db, add_advert_id_to_db
from work_with_text.correction_text_of_post import correction_text_of_post


def get_posts_from_trubamet(db, cursor) -> list:
    adverts_list = []
    urls = ["https://trubamet.ru", "https://trubamet.ru/doska/show&pos=2&razdId=0"]
    for url in urls:
        response = requests.get(url)

        soup = BeautifulSoup(response.text)
        adverts_div = soup.find('div', {'id': 'doska'})
        adverts_on_page = adverts_div.find_all("div")

        for advert in adverts_on_page:
            advert_id = advert.get('id')
            table_row = advert.find("tr")
            if table_row is not None:
                text = table_row.text
                text = text.replace("Организация:", "\nОрганизация:")
                text = text.replace("Адрес:", "\nАдрес:")
                text = text.replace("Конт.лицо:", "\nКонт.лицо:")
                text = text.replace("Тел.:", "\nТел.:")
                if "Сайт" in text:
                    text = text[:text.find("Сайт:")]

                if is_advert_id_not_in_db(advert_id, cursor):
                    add_advert_id_to_db(advert_id, db, cursor)
                    advert_text = correction_text_of_post(text)
                    index = 0
                    while len(advert_text) != 0:
                        if len(advert_text) > 4096:
                            index = advert_text[index:4098].rfind(' ')
                            adverts_list.append(advert_text[:index])
                            advert_text = advert_text[index:]
                        else:
                            adverts_list.append(advert_text)
                            break

    return adverts_list


if __name__ == '__main__':
    db = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/vk_to_telegram")
    cursor = db.cursor()

    a = get_posts_from_trubamet(db, cursor)
    print(a)
