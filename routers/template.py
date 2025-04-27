from fastapi import APIRouter,Form,UploadFile,File,Request
from fastapi.templating import Jinja2Templates
import shutil


router = APIRouter(
    prefix='/templates',
    tags=['Templates']
)

templates = Jinja2Templates(directory='templates')

@router.post('/user-profile')
def user_profile(
    request : Request,
    name : str = Form(...),
    email : str = Form(...),
    bio : str = Form(...),
    avtar : UploadFile = File(...)
):
 avatar_url = None
 if avtar:
  file_location = f"templates/static/avtars/{avtar.filename}"

  with open(file_location,'wb') as buffer:
   shutil.copyfileobj(avtar.file,buffer)

  avatar_url = file_location

  return templates.TemplateResponse('user_profile.html',{
   'request':request,
   'name' :name,
   'email' : email,
   'bio' : bio,
   'avatar_url': avatar_url
  })