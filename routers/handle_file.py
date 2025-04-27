from fastapi import APIRouter,File,UploadFile
from fastapi.responses import FileResponse
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

@router.get('/download')
def download_file(filename:str):
    path = f"uploaded_files/{filename}"
    return FileResponse(path,media_type='application/octet-stream',filename=filename)



@router.post('/upload-profile')
def upload_profilt(file:UploadFile = File(...)):
    path = f"uploads/{file.filename}"

    with open(path,'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)

    return{
     "filename": path,
     "message": "File uploaded successfully."
}

@router.get('/download-profile/{filename}')
def download_file(filename:str):
    path = f"uploads/{filename}"
    return FileResponse(path,media_type='application/jpeg',filename=filename)


