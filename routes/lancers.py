from fastapi import APIRouter, HTTPException
from db import db
from datetime import datetime
from bson import ObjectId
import pytz

router = APIRouter()


@router.get("/get_lancer/{lancer_id}")
async def get_lancer(lancer_id: str):
    lancer = await db.lancers.find_one({"lancer_id": lancer_id})
    if not lancer:
        return {"user_id": None, "user_name": None}
    
    # Get user name from user_id
    user = await db.users.find_one({"_id": lancer["user_id"]}, {"name": 1})
    user_name = user["name"] if user else "Unknown User"
    
    # Handle time display - if timezone info exists, use it
    time_display = lancer["time"]
    if "timezone" in lancer and lancer["timezone"]:
        # Convert to EDT for display if needed
        if lancer["time"].tzinfo is None:
            # If time is naive, assume it's in the stored timezone
            edt_tz = pytz.timezone(lancer["timezone"])
            time_display = edt_tz.localize(lancer["time"])
        else:
            # Convert to EDT timezone
            edt_tz = pytz.timezone("US/Eastern")
            time_display = lancer["time"].astimezone(edt_tz)
    
    return {
        "lancer_id": lancer["lancer_id"],
        "user_id": str(lancer["user_id"]),
        "user_name": user_name,
        "time": time_display,
        "status": lancer["status"]
    }

@router.put("/change_status/{lancer_id}")
async def change_status(lancer_id: str, status: int, user_id: str):
    # Convert string user_id to ObjectId
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    
    # Check if user exists
    user = await db.users.find_one({"_id": user_object_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if lancer exists
    existing_lancer = await db.lancers.find_one({"lancer_id": lancer_id})
    
    if existing_lancer:
        # Update existing lancer status
        result = await db.lancers.update_one(
            {"lancer_id": lancer_id},
            {"$set": {"status": status}}
        )
        return {"message": "Status updated"}
    else:
        # Create new lancer with the given status
        # Get current time in EDT timezone
        edt_timezone = pytz.timezone("US/Eastern")
        edt_time = datetime.now(edt_timezone)
        
        # Store both the EDT time and timezone info
        new_lancer = {
            "lancer_id": lancer_id,
            "user_id": user_object_id,
            "time": edt_time,
            "timezone": "US/Eastern",  # Store timezone info separately
            "status": status
        }
        result = await db.lancers.insert_one(new_lancer)
        return {"message": "Lancer created with status", "id": str(result.inserted_id)}
