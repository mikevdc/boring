from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scripts.routers import math_router

def create_test_app() -> FastAPI:
    app = FastAPI(title="Boring App - Test")

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(math_router)

    return app


app = create_test_app()