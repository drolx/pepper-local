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
from typing import Any, Dict, Union

from app import Cached, Step, app_logger, fetch_location_address, parse_date_time
from app.db import get_db
from app.model_schemas import PositionSchema
from app.models import Device, Position

from .htypes import DeviceInput, PositionInput


class HandlerProcessPosition(Step[DeviceInput, Union[PositionInput, None]]):
    def __init__(self, cache: Cached) -> None:
        super().__init__(cache)

    async def process(self, input_data: DeviceInput) -> Union[PositionInput, None]:
        device: Dict[str, Any] = input_data["Device"]
        source: Dict[str, Any] = input_data["Source"]
        _device: Union[Dict[str, Any], None]

        try:
            _device = self.get_device_cache(device["unique_id"])
            if _device is not None:
                if _device["moved_at"] is not None and parse_date_time(
                    source["device_data"]["traccar"]["moved_at"], "%Y-%m-%d %H:%M:%S"
                ).astimezone() > datetime.fromisoformat(_device["moved_at"]):
                    pass
                elif _device["moved_at"] is not None and parse_date_time(
                    source["device_data"]["traccar"]["moved_at"], "%Y-%m-%d %H:%M:%S"
                ).astimezone() == datetime.fromisoformat(_device["moved_at"]):
                    self.update_device_cache(device)

                    return None
        except Exception as e:
            app_logger.error(f"Error using cached device for processing position - {e}")

        with get_db() as db:
            position = Position(
                time=parse_date_time(
                    source["device_data"]["traccar"]["time"], "%Y-%m-%d %H:%M:%S"
                ).astimezone(),
                speed=source["speed"],
                latitude=source["lat"],
                longitude=source["lng"],
                course=source.get("course", 0),
                altitude=source.get("altitude", 0),
                protocol=source["device_data"]["traccar"].get("protocol", "osmand"),
            )

            app_logger.debug(
                f'processing position for {device["unique_id"]} | ({position.latitude}, {position.longitude}) | {position.protocol}'
            )

            # Halt if no device exist
            if device is not None:
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
                    position.device_id = device["id"]
                    try:
                        address: Union[str, None] = await fetch_location_address(
                            position.latitude, position.longitude
                        )
                        if address is not None:
                            position.address = address
                    except Exception as e:
                        app_logger.error(f"Error resolving coordinate address - {e}")

                    db.add(position)
                    db.commit()

                    device_state = (
                        db.query(Device)
                        .filter_by(unique_id=device["unique_id"])
                        .first()
                    )

                    try:
                        if device_state is not None:
                            device_state.position_id = position.id
                            db.commit()
                            self.update_device_cache(device)
                    except Exception as e:
                        app_logger.error(f"Error updating device - {e}")

                position_object: Union[Dict[str, Any], Any] = PositionSchema().dump(position)
                result: PositionInput = {
                    "Position": position_object,
                    "Device": device,
                }

                db.close()

                return result
