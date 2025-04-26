from fastapi import APIRouter, Depends, HTTPException,status
from schemas.user import UserBase,UserDisplay,UserPartial
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import DbUser
from typing import List
from hash import Hash
from auth_token import get_current_user



router = APIRouter(
    prefix='/users',
    tags=['Users']
)



@router.post('/',response_model=UserDisplay)
def create_user(request : UserBase ,db:Session = Depends(get_db)):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @router.post('/create',response_model=UserDisplay)
# def create_user(request : UserBase ,db:Session = Depends(get_db)):
#     new_user = DbUser(**request.model_dump())

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

@router.get('/',response_model=List[UserDisplay])
def get_users(db:Session = Depends(get_db)):
    users = db.query(DbUser).all()
    return users


@router.get('/user',response_model=UserDisplay)
def get_user(db:Session = Depends(get_db), current_user = Depends(get_current_user)):

    user = current_user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    return user

@router.put('/{id}',response_model=UserDisplay)
def update_user(id:int, request: UserBase, db:Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
    )

    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)

    db.commit()
    db.refresh(user)
    return user


@router.patch('/{id}',response_model=UserDisplay)
def update_user(id:int, request: UserPartial, db:Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.id == id).first()

    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )


    if request.username is not None:
        user.username = request.username
    if request.email is not None:
        user.email = request.email
    if request.password is not None:
         user.password = Hash.bcrypt(request.password)

    db.commit()
    db.refresh(user)
    return user


@router.delete('/{id}')
def delete_user(id:int, db:Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    db.delete(user)
    db.commit()
    return f"User with ID :{id} deleted successfully"
