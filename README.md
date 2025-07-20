## 🎬 Movies Club API
A RESTful Flask API backend for the Movies Club platform — where users can sign up, post and review movies, join clubs based on genre, follow other users, and track watched films.

## 📁 Project Structure
```
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── seed.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── movie_post_routes.py
│   │   ├── club_routes.py
│   │   ├── comment_feed_routes.py
│   │   └── watch_routes.py
├── migrations/
├── instance/
│   └── app.db  # (if SQLite is used)
├── tests/
├── .env
├── app.py
├── config.py
├── requirements.txt
├── README.md
```
## 🛠️ Setup Instructions
## 1. Clone the Repository 
``
`git clone https://github.com/TV-Series-Movies-Club/Back-End`
`cd movies-club-api`

 ## 2. Create & Activate Virtual Environment 
``
`python3 -m venv venv`
`source venv/bin/activate`  
`source venv/bin/activate.fish` # On Windows use: 

## 3. Install Dependencies 

`pip install -r requirements.txt`

## 4. Configure Environment Variables 
Create a .env file in the root directory with the following:
``
`FLASK_APP=app`
`FLASK_ENV=development`
`JWT_SECRET_KEY=your_jwt_secret`
`DATABASE_URL=sqlite:///movies_club.db`

If using PostgreSQL:

`DATABASE_URL=postgresql://username:password@localhost:5000/movies_club`

Make sure your PostgreSQL server is running and the database exists.

## 5. Initialize the Database 
``
`flask db init`
`flask db migrate -m "Initial migration"`
`flask db upgrade`
`python app/seed.py` (Optional) To seed data:

## 🚀 Running the App 
Start the development server:
``
`flask run`
`Visit: http://127.0.0.1:5000/`

### 🔐 Authentication
This API uses JWT-based authentication.

On login, receive an access and refresh token.

Send requests to protected endpoints using:
``
`Authorization: Bearer <access_token>`

## 📮 Endpoints Overview
| Method | Endpoint                                   | Description              |
| ------ | ------------------------------------------ | ------------------------ |
| POST   | /auth/signup                               | Register a new user      |
| POST   | /auth/login                                | Login and receive tokens |
| GET    | /users/me                                  | Get current user info    |
| PUT    | /users/profile                             | Update profile info      |
| PUT    | /users/profile/password                    | Change password          |
| POST   | /movies/                                   | Add a movie post         |
| POST   | /clubs/                                    | Create a movie club      |
| POST   | /feeds/comments/posts/\<post\_id>/comments | Comment on a post        |
| POST   | /watch/                                    | Log a watched movie      |
| GET    | /watch/                                    | View watched movies      |


## 🧾 Technologies Used
-Python 3
-Flask
-Flask SQLAlchemy
-Flask JWT Extended
-Flask Migrate
-PostgreSQL or SQLite
-dotenv
-CORS

## 👨‍💻 Author
Billadams Nyamweno — GitHub