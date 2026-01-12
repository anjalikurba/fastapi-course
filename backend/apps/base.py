from fastapi import APIRouter
from apps.v1 import route_blog
from apps.v1 import route_login

app_router = APIRouter()
app_router.include_router(route_blog.router, prefix="", tags=["Home"])
app_router.include_router(route_login.router, prefix="/auth", tags=["Login"])
