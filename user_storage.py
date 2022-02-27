from dataclasses import dataclass


@dataclass
class UserInfo:
    age: int
    city_id: int
    sex: int
    relation: int
    process_stage: str


class UserStorage:
    def get_user_info(self, user_id):
        # вернет инфо о юзере - UserInfo
        # вернет None если не нашли пользователя
        # в случае ошибки выбросим исключение CantGetUserInfo
        pass

    def keep_user_decision(self, user_id, match_id, decision):
        pass

    def get_user_match(self, user_id, match_id):
        pass

    def keep_user_vk_id(self, user_id):
        pass

    def update_process_stage(self, user_id, process_stage):
        pass

    def update_user_offset(self, user_id, offset):
        pass

    def update_user_offered_match(self, user_id, offered_vk_id):
        pass

    def keep_user_age(self, user_id, age):
        pass

    def keep_user_city_id(self, user_id, city_id):
        pass

    def keep_user_sex(self, user_id, sex):
        pass

    def keep_user_relation(self, user_id, relation):
        pass

    def get_user_search_offset(self, user_id):
        pass

    def get_offered_match(self, user_id):
        pass


class CantGetUserInfo(Exception):
    pass