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
#  Created At: Thu 09 Jan 2025 10:07:39
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Thu 09 Jan 2025 10:07:39

from aiohttp import web

from app import Cached, global_event_loop
from app.db import init_db
from app.routes import setup_routes
from app.tasks import periodic_fetch


def init(app: web.Application) -> web.Application:
    setup_routes(app)

    return app


def main():
    global_event_loop.create_task(init_db())
    global_event_loop.create_task(periodic_fetch())

    app = init(web.Application())

    web.run_app(app, loop=global_event_loop)

    # handler = app.make_handler()
    # f = global_event_loop.create_server(handler, "0.0.0.0", 8080)
    # srv = global_event_loop.run_until_complete(f)
    # try:
    #     global_event_loop.run_forever()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     global_event_loop.run_until_complete(handler.shutdown())
    #     srv.close()
    #     global_event_loop.run_until_complete(srv.wait_closed())
    #     global_event_loop.run_until_complete(app.shutdown())
    #     global_event_loop.close()
