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
#  Created At: Mon 06 Jan 2025 11:47:08
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Mon 06 Jan 2025 11:47:08

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://pepper:pepper@localhost:15432/pepper')
API_BASE_URL: str = os.getenv('API_BASE_URL', '')
API_USER: str = os.getenv('API_USER', '')
API_PASS: str = os.getenv('API_PASS', '')
LOGIN_ENDPOINT: str = '/api/login'
GET_DEVICES_ENDPOINT: str = '/api/get_devices'
AUTH_INTERVAL: int = 3600
FETCH_INTERVAL: int = 30
OFFLINE_INTERVAL: int = 90
