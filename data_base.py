import sqlalchemy

import process_stages
from user_storage import UserStorage, StorageError, UserInfo

engine = sqlalchemy.create_engine('postgresql://vkinder:123456@localhost:5432/vkinder')
connection = engine.connect()


class UserStorageDb(UserStorage):
    def get_user_info(self, user_id):
        try:
            users = connection.execute(
                f"SELECT age, city_id, sex, relation, process_stage FROM user_information "
                f"WHERE  vk_id = '{user_id}' limit 1;").fetchall()
            if len(users) == 0:
                return None
            else:
                user_row = users[0]
                return UserInfo(user_row[0], user_row[1], user_row[2], user_row[3], user_row[4])
        except Exception:
            raise StorageError()

    def keep_user_decision(self, user_id, match_id, decision):
        try:
            connection.execute(
                f"INSERT INTO desicionstatus (vkid_searching, vkid_match, status) "
                f"VALUES ('{user_id}', '{match_id}', '{decision}');")
            return True
        except Exception:
            return False

    def get_user_match(self, user_id, match_id):
        try:
            return connection.execute(
                f"SELECT status FROM desicionstatus "
                f"WHERE  vkid_searching = '{user_id}' AND vkid_match = '{match_id}' ;").fetchall()
        except Exception:
            raise StorageError()

    def keep_user_vk_id(self, user_id):
        try:
            connection.execute(
                f"INSERT INTO user_information (vk_id, age, city_id, sex, relation, process_stage) "
                f"VALUES ('{user_id}', 0, 0, 0, 0, '{process_stages.new_user_created}');")
        except Exception:
            pass

    def update_process_stage(self, user_id, process_stage):
        try:
            connection.execute(
                f"UPDATE user_information SET process_stage = '{process_stage}' WHERE vk_id = '{user_id}';")
        except Exception:
            pass

    def update_user_offset(self, user_id, offset):
        try:
            connection.execute(
                f"UPDATE user_information SET search_offset = '{offset}' WHERE vk_id = '{user_id}';")
        except Exception:
            pass

    def update_user_offered_match(self, user_id, offered_vk_id):
        try:
            connection.execute(
                f"UPDATE user_information SET offered_vk_id = '{offered_vk_id}' WHERE vk_id = '{user_id}';")
        except Exception:
            pass

    def keep_user_age(self, user_id, age):
        try:
            connection.execute(
                f"UPDATE user_information SET age= {age} WHERE vk_id = '{user_id}';")
        except Exception:
            pass

    def keep_user_city_id(self, user_id, city_id):
        try:
            connection.execute(
                f"UPDATE user_information SET city_id={city_id} WHERE vk_id = '{user_id}';")
        except Exception:
            pass

    def keep_user_sex(self, user_id, sex):
        try:
            connection.execute(
                f"UPDATE user_information SET sex={sex} WHERE vk_id = '{user_id}';")
        except Exception:
            pass

    def keep_user_relation(self, user_id, relation):
        try:
            connection.execute(
                f"UPDATE user_information SET relation= {relation} WHERE vk_id = '{user_id}';")
        except Exception:
            pass

    def get_user_search_offset(self, user_id):
        try:
            return connection.execute(
                f"SELECT search_offset FROM user_information "
                f"WHERE  vk_id = '{user_id}' limit 1;").fetchall()[0][0]
        except Exception:
            return 0

    def get_offered_match(self, user_id):
        try:
            return connection.execute(
                f"SELECT offered_vk_id FROM user_information "
                f"WHERE  vk_id = '{user_id}' limit 1;").fetchall()[0][0]
        except Exception:
            return None
