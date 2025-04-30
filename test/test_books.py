from routers.books import get_db, validate_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[validate_current_user] = override_validate_current_user


def test_read_all(test_books):
    response = client.get("/books")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1,
                                "title": "Küçük Prens",
                                "author_id": 5,
                                "description": "Saint-Exupéry 1943’te Küçük Prens’i yayımladığında, dünya çapında muazzam bir başarı kazanacak bir yapıta imza attığını tahmin bile edemezdi. Bu bilgelikle dolu, büyüleyici masal aradan geçen onca yıla rağmen bütün dünyada her yaştan okurun yüreğini ısıtmaya devam ediyor.",
                                "rating": 5,
                                "published_date": 1970,
                                "image_path": "uploaded_images/books/2d7d0f88-4784-4193-a8cb-50d2c6366fad.jpg",
                                "page_count": 70}]


def test_update_page_count(test_books):
    response = client.put("/books/update_page_count/?book_id=1&page_count=100")
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    model = db.query(Book).filter(Book.id == 1).first()
    assert model.page_count == 100

