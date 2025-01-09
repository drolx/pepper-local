from typing import Any, Dict

from app import Step


class HandlerValidateDevice(Step[Dict[str, Any], Dict[str, Any] | None]):
	async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any] | None:
		required_fields = [
			'name',
			'time',
			'lat',
			'course',
			'speed',
			'altitude',
			'address',
			'protocol',
			'device_data.imei',
			'device_data.traccar.moved_at',
			'device_data.traccar.stoped_at',
			'device_data.traccar.protocol',
		]

		for field in required_fields:
			keys = field.split('.')
			value = input_data
			try:
				for key in keys:
					value = value[key]
			except (KeyError, TypeError):
				return None
			if value is None:
				return None

			return input_data
