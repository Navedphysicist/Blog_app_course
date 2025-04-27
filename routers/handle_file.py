from fastapi import APIRouter,File,UploadFile
import shutil


router = APIRouter(
    prefix='/files',
    tags=['files']
)


@router.post('/')
def get_file(file:bytes = File(...)):
    content = file.decode('utf-8')
    content_lines = content.split('\n')
    content_lines = [ x.upper() for x in content_lines ]

    return {
        'content_lines' : content_lines
    }


@router.post('/upload')
def get_upload(uploaded_file : UploadFile = File(...)):
    path = f"uploaded_files/{uploaded_file.filename}"

    with open(path,'w+b') as new_file:
        shutil.copyfileobj(uploaded_file.file,new_file)

    return {
        'msg':'file successfully created',
        'path':path
    }




