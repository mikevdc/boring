import mariadb
from scripts.lib.db.mariadb_transaction import MariaDBTransaction
from scripts.lib.enums import Operation
from scripts.lib.services.users import logger
from scripts.lib.services.users.model import User
from scripts.lib.services.users.dao import UserDAO


def show_all_users():
    logger.debug("Finding all users...")

    users_dao = UserDAO(logger)

    try:
        with MariaDBTransaction(logger) as db:
            users: list[User] = users_dao.get_all(db)

            if not users:
                logger.debug("No users were found.")
                return None
            return users
        
    except Exception as e:
        logger.error(f"An error was raised: {e}")
    
    return []
