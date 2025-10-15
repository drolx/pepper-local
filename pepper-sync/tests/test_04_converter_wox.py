from pepper.converters.wox import WoxConverter
import json
import pytest


@pytest.fixture
def instance():
    return WoxConverter()

@pytest.fixture
def data_devices():
    data: dict[str, object] = {}
    with open("test-data/wox-test-devices.json", "r") as file:
        data = json.load(file)
    return data


def test_convert_to_device_object(instance, data_devices):
    resolved_data = instance.resolve_devices(data_devices)
    assert resolved_data[0].name == "AAB 77 XD"

def test_convert_to_position_object(instance, data_devices):
    resolved_data = instance.resolve_positions(data_devices)
    assert resolved_data[0].speed == 64
    assert resolved_data[0].course == 94
    assert resolved_data[0].altitude == 0
