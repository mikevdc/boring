from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from scripts.lib.services.users import logger
from scripts.lib.services.users.schema import User, UserCreate
from scripts.lib.services.users.users import show_all_users, create_user

router = APIRouter(prefix="/users")

@router.get("/all")
async def get_all_users():
    logger.info("Searching for all users.")
    try:
        users: list[User] = show_all_users()
        if not users:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No users were found.")
        
        data = {
            "users": users
        }

        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = jsonable_encoder(data)
        )

    except Exception as e:
        logger.error(f"There was a problem while searching for all users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An exception occurred while execution.")
    
    finally:
        logger.info("Ends the search for all users.")


@router.post("/create")
async def new_user(user: UserCreate):
    logger.info("Creating a new user.")
    try:
        create_user(user)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = f"User {user.username} created."
        )

    except Exception as e:
        logger.error(f"There was a problem creating the user: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An exception occurred while execution.")
    
    finally:
        logger.info("Ends the creation of a new user.")