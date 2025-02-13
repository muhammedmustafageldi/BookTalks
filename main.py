from fastapi import FastAPI
from db.models import Base
from db.database import engine
from fastapi.staticfiles import StaticFiles
from routers import auth, books, authors, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)

app.mount("/uploaded_images", StaticFiles(directory='uploaded_images'), name="images")