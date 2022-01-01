from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from cassandra.cqlengine.management import sync_table
from app.users.models import User
from app import db, utils
from app.users.schemas import UserSIgnUpSchema, UserLoginSchema
from app.shortcuts import render

app = FastAPI()
DB_SESSION = None


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return render(request, "home.html")


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get("session_id") or None
    return render(request, "auth/login.html", {"logged_in": session_id is not None})


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
        "data": data,
        "errors": errors,
    }

    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)
    else:
        return render(request, "auth/login.html", {"logged_in": True}, cookies=data)


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "auth/signup.html")


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
        "data": data,
        "errors": errors,
    }

    if len(errors) > 0:
        return render(request, "auth/signup.html", context, status_code=400)
    else:
        return render(request, "auth/signup.html", context)


@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)
