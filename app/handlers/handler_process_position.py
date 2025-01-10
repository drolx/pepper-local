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
#  Created At: Wed 08 Jan 2025 09:52:27
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Wed 08 Jan 2025 09:52:27

from datetime import datetime
from typing import Any, Dict

from app import Cached, Step, app_logger, parse_date_time
from app.db import get_db
from app.model_schemas import PositionSchema
from app.models import Device, Position

from .htypes import DeviceInput, PositionInput


class HandlerProcessPosition(Step[DeviceInput, PositionInput | None]):
    async def process(self, input_data: DeviceInput) -> PositionInput | None:
        device: Dict[str, Any] = input_data["Device"]
        f_data: Dict[str, Any] = input_data["Source"]

        _device: Dict[str, Any] | None
        position = Position(
            time=parse_date_time(f_data["time"]),
            speed=f_data["speed"],
            latitude=f_data["lat"],
            longitude=f_data["lng"],
            course=f_data.get("course", 0),
            altitude=f_data.get("altitude", 0),
            address=f_data.get("address", ""),
            protocol=f_data["device_data"]["traccar"].get("protocol", "osmand"),
        )

        try:
            _device = Cached().get(f"device-{device['unique_id']}", Dict[str, Any])
            if _device is not None:
                if _device["moved_at"] is not None and parse_date_time(
                    f_data["device_data"]["traccar"]["moved_at"], "%Y-%m-%d %H:%M:%S"
                ).astimezone() > datetime.fromisoformat(_device["moved_at"]):
                    pass
                else:
                    return None
        except Exception as e:
            app_logger.error(f"Error using cached device for processing position - {e}")

        app_logger.info(
            f'processing position for {device["unique_id"]} | ({position.latitude}, {position.longitude}) | {position.protocol}'
        )

        with get_db() as db:
            ref_device: Device = (
                db.query(Device).filter_by(unique_id=device["unique_id"]).first()
            )

            # Halt if no device exist
            if ref_device is not None:
                # Cancel pipeline execution if new position time is greater than previous
                old_position = (
                    db.query(Position)
                    .filter(
                        Position.time < position.time,
                        Position.device_id == device["id"],
                    )
                    .first()
                )
                if old_position is None and device["position_id"] is not None:
                    return None
                else:
                    position.device_id = ref_device.id
                    db.add(position)
                    db.commit()

                    ref_device.position_id = position.id
                    db.commit()

                position_object: Dict[str, Any] | Any = PositionSchema().dump(position)
                result: PositionInput = {
                    "Position": position_object,
                    "Device": device,
                }

                return result

            db.close()

            return None
