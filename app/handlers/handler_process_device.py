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
#  Created At: Wed 08 Jan 2025 09:52:10
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Wed 08 Jan 2025 09:52:10

from datetime import datetime
from typing import Any, Dict

from app import Cached, Step, app_logger, parse_date_time
from app.db import get_db
from app.handlers.htypes import DeviceInput
from app.model_schemas import DeviceSchema
from app.models import Device


class HandlerProcessDevice(Step[Dict[str, Any], DeviceInput | None]):
    def __init__(self, cache: Cached) -> None:
        super().__init__(cache)

    async def process(self, input_data: Dict[str, Any]) -> DeviceInput | None:
        source_data = input_data
        moved_at: datetime = parse_date_time(
            source_data["device_data"]["traccar"]["moved_at"], "%Y-%m-%d %H:%M:%S"
        )
        stoped_at: datetime = parse_date_time(
            source_data["device_data"]["traccar"]["stoped_at"], "%Y-%m-%d %H:%M:%S"
        )

        cur_device: Device
        new_object = Device(
            name=source_data["name"],
            unique_id=source_data["device_data"]["imei"],
            time=parse_date_time(source_data["time"]),
            moved_at=moved_at,
            stoped_at=stoped_at,
        )

        try:
            _device = self.get_device_cache(f'{new_object.unique_id}')
            if _device is not None and _device["time"] is not None:
                if parse_date_time(
                    source_data["time"]
                ).astimezone() > datetime.fromisoformat(_device["time"]):
                    pass
                else:
                    return None
            print(_device)
        except Exception as e:
            app_logger.error(f'Error retrieving cached object == {e}')

        app_logger.info(
            f'Processing input for {new_object.name} | ({new_object.unique_id}) position data...'
        )

        with get_db() as db:
            cur_device = (
                db.query(Device).filter_by(unique_id=new_object.unique_id).first()
            )

            if cur_device is None:
                db.add(new_object)
                app_logger.info(f'Created {new_object.unique_id} as new device')
                db.commit()
            elif cur_device.time is not new_object.time:
                cur_device.name = new_object.name
                cur_device.time = new_object.time
                db.commit()
                new_object = cur_device

            device_object: Dict[str, Any] | Any = DeviceSchema().dump(new_object)
            db.close()

            return {
                "Source": source_data,
                "Device": device_object,
            }
