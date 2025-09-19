# FastAPI Backend Project

A FastAPI backend application with MongoDB integration for user management and lancer tracking.

## Features

- User authentication (signup/signin)
- Lancer management with status tracking
- EDT timezone support
- CORS enabled for frontend integration

## API Endpoints

### Users
- `POST /signup` - Create new user
- `POST /signin` - User authentication
- `GET /users_all` - Get all users with lancer counts
- `GET /users_day` - Get users with today's lancer activity

### Lancers
- `GET /get_lancer/{lancer_id}` - Get lancer details by ID
- `PUT /change_status/{lancer_id}` - Update lancer status (creates if doesn't exist)

## Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn motor pymongo passlib[bcrypt] python-multipart pytz
```

2. Set environment variables:
```bash
export MONGO_URI="mongodb://localhost:27017"
export DB_NAME="fastapi_db"
```

3. Run the server:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Database

The application uses MongoDB with the following collections:
- `users` - User accounts
- `lancers` - Lancer records with status tracking

## Timezone

All timestamps are stored and displayed in EDT (Eastern Daylight Time).

