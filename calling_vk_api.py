import vk_api
import json
import getting_searching_info

def get_tokens(path_to_token_group, path_to_token_user):
    with open(path_to_token_group, 'r') as file_object:
        token_group = file_object.read().strip()
    with open(path_to_token_user, 'r') as file_object:
        token_user = file_object.read().strip()
    return token_group, token_user


token_group, token_user = get_tokens('VK_Access.txt', 'vk_token.txt')
vk_group = vk_api.VkApi(token=token_group)
vk_user = vk_api.VkApi(token=token_user)


def getting_user_info(user_ids):
    user_info = vk_group.method('users.get', {'user_ids': user_ids,
                                              'fields': 'first_name, last_name, bdate,  photo_50, city_name, home_town, relation,sex'})[
        0]
    with open('users_info.json', 'w', encoding='utf-8') as f:
        json.dump(user_info, f, ensure_ascii=False)

    return user_info


def get_city_id(city_name):
    city_name = vk_user.method('database.getCities', {'country_id': 1, 'q': city_name, 'need_all': 0, 'count': 1})
    return city_name['items'][0]['id']


def getting_matches(user_info):
    age = getting_searching_info.getting_age(user_info)
    city_id = get_city_id(getting_searching_info.getting_city(user_info))
    sex = getting_searching_info.getting_sex(user_info)
    relation = getting_searching_info.getting_relation(user_info)
    match_offset = 0
    offset = match_offset

    print(age, city_id, sex, relation)

    match_info = vk_user.method('users.search',
                                {'city': city_id, 'sex': sex, 'status': relation, 'age_from': age, 'age_to': age,
                                 'is_closed': False, 'offset': offset,
                                 'has_photo': 1,
                                 'fields': 'id, first_name, last_name, city_name'})

    with open('match_info.json', 'w', encoding='utf-8') as f:
        json.dump(match_info, f, ensure_ascii=False)
    return match_info['items']


def getting_photo_info(user_id):
    photo_info = vk_user.method('photos.get', {'owner_id': user_id, 'album_id': "profile", 'extended': 1, })
    with open('photo_info.json', 'w', encoding='utf-8') as f:
        json.dump(photo_info, f, ensure_ascii=False)
    return photo_info
