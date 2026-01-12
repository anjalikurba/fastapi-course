
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.user import UserCreate,ShowUser
from db.repository.user import create_new_user, get_user_by_email

router = APIRouter()

@router.post("/",response_model = ShowUser,status_code=status.HTTP_201_CREATED)
def create_user(user : UserCreate,db : Session = Depends(get_db)):
    user_exist = get_user_by_email(email=user.email, db=db)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = create_new_user(user = user,db = db)
    return user
