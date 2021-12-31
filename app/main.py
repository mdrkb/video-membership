import json

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
# from app import config
from cassandra.cqlengine.management import sync_table
from app.users.models import User
from app import db, utils
import pathlib
from fastapi.templating import Jinja2Templates
from app.users.schemas import UserSIgnUpSchema, UserLoginSchema

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
# settings = config.get_settings()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
DB_SESSION = None


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home.html", context)


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/login.html", context)


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request,
                    email: str = Form(...),
                    password: str = Form(...)
                    ):
    raw_data = {
        "email": email,
        "password": password
    }
    data, errors = utils.valid_schema_or_error(raw_data, UserLoginSchema)
    context = {
        "request": request,
        "data": data,
        "errors": errors,
    }
    return templates.TemplateResponse("auth/login.html", context)


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/signup.html", context)


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request,
                     email: str = Form(...),
                     password: str = Form(...),
                     password_confirm: str = Form(...),
                     ):
    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data, errors = utils.valid_schema_or_error(raw_data, UserSIgnUpSchema)
    context = {
        "request": request,
        "data": data,
        "errors": errors,
    }
    return templates.TemplateResponse("auth/signup.html", context)


@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)
