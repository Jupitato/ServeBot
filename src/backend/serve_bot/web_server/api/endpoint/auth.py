from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr

auth_router = APIRouter()

# 简单的用户数据存储（实际应用中应使用数据库）
users_db = {
    "test@example.com": {
        "id": "user-001",
        "name": "测试用户",
        "email": "test@example.com",
        "password": "password123"  # 实际应用中应存储哈希值
    }
}

# JWT密钥（实际应用中应存储在环境变量中）
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    accessToken: str


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@auth_router.post("/auth/login", response_model=UserResponse)
async def login(login_data: LoginRequest):
    user = users_db.get(login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    if user["password"] != login_data.password:  # 实际应用中应比较哈希值
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    # 创建访问令牌
    access_token = create_access_token(
        data={"sub": user["email"], "id": user["id"]}
    )

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "accessToken": access_token
    }


# 用于验证令牌的依赖项
async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="无效的认证凭据")
        user = users_db.get(email)
        if user is None:
            raise HTTPException(status_code=401, detail="用户不存在")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="无效的认证凭据")


@auth_router.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"]
    }
