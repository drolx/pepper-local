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
#  Created At: Thu 09 Jan 2025 18:16:31
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Thu 09 Jan 2025 18:16:31


from aiohttp import web
from routes.objects import get_recent_status
from routes.positions import get_positions
from aiohttp_swagger3 import (
    RapiDocUiSettings,
    SwaggerDocs,
    SwaggerInfo,
    SwaggerLicense,
    SwaggerContact,
)


def setup_routes(app: web.Application):
    swagger = SwaggerDocs(
        app,
        validate=False,
        rapidoc_ui_settings=RapiDocUiSettings(
            path="/", bg_color="#ffffff", text_color="#7f7f7f"
        ),
        info=SwaggerInfo(
            title="Pepper Local",
            version="1.0.0",
            license=SwaggerLicense(
                name="drolx Source License",
                url="https://drolx.com/licenses/source-license-1.0",
            ),
            contact=SwaggerContact(
                name="drolx Labs",
                email="dev@drolx.com",
                url="https://drolx.com",
            ),
            description="A simplefied API to interface with any telematics service",
        ),
        # components="components.yaml",
    )

    swagger.add_get("/api/objects", get_recent_status, allow_head=False)
    swagger.add_get("/api/positions", get_positions, allow_head=False)
