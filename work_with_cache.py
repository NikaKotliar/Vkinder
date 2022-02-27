import dataclasses

import process_stages
from data_base import UserStorageDb
from user_storage import UserStorage, UserInfo


class CacheWork(UserStorage):
    def __init__(self):
        self.database = UserStorageDb()
        self.users_cache = {}
        self.offset_cache = {}
        self.offered_matches_cache = {}

    def get_user_info(self, user_id):
        if user_id in self.users_cache.keys():
            return self.users_cache[user_id]
        else:
            user_info = self.database.get_user_info(user_id)
            if user_info is not None:
                self.users_cache[user_id] = user_info
                return user_info
            return None

    def keep_user_decision(self, user_id, match_id, decision):
        return self.database.keep_user_decision(user_id, match_id, decision)

    def get_user_match(self, user_id, match_id):
        try:
            return self.database.get_user_match(user_id, match_id)
        except Exception:
            return []

    def keep_user_vk_id(self, user_id):
        self.database.keep_user_vk_id(user_id)
        self.users_cache[user_id] = UserInfo(0, 0, 0, 0, process_stages.new_user_created)

    def update_process_stage(self, user_id, process_stage):
        self.database.update_process_stage(user_id, process_stage)
        info = self.users_cache[user_id]
        info.process_stage = process_stage

    def update_user_offset(self, user_id, offset):
        self.database.update_user_offset(user_id, offset)
        self.offset_cache[user_id] = offset

    def update_user_offered_match(self, user_id, offered_vk_id):
        self.database.update_user_offered_match(user_id, offered_vk_id)
        self.offered_matches_cache[user_id] = offered_vk_id

    def keep_user_age(self, user_id, age):
        self.database.keep_user_age(user_id, age)
        info = self.users_cache[user_id]
        info.age = age

    def keep_user_city_id(self, user_id, city_id):
        self.database.keep_user_city_id(user_id, city_id)
        info = self.users_cache[user_id]
        info.city_id = city_id

    def keep_user_sex(self, user_id, sex):
        self.database.keep_user_sex(user_id, sex)
        info = self.users_cache[user_id]
        info.sex = sex

    def keep_user_relation(self, user_id, relation):
        self.database.keep_user_relation(user_id, relation)
        info = self.users_cache[user_id]
        info.relation = relation

    def get_user_search_offset(self, user_id):
        if user_id in self.offset_cache.keys():
            return self.offset_cache[user_id]
        else:
            user_offset = self.database.get_user_search_offset(user_id)
            self.offset_cache[user_id] = user_offset
            return user_offset

    def get_offered_match(self, user_id):
        if user_id in self.offered_matches_cache.keys():
            return self.offered_matches_cache[user_id]
        else:
            offered_match = self.database.get_offered_match(user_id)
            if offered_match is not None:
                self.offered_matches_cache[user_id] = offered_match
                return offered_match
            return None
