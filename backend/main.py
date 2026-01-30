from fastapi import FastAPI
from core.config import settings
from db.session import engine 
from db.base import Base
from apis.base import api_router
from apps.base import app_router
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()

def include_router(app):
	app.include_router(api_router)
	app.include_router(app_router)

def configure_static(app):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


def create_tables():
	Base.metadata.create_all(bind=engine)

def start_application():
	app = FastAPI(title=settings.PROJECT_TITLE,version=settings.PROJECT_VERSION)
	include_router(app)
	configure_static(app)
	create_tables()
	
	return app

app = start_application()

@app.get("/")
def home():
    return {"message": "Hello World"}

