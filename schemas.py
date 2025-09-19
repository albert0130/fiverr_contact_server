from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from db import PyObjectId

# User schemas
class UserSignup(BaseModel):
    name: str
    password: str

class UserSignin(BaseModel):
    name: str
    password: str

class UserOut(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str

    class Config:
        json_encoders = {PyObjectId: str}
        populate_by_name = True

# Lancer schemas

class LancerOut(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    lancer_id: str
    user_id: PyObjectId
    time: datetime
    status: int

    class Config:
        json_encoders = {PyObjectId: str}
        populate_by_name = True
