from fastapi import FastAPI
from . import config
from cassandra.cqlengine.management import sync_table
from .users.models import User
from . import db

app = FastAPI()
settings = config.get_settings()
DB_SESSION = None


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/")
def homepage():
    return {"Hello": "World!"}
