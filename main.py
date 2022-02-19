import choosing_match
import data_base
import getting_searching_info
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
import calling_vk_api
import process_stages

long_poll = VkLongPoll(calling_vk_api.vk_group)


def write_msg(user_id, message):
    calling_vk_api.vk_group.method(
        'messages.send',
        {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), }
    )


def write_msg_with_attachment(user_id, message, attachment):
    calling_vk_api.vk_group.method(
        'messages.send',
        {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'attachment': attachment}
    )


def validate_user(user_id):
    users_data = data_base.get_user_info(user_id)
    if len(users_data) > 0:
        write_msg(user_id, f"Кажется вы у нас уже были...")
        validate_user_params(user_id)
    else:
        data_base.keep_user_vk_id(user_id)
        validate_user_params(user_id)
    return None


def validate_user_params(user_id):
    user_vk_info = calling_vk_api.getting_user_info(user_id)
    actual_db_info = data_base.get_user_info(user_id)[0]
    if data_base.helper_get_age(actual_db_info) == 0:
        age = getting_searching_info.getting_age(user_vk_info)
        if age is None:
            write_msg(user_id, f"Введите ваш возраст: ")
            data_base.update_process_stage(user_id, process_stages.waiting_age)
            return
        else:
            data_base.keep_user_age(user_id, age)

    if data_base.helper_get_city_id(actual_db_info) == 0:
        city_name = getting_searching_info.getting_city(user_vk_info)
        if city_name is None:
            write_msg(user_id, f"Введите ваш город: ")
            data_base.update_process_stage(user_id, process_stages.waiting_city_name)
            return
        else:
            city_id = calling_vk_api.get_city_id(city_name)
            data_base.keep_user_city_id(user_id, city_id)

    if data_base.helper_get_sex(actual_db_info) == 0:
        sex = getting_searching_info.getting_sex(user_vk_info)
        if sex is None:
            write_msg(user_id, f''' Введите ваш пол
            # 1 — женский;
            # 2 — мужской;
            # ''')
            data_base.update_process_stage(user_id, process_stages.waiting_sex)
            return
        else:
            data_base.keep_user_sex(user_id, sex)

    if data_base.helper_get_relation(actual_db_info) == 0:
        relation = getting_searching_info.getting_relation(user_vk_info)
        if relation is None:
            write_msg(user_id, f'''Введите ваше семейное положениe:
            1 — не женат/не замужем;
            2 — есть друг/есть подруга;
            3 — помолвлен/помолвлена;
            4 — женат/замужем;
            5 — всё сложно;
            6 — в активном поиске;
            7 — влюблён/влюблена;
            8 — в гражданском браке;
            ''')
            data_base.update_process_stage(user_id, process_stages.waiting_relation)
            return
        else:
            data_base.keep_user_relation(user_id, relation)
    data_base.update_process_stage(user_id, process_stages.complete)
    write_msg(user_id, f"Вы готовы начать подбор,  Чтобы начать подбор пар напиши 'Найди мне пару'")


def handle_message(request, user_id):
    user_db_infos = data_base.get_user_info(user_id)
    if len(user_db_infos) == 1:
        if data_base.helper_get_process_stage(user_db_infos[0]) == process_stages.waiting_age:
            data_base.keep_user_age(user_id, int(request))
            validate_user_params(user_id)
            return
        if data_base.helper_get_process_stage(user_db_infos[0]) == process_stages.waiting_city_name:
            city_id = calling_vk_api.get_city_id(request)
            data_base.keep_user_city_id(user_id, city_id)
            validate_user_params(user_id)
            return
        if data_base.helper_get_process_stage(user_db_infos[0]) == process_stages.waiting_sex:
            sex_user = getting_searching_info.getting_sex_from_user(int(request))
            data_base.keep_user_sex(user_id, sex_user)
            validate_user_params(user_id)
            return
        if data_base.helper_get_process_stage(user_db_infos[0]) == process_stages.waiting_relation:
            data_base.keep_user_relation(user_id, request)
            validate_user_params(user_id)
            return

    if request == "привет":
        validate_user(user_id)
    elif request == 'найди мне пару':
        show_next_match(user_id)
    elif request == '1':
        match_id = data_base.get_offered_match(user_id)
        choosing_match.made_desicion(user_id, match_id, 1)
        show_next_match(user_id)
    elif request == '0':
        match_id = data_base.get_offered_match(user_id)
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


def show_next_match(user_id):
    age, city_id, sex, relation, stage = data_base.get_user_info(user_id)[0]
    offset = data_base.get_user_search_offset(user_id)

    match_infos = calling_vk_api.getting_matches(age, city_id, sex, relation, offset)
    local_counter = find_next_not_closed(0, match_infos, user_id)
    while local_counter >= len(match_infos):
        offset += calling_vk_api.matches_per_page
        data_base.update_user_offset(user_id, offset)
        match_infos = calling_vk_api.getting_matches(age, city_id, sex, relation, offset)
        local_counter = find_next_not_closed(0, match_infos, user_id)

    match_id = match_infos[local_counter]['id']
    data_base.update_user_offered_match(user_id, match_id)
    photo_info = calling_vk_api.getting_photo_info(match_id)['items']
    link, three_popular_photo = choosing_match.get_user_info(photo_info, match_id)
    write_msg(user_id, f"Я нашел для вас пару {link}")
    photos_urls = ','.join(three_popular_photo)
    write_msg_with_attachment(user_id, f"Оцените фотографии", photos_urls)
    write_msg(user_id, "Нажмите\n1 - если вам понравилась пара\n0 - чтобы посмотреть следующего человека")
    return None


def find_next_not_closed(current_counter, match_infos, user_id):
    result = current_counter + 1
    while result < len(match_infos) and not can_show(match_infos[result], user_id):
        result += 1
    return result


def can_show(match_info, user_id):
    return len(data_base.get_user_match(user_id, match_info['id'])) == 0 and not match_info['is_closed']


start_polling()
