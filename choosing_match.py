import data_base


def extract_photos(photo_infos):
    users_photo_dict = {}
    for item in photo_infos:
        sravnenie = item['likes']['count'] + item['comments']['count']
        users_photo_dict[f"photo{item['owner_id']}_{item['id']}"] = sravnenie
    return users_photo_dict


def photo_as_dict(photo_info):
    return {'link': photo_info[0], 'likes': photo_info[1]}


def get_user_info(photo_dict, id):
    photo_info = extract_photos(photo_dict)
    link = 'https://vk.com/id' + str(id)
    list_photos = list(photo_info.items())
    list_photos.sort(key=lambda i: i[1], reverse=True)
    photos = [i[0] for i in list_photos[:3]]
    return link, photos


def made_desicion(user_id, match_id, decision):
    data_base.keep_user_desicion(user_id, match_id, decision)
