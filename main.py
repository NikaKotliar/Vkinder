from random import randrange
import json
import vk_api
from pprint import pprint
from datetime import date
import datetime
import calling_vk_api
import choosing_match

user_ids = 'alex_kryptonite'
match_counter = -1
user_info = calling_vk_api.getting_user_info(user_ids)
match_infos = calling_vk_api.getting_matches(user_info)


def find_next_not_closed(current_counter, infos):
    result = current_counter + 1
    while infos[result]['is_closed']:
        result += 1
    return result


while input('Print exit to exit ') != 'exit':
    match_counter = find_next_not_closed(match_counter, match_infos)
    match_id = match_infos[match_counter]['id']
    photo_info = calling_vk_api.getting_photo_info(match_id)['items']
    tree_popular_photo = choosing_match.get_user_info(photo_info, match_id)
    choosing_match.made_desicion(user_info['id'], match_id)

#
# def write_msg(user_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
#
#
# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#
#         if event.to_me:
#             request = event.text
#
#             if request == "привет":
#                 write_msg(event.user_id, f"Хай, {event.user_id}")
#             elif request == "пока":
#                 write_msg(event.user_id, "Пока((")
#             else:
#                 write_msg(event.user_id, "Не поняла вашего ответа...")
