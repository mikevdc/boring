import mariadb

from fastapi import HTTPException, status
from scripts.lib.db.mariadb_transaction import MariaDBTransaction
from scripts.lib.enums import Operation
from scripts.lib.services.users import logger
from scripts.lib.services.users.schema import User, UserCreate
from scripts.lib.services.users.dao import UserDAO


def show_all_users():
    logger.debug("Finding all users...")

    users_dao = UserDAO(logger)

    try:
        transaction: MariaDBTransaction = MariaDBTransaction(logger)
        if transaction is None:
            raise ConnectionError("Couldn't get a connection.")
        
        users: list[User] = users_dao.get_all(transaction)

        if not users:
            logger.debug("No users were found.")
            return None
        return users
        
    except Exception as e:
        logger.error(f"An error was raised: {e}")
    
    return []


def create_user(user: UserCreate) -> int:
    logger.debug(f"Creating new user {user.username}")
    
    user_id: int | None = None
    users_dao = UserDAO(logger)
    try:
        transaction: MariaDBTransaction = MariaDBTransaction(logger)
        if transaction is None:
            raise ConnectionError("Couldn't get a connection.")
        
        username = user.username
        logger.debug(f"Checking if username {username} already exists...")

        username_already_exists = users_dao.get_by_username(username, transaction)
        if username_already_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The username {username} already exists.")
        
        logger.debug(f"Username {username} doesn't exist.")
        user_id = users_dao.create(user, transaction)
        transaction.commit()
    
    except Exception as e:
        transaction.rollback()
        raise e
    
    if not user_id:
        transaction.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="The user wasn't created.")
    return user_id

