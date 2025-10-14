from fastapi.routing import APIRouter

from pepper.models import Status
from pepper.models.users import User

router = APIRouter(prefix="/api/identity", tags=["identity"])
user_test_response = {}


@router.post("", response_model=User)
async def sign_in():
    return user_test_response


@router.get("", response_model=User)
async def get_session():
    return user_test_response


@router.delete("", response_model=Status)
async def sign_out():
    return Status()

@router.get("/profile", response_model=User)
async def get_profile():
    return user_test_response

