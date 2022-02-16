from pprint import pprint
import calling_vk_api
import data_base


appropriate_photos_types = ['z', 'y', 'r', 'x']


def select_size(sizes):
    for size in sizes:
        if size['type'] in appropriate_photos_types:
            return size
    return None


def extract_photos(photo_infos):
    users_photo_dict = {}
    for item in photo_infos:
        preferable_size = select_size(item['sizes'])
        if preferable_size is None:
            continue
        url = preferable_size['url']
        sravnenie = item['likes']['count'] + item['comments']['count']
        users_photo_dict[url] = sravnenie
    return users_photo_dict


def get_user_info(photo_dict, id):
    photo_info = extract_photos(photo_dict)
    person_link = 'https://vk.com/id' + str(id)
    print('Ссылка: ' + person_link)
    list_photos = list(photo_info.items())
    list_photos.sort(key=lambda i: i[1], reverse=True)
    for i in list_photos[:3]:
        print(i[0], ':', i[1])


def made_desicion(user_id, match_id):
    user_decision = input('Введите 1 если Да и 0 если Нет ')
    data_base.keep_user_desicion(user_id, match_id, user_decision)
