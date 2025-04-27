from fastapi import FastAPI,Request
from db.database import Base,engine
from routers import user,auth,blog,books,handle_file,template
from fastapi.staticfiles import StaticFiles
import time


app = FastAPI(
    title='Blog API',
    description='Create Blogs'
)

@app.get('/')
def root():
    return {
        'message' : "Welcome the Blog API."
    }

app.mount('/ufiles',StaticFiles(directory='uploaded_files'))
app.mount('/templates/static',StaticFiles(directory='templates'))

@app.middleware('http')
async def log_requests(request:Request,call_next):
    start_time = time.time()

    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['X-Process-Time'] = str(duration)
    print(f"Request : {request.url} | Time Taken: {duration}")
    return response




app.include_router(user.router)
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(books.router)
app.include_router(handle_file.router)
app.include_router(template.router)


Base.metadata.create_all(engine)

