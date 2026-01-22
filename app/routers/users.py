from fastapi import APIRouter,Depends, HTTPException
from app.database import users_collection
from app.auth import hash_password, verify_password, create_access_token, admin_required
from datetime import datetime
from bson import ObjectId

from app.schemas import loginSchema, UserSchema

router = APIRouter()

@router.get("/all", dependencies=[Depends(admin_required)])
async def get_all_users():
    users = await users_collection.find({}, {"password": 0}).to_list(length=None)  # Exclude password field
    for user in users:
        user["_id"] = str(user["_id"])
    return users

@router.post("/register")
async def register(data: loginSchema):
    if await users_collection.find_one({"email": data.email}):
        raise HTTPException(400, "User already exists")

    await users_collection.insert_one({
        "email": data.email,
        "password": hash_password(data.password),
        "role": "user",
        "created_at": datetime.utcnow()
    })
    return {"message": "User registered"}


@router.post("/login")
async def login(data: loginSchema):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(user)
    return {"access_token": token}

@router.put("/users/{user_}/role")
async def update_user_role(
    user_id: str,
    role: str,
    current_user=Depends(admin_required)
):
    if role not in ["admin", "user"]:
        raise HTTPException(400, "Invalid role")

    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": role}}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "User not found")

    return {
        "message": f"User role updated to '{role}'"
    }
