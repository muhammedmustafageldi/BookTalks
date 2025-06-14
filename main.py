from fastapi import FastAPI
from db.models import Base
from db.database import engine
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse
from routers.auth.api_routes import router as auth_api_router
from routers.auth.html_routes import router as auth_html_router
from routers.authors.api_routes import router as authors_api_router
from routers.authors.html_routes import router as authors_html_router
from routers.books.api_routes import router as books_api_router
from routers.books.html_routes import router as books_html_router
from routers.users.api_routes import router as users_api_router
from routers.users.html_routes import router as users_html_router
from routers.comments.api_routes import router as comment_api_router
from routers.comments.html_routes import router as comment_html_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Home page path is -> /books
@app.get("/")
async def index():
    return RedirectResponse(url="/books", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def healthy_check():
    return {'status': 'healthy'}

# Auth routes
app.include_router(auth_api_router)
app.include_router(auth_html_router)

# Authors routes
app.include_router(authors_api_router)
app.include_router(authors_html_router)

# Books routes
app.include_router(books_api_router)
app.include_router(books_html_router)

# Users routes
app.include_router(users_api_router)
app.include_router(users_html_router)

# Comment route
app.include_router(comment_api_router)
app.include_router(comment_html_router)

app.mount("/uploaded_images", StaticFiles(directory='uploaded_images'), name="images")
app.mount("/static", StaticFiles(directory='static'), name="static")