# 📚 BookTalks - FastAPI Book Management Application

A fullstack book management application built with FastAPI, featuring user authentication, book catalog, reviews, and a responsive UI! 🚀

## 🔍 About The Project

BookTalks is a comprehensive book management system that allows users to browse books, read details, leave comments, and mark favorites. Administrators have special privileges like adding new books and authors.

## 🛠️ Technologies & Architecture

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: JWT token-based auth with role management
- **Architecture Highlights**:
  - 📂 **Repository Pattern**: Clean separation of data access logic
  - 🔀 **Router Segregation**: Separate API and HTML routers for each module
  - 🧩 **Modular Structure**: Organized by feature (books, authors, users)
  - 🖼️ **Templates**: Jinja2 templates with partial rendering support
  - 🔒 **Security**: Password hashing and JWT authentication
  - 📱 **Responsive Design**: Mobile-friendly interface

## 📸 Screenshots

### Authentication System

<p align="center">
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/2.png" alt="Register Page" width="400"/>
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/1.png" alt="Login Page" width="400"/>
</p>

### Book Browsing

<p align="center">
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/3.png" alt="Main Books Page" width="400"/>
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/4.png" alt="Book Details" width="400"/>
</p>

### Comments System

<p align="center">
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/5.png" alt="Book Comments 1" width="400"/>
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/6.png" alt="Book Comments 2" width="400"/>
</p>

### Authors

<p align="center">
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/7.png" alt="Authors List" width="400"/>
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/8.png" alt="Author Details" width="400"/>
</p>

### User Profile

<p align="center">
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/10.png" alt="User Profile Page" width="400"/>
</p>

### API Documentation

<p align="center">
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/11.png" alt="Swagger UI 1" width="400"/>
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/12.png" alt="Swagger UI 2" width="400"/>
  <img src="https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/13.png" alt="Swagger UI 3" width="400"/>
</p>

## 🚀 Features

- User registration and authentication
- Book browsing and searching
- Author information
- Commenting system with nested replies
- User favorites management
- Admin privileges for content management
- File uploads for book covers, author images
- Responsive design for all devices

## 🔧 Setup and Installation

```bash
# Clone the repository
git clone https://github.com/muhammedmustafageldi/BookTalks.git

# Navigate to project directory
cd BookTalks

# Install dependencies
pip install -r requirements.txt

# Set up the database
alembic upgrade head

# Run the application
uvicorn main:app --reload
```

## 👤 Author

**Muhammed Mustafa Geldi**  
GitHub: [muhammedmustafageldi](https://github.com/muhammedmustafageldi)

### License 📝
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you like this project, don't forget to give it a star! ✨
