from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from scripts.lib.services.math import logger
from scripts.lib.services.math.math import show_all_operations

router = APIRouter(prefix="/maths")

@router.get("/all")
async def get_all_operations():
    logger.info("Searching for all operations.")
    try:
        operations = show_all_operations()
        if not operations:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No operations were found.")
        
        data = {
            "operations": operations
        }

        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = jsonable_encoder(data)
        )

    except Exception as e:
        logger.error("There was a problem while searching for all operations: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An exception occurred while execution.")
    
    finally:
        logger.info("Ends the search for all operations.")
