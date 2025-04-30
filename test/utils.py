from sqlalchemy import create_engine, StaticPool, text
from main import app
from sqlalchemy.orm import sessionmaker
from db.database import Base
from fastapi.testclient import TestClient
import pytest
from db.models import Book
from db.models import User
from routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_validate_current_user():
    return {'username': "Swanky", 'user_id': 1, 'role': "admin"}


client = TestClient(app=app)

@pytest.fixture
def test_books():
    book = Book(
        id=1,
        title="Küçük Prens",
        author_id=5,
        description="Saint-Exupéry 1943’te Küçük Prens’i yayımladığında, dünya çapında muazzam bir başarı kazanacak bir yapıta imza attığını tahmin bile edemezdi. Bu bilgelikle dolu, büyüleyici masal aradan geçen onca yıla rağmen bütün dünyada her yaştan okurun yüreğini ısıtmaya devam ediyor.",
        rating=5,
        published_date=1970,
        image_path="uploaded_images/books/2d7d0f88-4784-4193-a8cb-50d2c6366fad.jpg",
        page_count=70
    )

    db = TestingSessionLocal()
    db.add(book)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM books;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = User(
        id=1,
        email='swankydata9@gmail.com',
        username='Swanky',
        hashed_password=bcrypt_context.hash("test_password"),
        role='admin'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    # Clean database
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()