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
#  Created At: Thu 09 Jan 2025 18:21:56
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Thu 09 Jan 2025 18:21:56

import json
from typing import List, Tuple
from aiohttp import web
from sqlalchemy import Row
from sqlalchemy.orm import Session
from utils import CustomJSONEncoder

from app.db import get_db
from app.models import Device, Position


def serialize_position_results(query_results: List[Row[Tuple[Device, Position]]]):
    results = []
    for device, position in query_results:
        results.append(
            {
                "id": position.id,
                "name": device.name,
                "time": position.time,
                "address": position.address,
                "speed": position.speed,
                "latitude": position.latitude,
                "longitude": position.longitude,
                "course": position.course,
                "altitude": position.altitude,
            }
        )
    return results


async def get_positions(request: web.Request) -> web.Response:
    _ = request
    db: Session = get_db()

    result = (
        db.query(
            Device,
            Position,
        )
        .join(Position, Device.id == Position.device_id)
        .order_by(Position.id, Position.time)
        .limit(100)
        .all()
    )

    serialized_results = serialize_position_results(result)
    text = json.dumps(serialized_results, cls=CustomJSONEncoder)

    return web.json_response(json.loads(text))
