from typing import List, Optional
import uuid

from fastapi.routing import APIRouter

from pepper.models import Status
from pepper.models.users import User, UserInput

router = APIRouter(prefix="/api/users", tags=["users"])
user_test_response = User(id=uuid.uuid4(), full_name="Test user", phone="099988373737", email="test@dev.local")

@router.get("", response_model=List[User])
async def get_users(search: str | None = None, page: int = 1, limit: int = 1000):
    return [user_test_response]


@router.get("/{id:path}", response_model=User | Status)
async def get_user_by_id(id: uuid.UUID):
    if user_test_response.id is not id:
        return Status(code=500, message="Request failed")

    return user_test_response

@router.post("", response_model=User)
async def create_user(payload: UserInput):
    return payload


@router.put("", response_model=User)
async def update_user(payload: UserInput):
    return payload

@router.delete("/{id:path}", response_model=Status)
async def delete_user(id: uuid.UUID):
    return Status(message=f"user {id} deleted sucessfully")


