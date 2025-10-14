
from fastapi.routing import APIRouter
from pepper import queue_forward

from pepper.types.forward import ForwardObject

router = APIRouter(prefix="/api/forward", tags=["forward"])

@router.post("")
async def create_user(payload: ForwardObject):
    typed_payload = payload.model_dump(exclude_unset=True)
    queue_forward.push(typed_payload)