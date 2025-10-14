import uuid

from fastapi import HTTPException
from fastapi.routing import APIRouter

from pepper.models import Status
from pepper.models.users import User, UserInput, UserModel

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=list[User])
async def get_users(search: str = "", page: int = 1, limit: int = 1000):  # pyright: ignore[reportUnusedParameter]
    offset =  (page - 1) * limit 
    query = UserModel.all().filter(full_name__contains=search).offset(offset).limit(limit)
    return await User.from_queryset(query)


@router.get("/{id:path}", response_model=User | Status)
async def get_user_by_id(id: uuid.UUID):
    query = UserModel.get(id=id)
    return await User.from_queryset_single(query)

@router.post("", response_model=User)
async def create_user(payload: UserInput):
    typed_payload = payload.model_dump(exclude_unset=True)
    typed_payload["password_hash"] = "x"
    user_obj = await UserModel.create(**typed_payload)  # pyright: ignore[reportAny]
    return await User.from_tortoise_orm(user_obj)


@router.put("", response_model=User)
async def update_user(payload: UserInput):
    id = payload.id
    filtered_payload = payload.model_dump(exclude_unset=True)
    await UserModel.filter(id=id).update(**filtered_payload)
    return await User.from_queryset_single(UserModel.get(id=id))

@router.delete("/{id:path}", response_model=Status)
async def delete_user(id: uuid.UUID):
    deleted_count = await UserModel.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return Status(message=f"Deleted user {id}")


