# 📝 BlogProject (Django + Docker)

A full-featured blog application built with Django and Docker. This project allows users to create, edit, and engage with blog posts. Designed as a learning-friendly yet production-ready full-stack web app.

---

## 🚀 Features

- 🧑‍💻 User authentication (signup, login, logout)
- ✍️ Create, edit, and delete blog posts
- 💬 Comment system
- ❤️ Like posts
- 👤 User profiles with avatars and bios
- 🖼️ Bootstrap-powered responsive UI
- 🎠 Homepage image carousel
- 🐳 Dockerized for easy development and deployment

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Containerization**: Docker, Docker Compose
- **Production Server**: Gunicorn

---

## 📂 Project Structure

blogproject/ ├── blog_app/ # Blog logic: posts, likes, comments ├── account/ # User registration and profile ├── templates/ # HTML templates ├── static/ # Static files ├── media/ # Uploaded media ├── Dockerfile # Docker image config ├── docker-compose.yml # Multi-container setup ├── .env # Environment variables ├── requirements.txt # Python dependencies ├── manage.py └── db.sqlite3

yaml
Copy
Edit

---

## ⚙️ Getting Started (Docker)

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)


📃 License
This project is licensed under the MIT License. See LICENSE file for details.

🙋‍♂️ Author
Abhiram Pullanikad
📫 GitHub



### 1. Clone the repository

```bash
git clone https://github.com/Abhirampullanikad/blogproject.git
cd blogproject

2. Create .env file
Create a .env file in the project root:


DEBUG=1
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost 127.0.0.1
DATABASE_URL=postgres://bloguser:blogpass@db:5432/blogdb

3. Build and start the containers
docker-compose up --build

4. Run migrations and create superuser

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

5. Access the app
App: http://localhost:8000

Admin: http://localhost:8000/admin

🧪 Development Tips
To run a shell inside the container:


docker-compose exec web bash
To stop containers:


docker-compose down
