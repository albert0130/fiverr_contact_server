from fastapi import APIRouter, HTTPException
from db import db
from schemas import UserSignup, UserSignin
from models import hash_password, verify_password
from bson import ObjectId
from datetime import datetime, timedelta
import pytz

router = APIRouter()

@router.post("/signup")
async def signup(user: UserSignup):
    exists = await db.users.find_one({"name": user.name})
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = hash_password(user.password)
    new_user = {"name": user.name, "password": hashed_pw}
    result = await db.users.insert_one(new_user)
    return {"id": str(result.inserted_id), "user_id": str(result.inserted_id), "name": user.name}

@router.post("/signin")
async def signin(user: UserSignin):
    db_user = await db.users.find_one({"name": user.name})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": str(db_user["_id"]), "user_id": str(db_user["_id"]), "name": db_user["name"]}

@router.get("/users_all")
async def get_all_users():
    try:
        # Simple approach: get all users first
        users = await db.users.find({}, {"name": 1, "_id": 1}).to_list(None)
        
        # For each user, count their lancers
        result = []
        for user in users:
            lancer_count = await db.lancers.count_documents({"user_id": user["_id"]})
            result.append({
                "name": user["name"],
                "contact_count": lancer_count,
                "_id": str(user["_id"])
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/users_day")
async def get_users_day():
    now = datetime.now(pytz.timezone("US/Eastern"))
    if now.hour < 19:
        start_time = (now - timedelta(days=1)).replace(hour=19, minute=0, second=0, microsecond=0)
    else:
        start_time = now.replace(hour=19, minute=0, second=0, microsecond=0)

    pipeline = [
        {
            "$lookup": {
                "from": "lancers",
                "let": {"user_id": "$_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$user_id", "$$user_id"]}, "time": {"$gte": start_time}}},
                ],
                "as": "lancers_today"
            }
        },
        {
            "$project": {
                "name": 1,
                "contact_count": {"$size": "$lancers_today"}
            }
        }
    ]
    users = await db.users.aggregate(pipeline).to_list(None)
    return users
