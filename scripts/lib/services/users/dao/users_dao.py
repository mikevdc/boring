import mariadb

from scripts.lib.db.mariadb_transaction import MariaDBTransaction
from scripts.lib.services.users import logger
from scripts.lib.services.users.model import User

class UserDAO:

    def __init__(self, logger):
        self.logger = logger
        

    def get_all(self, transaction: MariaDBTransaction) -> list[User]:
        self.logger.debug(f"UserDAO.get_all()")
        sql = f'''
SELECT
    username,
    email,
    created_at
FROM
    users'''
        params: list = []
        try:
            users = transaction.execute_query(sql, params)
            if users:
                return [User(**user) for user in users]

        except ConnectionError as e:
            logger.error(f"Error: {e}")

        except mariadb.Error as e:
            logger.error(f"An error was raised executing a DB query: {e}")
        
        return []

        
