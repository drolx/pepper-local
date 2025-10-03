# Copyright (c) 2025 <Godwin peter. O>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#  Project: thalia
#  Author: Godwin peter. O (me@godwin.dev)
#  Created At: Mon 06 Jan 2025 11:47:01
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Mon 06 Jan 2025 11:47:01

import enum
from dataclasses import dataclass

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Sequence,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_enum_values(enum_class):
    return [member.value for member in enum_class]


class DeviceStatus(str, enum.Enum):
    Parked = "parked"
    Moving = "moving"
    Idling = "idling"
    Offline = "offline"


@dataclass
class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, Sequence("device_id_seq"), primary_key=True)
    group_id = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    _status = Column(
        Enum(
            DeviceStatus,
        ),
        nullable=True,
        default=DeviceStatus.Offline,
    )
    time = Column(DateTime(timezone=True), nullable=True)
    unique_id = Column(String, nullable=False)
    position_id = Column(Integer, nullable=True)
    odometer = Column(Float, default=0)
    moved_at = Column(DateTime(timezone=True), nullable=True)
    stoped_at = Column(DateTime(timezone=True), nullable=True)
    battery = Column(Float, default=0)
    charging = Column(Boolean, default=True)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: DeviceStatus):
        self._status = value


@dataclass
class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, Sequence("position_id_seq"), primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)
    speed = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    course = Column(String, nullable=True, default=0)
    altitude = Column(Float, nullable=True, default=0)
    distance = Column(Float, default=0)
    _address = Column(String, nullable=True)
    protocol = Column(String, default="")

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = value


def serialize_row(row, models):
    serialized_data = {}
    for model in models:
        table_name = model.__tablename__
        serialized_data[table_name] = {
            column.name: getattr(row, f"{table_name}_{column.name}")
            for column in model.__table__.columns
        }
    return serialized_data


def serialize_query_results(query_results, models):
    return [serialize_row(row, models) for row in query_results]
