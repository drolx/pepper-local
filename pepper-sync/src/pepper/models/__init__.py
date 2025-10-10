from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

from .address import AddressModel, Address, AddressInput, AddressList
from .devices import DeviceModel, Device, DeviceInput, DeviceList, DeviceStatus
from .events import EventModel, Event, EventInput, EventType, EventList
from .geofences import GeofenceModel, Geofence, GeofenceInput, GeofenceList
from .positions import PositionModel, Position, PositionInput, PositionList
from .service_events import ServerEventModel, ServerEvent, ServerEventInput, ServerEventList
from .users import UserModel, UserRole, User, UserInput, UserList

Base = declarative_base()

class Status(BaseModel):
    code: int = 200
    message: str = "Ok"

__all__ = [
    "Address",
    "AddressInput",
    "AddressList",
    "AddressModel",
    "Device",
    "DeviceInput",
    "DeviceList",
    "DeviceModel",
    "DeviceStatus",
    "Event",
    "EventInput",
    "EventList",
    "EventModel",
    "EventType",
    "Geofence",
    "GeofenceInput",
    "GeofenceList",
    "GeofenceModel",
    "Position",
    "PositionInput",
    "PositionList",
    "PositionModel",
    "ServerEvent",
    "ServerEventInput",
    "ServerEventList",
    "ServerEventModel",
    "User",
    "UserInput",
    "UserList",
    "UserModel",
    "UserList",
    "UserRole",
    "Base",
]
