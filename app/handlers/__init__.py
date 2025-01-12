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
#  Created At: Wed 08 Jan 2025 09:30:04
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Wed 08 Jan 2025 09:30:04

import asyncio
from typing import Any, Dict, List

from app import Cached, Pipeline
from app.handlers.handler_device_status import HandlerDeviceStatus
from app.handlers.handler_process_position import HandlerProcessPosition

from .handler_process_device import HandlerProcessDevice
from .handler_validator import HandlerValidateDevice


class LocationRequestHandler:
    pipeline: Pipeline
    input_data: List[Dict[str, Any]]
    cache: Cached

    def __init__(self, input_data: List[Dict[str, Any]]):
        pipeline = Pipeline()
        self.cache = Cached()
        pipeline.add_step(HandlerValidateDevice(self.cache))
        pipeline.add_step(HandlerProcessDevice(self.cache))
        pipeline.add_step(HandlerDeviceStatus(self.cache))
        pipeline.add_step(HandlerProcessPosition(self.cache))

        self.pipeline = pipeline
        self.input_data = input_data

    async def initAsync(self):
        tasks = [self.pipeline.run(i) for i in self.input_data]
        await asyncio.gather(*tasks)
        self.cache.close()
