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
#  Created At: Wed 08 Jan 2025 09:53:33
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Wed 08 Jan 2025 09:53:33

from datetime import datetime

from app import Step, settings
from app.db import get_db
from app.handlers.htypes import PositionInput
from app.models import Device, DeviceStatus


class HandlerDeviceStatus(Step[PositionInput, PositionInput | None]):
    async def process(self, input_data: PositionInput) -> PositionInput | None:
        current_time = datetime.now().astimezone()
        device = input_data["Device"]
        position = input_data["Position"]

        device_time = datetime.fromisoformat(position["time"])
        speed = position["speed"]
        status: DeviceStatus

        if (
            current_time - device_time
        ).total_seconds() > settings.OFFLINE_INTERVAL * 60:
            status = DeviceStatus.Offline
        elif speed > 3:
            status = DeviceStatus.Moving
        elif speed <= 3 and device.get("detect_engine") == "true":
            status = DeviceStatus.Idling
        else:
            status = DeviceStatus.Parked

        with get_db() as db:
            query_device = (
                db.query(Device).filter_by(unique_id=device["unique_id"]).first()
            )

            if query_device is not None:
                query_device.status = status
                db.commit()

            db.close()

        return None
