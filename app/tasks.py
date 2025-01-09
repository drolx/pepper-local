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
#  Created At: Mon 06 Jan 2025 11:48:09
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Mon 06 Jan 2025 11:48:09


import asyncio
from typing import Any, Dict, List

from aiohttp import ClientSession, MultipartWriter

from app import Cached, app_logger, global_event_loop
from app.handlers import LocationRequestHandler
from app.settings import (
	API_BASE_URL,
	API_PASS,
	API_USER,
	FETCH_INTERVAL,
	GET_DEVICES_ENDPOINT,
	LOGIN_ENDPOINT,
)

API_PROP_KEY: str = 'user_api_hash'


async def authenticate() -> str | None:
	async with ClientSession() as session:
		request_type = 'multipart/form-data'

		multi_part_data = MultipartWriter('mixed')
		multi_part_data.append(API_USER, {'Content-Type': 'multipart/form-data'}).set_content_disposition('form-data', name='email')
		multi_part_data.append(API_PASS, {'Content-Type': 'multipart/form-data'}).set_content_disposition('form-data', name='password')

		headers: Dict[str, str] = {
			'Accept': 'application/json',
			'Content-Type': f'{request_type}; boundary={multi_part_data.boundary}',
		}

		api_key: str | None = None
		response = await session.post(f'{API_BASE_URL}{LOGIN_ENDPOINT}', data=multi_part_data, headers=headers)
		data = await response.json()

		try:
			api_key = data['user_api_hash']
			if api_key is None:
				return None

			Cached().set(API_PROP_KEY, api_key)

		except Exception as e:
			app_logger.error(f'Authentication failed for {API_USER} - {e}')

		return api_key


async def fetch_devices() -> None:
	app_logger.info('**** Starting new synchronization action...')

	async with ClientSession() as session:
		api_hash = Cached().get(API_PROP_KEY, str)
		headers = {
			'Accept': 'application/json',
		}
		response = await session.get(
			f'{API_BASE_URL}{GET_DEVICES_ENDPOINT}?lang=en&user_api_hash={api_hash}',
			headers=headers,
		)

		if response.status == 401:
			auth_retry = await authenticate()
			if auth_retry is not None:
				await fetch_devices()

		data = await response.json()

		try:
			result: List[Dict[str, Any]] = data[0]['items']
			main_sync_handler = LocationRequestHandler(result)
			await main_sync_handler.initAsync()
		except Exception as e:
			app_logger.error(f'Fetch request failed to complete - {e}')


async def periodic_fetch():
	await asyncio.sleep(FETCH_INTERVAL)

	app_logger.info('**** Starting background process....')
	while True:
		global_event_loop.create_task(fetch_devices())
		await asyncio.sleep(FETCH_INTERVAL)
