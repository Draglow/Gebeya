# Django Product Posting Website

## Overview
This is a Django-based web application that allows users to post their product items, engage with posts through likes, comments, and replies, and interact with other users. The platform is designed to facilitate seamless product showcasing and user engagement.

## Features
- **User Authentication**: Users can sign up, log in, and manage their profiles.
- **Product Posting**: Users can create and update product listings with images and descriptions.
- **Likes System**: Users can like posts to show appreciation.
- **Comments & Replies**: Users can comment on posts and reply to other comments.
- **Responsive Design**: Fully mobile-friendly UI.
- **Admin Panel**: Manage users and posts from the Django admin interface.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Database**: PostgreSQL / SQLite (for development)
- **Authentication**: Django built-in authentication

## Installation

### Prerequisites
Ensure you have Python installed (version 3.8 or higher).

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/Gebeya.git
   cd Gebeya
   ```
2. Create a virtual environment:
   ```sh
   python -m venv env
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (optional for admin access):
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```
7. Access the application at `http://127.0.0.1:8000/`.



## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

