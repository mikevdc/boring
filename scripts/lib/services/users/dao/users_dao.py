import mariadb

from scripts.lib.db.mariadb_transaction import MariaDBTransaction
from scripts.lib.services.users import logger
from scripts.lib.services.users.schema import User, UserCreate

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

    def get_by_username(self, username: str, transaction: MariaDBTransaction) -> bool:
        self.logger.debug(f"UserDAO.get_by_username()")
        sql = f'''
SELECT
    username
FROM
    users
WHERE
    username = %s'''
        params: list = [username]
        try:
            username = transaction.execute_query(sql, params)

        except ConnectionError as e:
            logger.error(f"Error: {e}")

        except mariadb.Error as e:
            logger.error(f"An error was raised executing a DB query: {e}")

        if username:
            return True
        return False


    def create(self, user: UserCreate, transaction: MariaDBTransaction) -> int:
        self.logger.debug(f"UserDAO.get_by_username()")
        sql = f'''
INSERT into users (USERNAME, PASSWORD, EMAIL, CREATED_AT)
VALUES (%s, %s, %s, CURRENT_TIMESTAMP)'''
        params: list = [user.username, user.password, user.email]
        try:
           return transaction.execute_insert(sql, params)

        except ConnectionError as e:
            logger.error(f"Error: {e}")

        except mariadb.Error as e:
            logger.error(f"An error was raised executing a DB query: {e}")