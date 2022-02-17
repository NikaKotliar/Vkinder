from random import randrange
import json
import vk_api
from pprint import pprint
from datetime import date
import datetime
import calling_vk_api
import choosing_match
import vk_poling
import getting_searching_info
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
import calling_vk_api

age = None
city_id = None
sex = None
relation = None


long_poll = VkLongPoll(calling_vk_api.vk_group)


def write_msg(user_id, message):
    calling_vk_api.vk_group.method(
        'messages.send',
        {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), }
    )


def handle_message(request, user_id):
    if request == "привет":
        info = calling_vk_api.getting_user_info(user_id)
        if age is None or city_id is None or sex is None or relation is None:
            on_new_user(info)
        write_msg(user_id, f"Привет, {info['first_name']} Чтобы начать подбор пар напиши 'Найди мне пару'")
    elif request == 'найди мне пару':
        show_next_match(user_id)
    elif request == '1':
        choosing_match.made_desicion(user_id, match_id, 1)
        show_next_match(user_id)
    elif request == '0':
        choosing_match.made_desicion(user_id, match_id, 0)
        show_next_match(user_id)

    elif request == "пока":
        write_msg(user_id, "Пока((")
    else:
        write_msg(user_id, "Не поняла вашего ответа...")


def start_polling():
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower().strip()
                print(f"Message new: {request} from {event.user_id}")
                handle_message(request, event.user_id)


match_id = 1
match_counter = -1


def current_user_info(user_id):
    user_info = calling_vk_api.getting_user_info(user_id)


def show_next_match(user_id):
    global match_counter
    match_infos = calling_vk_api.getting_matches(city_id,sex,relation,age)
    match_counter = find_next_not_closed(match_counter, match_infos)
    global match_id
    match_id = match_infos[match_counter]['id']
    photo_info = calling_vk_api.getting_photo_info(match_id)['items']
    link, three_popular_photo = choosing_match.get_user_info(photo_info, match_id)
    write_msg(user_id, f"Я нашел для вас пару {link}")
    write_msg(user_id, f"Оцените фотографии {' , '.join(three_popular_photo)}")
    write_msg(user_id, "Нажмите 1 чтобы выбрать эту пару или 0 чтобы посмотреть следующего человека")
    return None


def find_next_not_closed(current_counter, infos):
    result = current_counter + 1
    while infos[result]['is_closed']:
        result += 1
    return result


def on_new_user(user_info):
    global age
    global city_id
    global sex
    global relation
    age = getting_searching_info.getting_age(user_info)
    city_id = calling_vk_api.get_city_id(getting_searching_info.getting_city(user_info))
    sex = getting_searching_info.getting_sex(user_info)
    relation = getting_searching_info.getting_relation(user_info)


start_polling()
