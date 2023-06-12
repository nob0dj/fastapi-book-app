from fastapi import FastAPI

import config
from auth import auth_router
from books import books_router
from kollections import kollections_router
from database import Base, engine
from scraps import scraps_router


app = FastAPI()

# router
app.include_router(router=books_router.router)
app.include_router(router=scraps_router.router)
app.include_router(router=auth_router.router)
app.include_router(router=kollections_router.router)

# database
Base.metadata.create_all(bind=engine)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
