import random
from pprint import pprint
import sqlalchemy
import process_stages

engine = sqlalchemy.create_engine('postgresql://vkinder:123456@localhost:5432/vkinder')
connection = engine.connect()


def keep_user_desicion(user_id, match_id, decision):
    connection.execute(
        f"INSERT INTO desicionstatus (vkid_searching, vkid_match, status) "
        f"VALUES ('{user_id}', '{match_id}', '{decision}');")


def get_user_match(user_id, match_id):
    return connection.execute(
        f"SELECT status FROM desicionstatus "
        f"WHERE  vkid_searching = '{user_id}' AND vkid_match = '{match_id}' ;").fetchall()


def keep_user_vk_id(user_id):
    connection.execute(
        f"INSERT INTO user_information (vk_id, age, city_id, sex, relation, process_stage) "
        f"VALUES ('{user_id}', 0,0,0,0, '{process_stages.new_user_created}');")


def update_process_stage(user_id, process_stage):
    connection.execute(
        f"UPDATE user_information SET process_stage = '{process_stage}' WHERE vk_id = '{user_id}';")


def keep_user_age(user_id, age):
    connection.execute(
        f"UPDATE user_information SET age= {age} WHERE vk_id = '{user_id}';")


def keep_user_city_id(user_id, city_id):
    connection.execute(
        f"UPDATE user_information SET city_id={city_id} WHERE vk_id = '{user_id}';")


def keep_user_sex(user_id, sex):
    connection.execute(
        f"UPDATE user_information SET sex={sex} WHERE vk_id = '{user_id}';")


def keep_user_relation(user_id, relation):
    connection.execute(
        f"UPDATE user_information SET relation= {relation} WHERE vk_id = '{user_id}';")


def get_user_info(user_id):
    return connection.execute(
        f"SELECT age, city_id, sex, relation, process_stage FROM user_information "
        f"WHERE  vk_id = '{user_id}' limit 1;").fetchall()


def helper_get_age(user_db_info):
    return user_db_info[0]


def helper_get_city_id(user_db_info):
    return user_db_info[1]


def helper_get_sex(user_db_info):
    return user_db_info[2]


def helper_get_relation(user_db_info):
    return user_db_info[3]


def helper_get_process_stage(user_db_info):
    return user_db_info[4]
