from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from scripts.lib.services.users import logger
from scripts.lib.services.users.model import User
from scripts.lib.services.users.users import show_all_users

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
        logger.error("There was a problem while searching for all users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An exception occurred while execution.")
    
    finally:
        logger.info("Ends the search for all users.")
