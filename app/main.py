from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# from app import config
from cassandra.cqlengine.management import sync_table
from app.users.models import User
from app import db
import pathlib
from fastapi.templating import Jinja2Templates

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


@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)
