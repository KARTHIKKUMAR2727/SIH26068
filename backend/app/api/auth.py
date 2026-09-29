from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from datetime import datetime, timezone
import uuid
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserProfile, UserUpdate
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.core.database import get_collection

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    users_col = get_collection("users")
    user = await users_col.find_one({"email": payload["sub"]})
    return user

@router.post("/register", response_model=TokenResponse)
async def register(user_in: UserRegister):
    users_col = get_collection("users")
    existing = await users_col.find_one({"email": user_in.email})
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email address already exists.")

    user_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    new_user = {
        "_id": user_id,
        "id": user_id,
        "name": user_in.name,
        "email": user_in.email,
        "password_hash": hash_password(user_in.password),
        "preferred_language": user_in.preferred_language or "en",
        "preferred_units": user_in.preferred_units or "metric",
        "default_location": user_in.default_location or "Chennai, Tamil Nadu, India",
        "role": "user",
        "created_at": now
    }
    await users_col.insert_one(new_user)

    token = create_access_token({"sub": new_user["email"], "id": user_id})
    profile = UserProfile(
        id=user_id,
        name=new_user["name"],
        email=new_user["email"],
        preferred_language=new_user["preferred_language"],
        preferred_units=new_user["preferred_units"],
        default_location=new_user["default_location"],
        created_at=now
    )
    return TokenResponse(access_token=token, user=profile)

@router.post("/login", response_model=TokenResponse)
async def login(login_in: UserLogin):
    users_col = get_collection("users")
    user = await users_col.find_one({"email": login_in.email})
    if not user or not verify_password(login_in.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": user["email"], "id": user.get("id", str(user.get("_id")))})
    profile = UserProfile(
        id=user.get("id", str(user.get("_id"))),
        name=user["name"],
        email=user["email"],
        preferred_language=user.get("preferred_language", "en"),
        preferred_units=user.get("preferred_units", "metric"),
        default_location=user.get("default_location", "Chennai, Tamil Nadu, India"),
        created_at=user.get("created_at", datetime.now(timezone.utc).isoformat())
    )
    return TokenResponse(access_token=token, user=profile)

@router.get("/me", response_model=UserProfile)
async def get_me(user: Optional[dict] = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UserProfile(
        id=user.get("id", str(user.get("_id"))),
        name=user["name"],
        email=user["email"],
        preferred_language=user.get("preferred_language", "en"),
        preferred_units=user.get("preferred_units", "metric"),
        default_location=user.get("default_location", "Chennai, Tamil Nadu, India"),
        created_at=user.get("created_at", "")
    )

@router.put("/preferences")
async def update_preferences(prefs: UserUpdate, user: Optional[dict] = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    users_col = get_collection("users")
    updates = {}
    if prefs.name is not None:
        updates["name"] = prefs.name
    if prefs.preferred_language is not None:
        updates["preferred_language"] = prefs.preferred_language
    if prefs.preferred_units is not None:
        updates["preferred_units"] = prefs.preferred_units
    if prefs.default_location is not None:
        updates["default_location"] = prefs.default_location

    if updates:
        await users_col.update_one({"email": user["email"]}, {"$set": updates})
    return {"status": "success", "message": "Preferences updated successfully."}
