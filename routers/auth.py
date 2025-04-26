from fastapi import APIRouter,Depends,HTTPException,status
from schemas.user import Token,Login
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import DbUser
from hash import Hash
from auth_token import create_token
from fastapi.security import OAuth2PasswordRequestForm




router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/login',response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()


    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    if not Hash.verify(request.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    access_token = create_token({'sub' : user.username})
    return {
        'access_token' : access_token
    }

