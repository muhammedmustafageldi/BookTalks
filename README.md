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
  ![Register Page](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/2.png)
  ![Login Page](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/1.png)
</p>

### Book Browsing

<p align="center">
  ![Main Books Page](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/3.png)
  ![Book Details](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/4.png)
</p>

### Comments System

<p align="center">
  ![Book Comments 1](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/5.png)
  ![Book Comments 2](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/6.png)
</p>

### Authors

<p align="center">
  ![Authors List](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/7.png)
  ![Author Details](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/8.png)
</p>

### User Profile

<p align="center">
  ![User Profile Page](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/10.png)
</p>

### API Documentation

<p align="center">
  ![Swagger UI 1](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/11.png)
  ![Swagger UI 2](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/12.png)
  ![Swagger UI 3](https://github.com/muhammedmustafageldi/My-Github-Files/blob/main/Screnshots/BookTalks/13.png)
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
