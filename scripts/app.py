import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.routers import math_router
from scripts.routers import users_router
from scripts.lib.utils.logger import logging_setup, RequestLogMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("⚡ Configuring the loggers...")
    logging_setup()
    print("✅ Logs are set!")
    print("🚀 Running application...")
    yield
    print("🏁 Shutting down application!")

app = FastAPI(title="Boring App", lifespan=lifespan)


app.add_middleware(
        CORSMiddleware,
        allow_origin_regex='http://.*',
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

app.add_middleware(RequestLogMiddleware)

app.include_router(math_router)
app.include_router(users_router)

if __name__ == "__main__":
    # logging_setup() -> Me dice ChatGPT que no es necesario, ya que el logging_setup() del lifespan se ejecuta igualmente.

    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
