from fastapi import FastAPI
from db.database import Base,engine
from routers import user,auth,blog,books,handle_file
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title='Blog API',
    description='Create Blogs'
)

@app.get('/')
def root():
    return {
        'message' : "Welcome the Blog API."
    }

app.mount('/files',StaticFiles(directory='uploaded_files'))


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(books.router)
app.include_router(handle_file.router)


Base.metadata.create_all(engine)