from fastapi import APIRouter, Depends, HTTPException,status
from schemas.blog import Blog
from sqlalchemy.orm import Session
from db.database import get_db
from models.blog import DbBlog
from typing import List
from hash import Hash
from auth_token import get_current_user



router = APIRouter(
    prefix='/blogs',
    tags=['Blogs']
)


@router.post('/',response_model=Blog)
def create_blog(request : Blog,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    user = current_user
    new_blog = DbBlog(
        title = request.title,
        content = request.content,
        user_id = user.id
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog
   
@router.get('/',response_model=List[Blog])
def get_user_blogs(db:Session = Depends(get_db),current_user = Depends(get_current_user)):

    blogs = db.query(DbBlog).filter(DbBlog.user_id == current_user.id).all()
    return blogs
