from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.user import get_user_by_email
from core.hashing import Hasher
from core.security import create_access_token
from jose import jwt, JWTError
from core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def authenticate_user(email: str,password: str,db: Session):
    user = get_user_by_email(email=email,db=db)
    print(f"DEBUG: Authenticating user {email}")
    if not user:
        print("DEBUG: User not found in DB")
        return False
    
    verification = Hasher.verify_password(password,user.password)
    print(f"DEBUG: Password verification for {email}: {verification}")
    
    if not verification:
        return False
    return user

@router.post('/token')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(detail="Incorrect username or password", status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=username, db=db)
    if user is None:
        raise credentials_exception
    return user