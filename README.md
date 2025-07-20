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
``` 
`git clone https://github.com/TV-Series-Movies-Club/Back-End`
`cd movies-club-api`
```
 ## 2. Create & Activate Virtual Environment 
```
`python3 -m venv venv`
`source venv/bin/activate` # On Windows use: `source venv/bin/activate.fish`   
```
## 3. Install Dependencies 

`pip install -r requirements.txt`

## 4. Configure Environment Variables 
Create a .env file in the root directory with the following:
```
`FLASK_APP=app`
`FLASK_ENV=development`
`JWT_SECRET_KEY=your_jwt_secret`
`DATABASE_URL=sqlite:///movies_club.db`
If using PostgreSQL:
`DATABASE_URL=postgresql://username:password@localhost:5000/movies_club`
```
Make sure your PostgreSQL server is running and the database exists.

## 5. Initialize the Database 
```
`flask db init`
`flask db migrate -m "Initial migration"`
`flask db upgrade`
`python app/seed.py` (Optional) To seed data:

```
## 🚀 Running the App 
Start the development server:
```
`flask run`
Visit: http://127.0.0.1:5000/
```
### 🔐 Authentication
This API uses JWT-based authentication.
On login, receive an access and refresh token.
Send requests to protected endpoints using:
``
`Authorization: Bearer <access_token>`

## 🧪 API Testing Tool

This project uses [Thunder Client](https://www.thunderclient.com/) — a lightweight REST API client extension for VS Code — for testing and interacting with the API endpoints during development.

### 🚀 How to Use Thunder Client

1. Install Thunder Client from the VS Code Extensions Marketplace.
2. Open the Thunder Client tab on the sidebar.
3. Create a new collection and add requests to test the API.
4. Include Authorization headers (e.g., JWT token) where necessary.
5. Send requests to endpoints like `http://localhost:5000/`.

## 📌 Core API Features

| **Feature**                 | **Endpoint(s)**                              | Method |
| --------------------------- | -------------------------------------------- | ------ |
| Signup                      | /auth/signup                                 | POST   |
| Login                       | /auth/login                                  | POST   |
| View Profile                | /users/me                                    | GET    |
| Update Profile              | /users/profile                               | PUT    |
| Change Password             | /users/profile/password                      | PUT    |
| Create a Post               | /posts/                                      | POST   |
| View All Posts              | /posts/                                      | GET    |
| Get a Specific Post         | /posts/\<post\_id>                           | GET    |
| Follow/Unfollow User        | /users/follow/<id>, /unfollow/<id>           | POST   |
| View Followers/Following    | /users/<id>/followers, /users/<id>/following | GET    |
| Create a Movie Club         | /clubs/                                      | POST   |
| Join a Movie Club           | /clubs/\<club\_id>/join                      | POST   |
| Comment/Review a Post       | /feeds/comments/posts/\<post\_id>/comments   | POST   |
| Get Comments on a Post      | /feeds/comments/posts/\<post\_id>/comments   | GET    |
| Track Watched Movies        | /watch/                                      | POST   |
| View Watched Movies History | /watch/                                      | GET    |

Most endpoints (except signup/login) require a Bearer token in the Authorization header:

Authorization: Bearer <your_jwt_token>

## 🧾 Technologies Used

- **Python 3**
- **Flask**
- **Flask SQLAlchemy**
- **Flask JWT Extended**
- **Flask Migrate**
- **PostgreSQL or SQLite**
- **dotenv**
- **CORS**

## 👨‍💻 Author
Billadams Nyamweno — GitHub