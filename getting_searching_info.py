from datetime import date
import datetime


search_info = {'age': None, 'sex': None, 'city_name': None, 'relation': None}

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def getting_age(user_info):
    if 'bdate' in user_info.keys():
        if user_info['bdate'].count('.') != 2:
            age = str(input('Введите возраст: '))
        else:
            age = calculate_age(datetime.datetime.strptime(user_info['bdate'], "%d.%m.%Y"))
    else:
        age = str(input('Введите возраст: '))
    return age

def getting_city(user_info):
    if 'city_name' in user_info.keys():
       city_name = user_info['city_name']
    else:
        city_name = str(input('Введите ваш город: '))
    return city_name

def getting_sex(user_info):
    if 'sex' in user_info.keys():
        if user_info['sex'] == 0:
            sex = str(input(''' Введите ваш пол
            1 — женский;
            2 — мужской;
            '''))
        elif user_info['sex'] == 1:
            sex = 2
        elif user_info['sex'] == 2:
            sex = 1
    return sex

def getting_relation(user_info):
    if 'relation' in user_info.keys():
        if user_info['relation'] == 0:
            relation = str(input('''Введите ваше семейное положениe: 
               1 — не женат/не замужем;
               2 — есть друг/есть подруга;
               3 — помолвлен/помолвлена;
               4 — женат/замужем;
               5 — всё сложно;
               6 — в активном поиске;
               7 — влюблён/влюблена;
               8 — в гражданском браке;
               '''))
        else:
            relation = user_info['relation']
    else:
        relation = str(input('''Введите ваше семейное положениe: 
    1 — не женат/не замужем;
    2 — есть друг/есть подруга;
    3 — помолвлен/помолвлена;
    4 — женат/замужем;
    5 — всё сложно;
    6 — в активном поиске;
    7 — влюблён/влюблена;
    8 — в гражданском браке;
    '''))
    return relation
#