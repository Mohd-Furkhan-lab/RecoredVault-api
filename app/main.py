from fastapi import FastAPI
from apis.v1.records import records
from apis.v1.users import users
from repo.db import engine,Base
from create_admin import createadmin

app=FastAPI()
app.include_router(records)
app.include_router(users)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    createadmin()


def get_app():
    return app

    