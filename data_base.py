import random
from pprint import pprint
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://vkinder:123456@localhost:5432/vkinder')
connection = engine.connect()


def keep_user_desicion(user_id, match_id, decision):
    connection.execute(
        f"INSERT INTO desicionstatus (vkid_searching, vkid_match, status) "
        f"VALUES ('{user_id}', '{match_id}', '{decision}');")
