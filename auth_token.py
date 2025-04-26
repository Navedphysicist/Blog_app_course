from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from typing import Optional
from datetime import datetime , timedelta, timezone
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import DbUser

SECRET_KEY  = 'SECRET'
ALGORITHIM  = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def create_token(data:dict , expires_delta : Optional[timedelta] = timedelta(30)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})

    encoded_jwt =  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHIM)
    return encoded_jwt


def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):

    credentials_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not authenticated',
            headers={'WWW-Authenticate':'Bearer'}
        )

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHIM)
        username = payload.get('sub')

        if not username:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception
    
    user  = db.query(DbUser).filter(DbUser.username == username).first()

    if not user:
        raise credentials_exception
    
    return user
