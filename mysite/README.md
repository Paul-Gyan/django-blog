# Django Blog App 📝

A full stack blog application built with Django and React.

## 🌐 Live Demo
Coming soon...

## 🛠️ Built With
- **Backend:** Python, Django, Django REST Framework
- **Frontend:** React.js
- **Database:** SQLite (development)
- **Authentication:** Django built-in auth

## ✨ Features
- View all blog posts
- Create, edit and delete posts
- User registration and login
- REST API for frontend integration
- Responsive design

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- Git

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Paul-Gyan/django-blog.git

# Navigate to project
cd django-blog

# Install dependencies
pip install django djangorestframework django-cors-headers

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver


#Frontend Setup
#Navigate to frontend folder
cd frontend

#Install dependencies
npm install

#start React app
npm start

#Usage
1. Visit http://127.0.0.1:800 for the Django app
2. visit http://localhost:3000 for React
3. visit htt://127.0.0.1:800/admin for the admin panel
4. Register an account to create post

#Project Structure
django-blog/
├── mysite/          ← Django settings
├── blog/            ← Main app
│   ├── models.py    ← Database models
│   ├── views.py     ← App logic
│   ├── urls.py      ← URL routing
│   ├── serializers.py ← API serializers
│   └── templates/   ← HTML templates
└── frontend/        ← React app
    └── src/
        └── App.js   ← Main React component

API Endpoints

Method   URL                 Desvription
GET      /api/posts/         Get all posts
GET      /api/posts/:id/     Get single post
POST     /api/posts/create/  Create a post

AUthor
Paul Gyan

.GitHub: @Paul-Gyan

License
This project is open source and available under the MIT License