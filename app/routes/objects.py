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
#  Project: pepper-local
#  Author: Godwin peter. O (me@godwin.dev)
#  Created At: Thu 09 Jan 2025 18:18:52
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Thu 09 Jan 2025 18:18:52

import json
from typing import List, Tuple
from aiohttp import web
from sqlalchemy import Row
from sqlalchemy.orm import Session
from utils import CustomJSONEncoder
from app.db import get_db
from app.models import Device, Position


def serialize_device_results(query_results: List[Row[Tuple[Device, Position]]]):
    results = []
    for device, position in query_results:
        results.append(
            {
                "id": device.id,
                "group_id": device.group_id,
                "name": device.name,
                "time": device.time,
                "status": device.status,
                "address": position.address,
                "speed": position.speed,
                "latitude": position.latitude,
                "longitude": position.longitude,
                "course": position.course,
                "altitude": position.altitude,
                "moved_at": device.moved_at,
                "stoped_at": device.stoped_at,
                "odometer": device.odometer,
                "battery": device.battery,
                "charging": device.charging,
            }
        )
    return results


async def get_recent_status(request: web.Request) -> web.Response:
    search: str = request.rel_url.query.get("search", "")
    page = int(request.rel_url.query.get("page", 1))
    limit = int(request.rel_url.query.get("limit", 250))
    offset = (page - 1) * limit

    db: Session = get_db()
    result = (
        db.query(
            Device,
            Position,
        )
        .join(Position, Device.position_id == Position.id)
        .order_by(Device.name)
        .filter(Device.name.like(f"%{search}%"))
        .limit(limit)
        .offset(offset)
        .all()
    )

    serialized_results = serialize_device_results(result)
    text = json.dumps(serialized_results, cls=CustomJSONEncoder)

    return web.json_response(json.loads(text))
