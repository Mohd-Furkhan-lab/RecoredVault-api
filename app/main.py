from fastapi import FastAPI
from apis.v1.records import records
from apis.v1.users import users


app=FastAPI()
app.include_router(records)
app.include_router(users)


def get_app():
    return app

    