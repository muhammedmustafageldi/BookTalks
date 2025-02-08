from fastapi import FastAPI
from models import Base
from database import engine
from fastapi.staticfiles import StaticFiles
from routers import auth, books, authors

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(authors.router)

app.mount("/uploaded_images", StaticFiles(directory='uploaded_images'), name="images")