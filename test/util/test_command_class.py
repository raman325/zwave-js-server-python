"""Test command class utility functions."""
import pytest

from zwave_js_server.const import (
    CC_SPECIFIC_METER_TYPE,
    CC_SPECIFIC_SCALE,
    CommandClass,
    ElectricScale,
    MeterType,
    MultilevelSensorType,
)
from zwave_js_server.exceptions import InvalidCommandClass, UnknownValueData
from zwave_js_server.model.node import Node
from zwave_js_server.model.value import MetaDataType, get_value_id, Value, ValueDataType
from zwave_js_server.util.command_class import (
    get_meter_scale_type,
    get_meter_type,
    get_multilevel_sensor_type,
)


async def test_get_meter_type(inovelli_switch: Node):
    """Test get_meter_type function."""
    node = inovelli_switch

    value_id = get_value_id(node, CommandClass.SWITCH_BINARY, "currentValue")
    with pytest.raises(InvalidCommandClass):
        get_meter_type(node.values.get(value_id))

    value_id = get_value_id(node, CommandClass.METER, "value", property_key=65537)
    assert get_meter_type(node.values.get(value_id)) == MeterType.ELECTRIC


async def test_get_invalid_meter_type(invalid_multilevel_sensor_type: Node):
    """Test receiving an invalid meter type."""
    node = invalid_multilevel_sensor_type

    # Create value with an invalid meterType ID
    metadata = MetaDataType(ccSpecific={CC_SPECIFIC_METER_TYPE: -1})
    value_data = ValueDataType(
        commandClass=CommandClass.METER,
        commandClassName="Meter",
        endpoint=0,
        property="value",
        propertyKey=9999999,
        metadata=metadata,
    )
    value = Value(node, value_data)
    with pytest.raises(UnknownValueData):
        get_meter_type(value)


async def test_get_meter_scale_type(inovelli_switch: Node):
    """Test get_meter_scale_type function."""
    node = inovelli_switch

    value_id = get_value_id(node, CommandClass.METER, "value", property_key=65537)
    assert (
        get_meter_scale_type(node.values.get(value_id)) == ElectricScale.KILOWATT_HOUR
    )


async def test_get_invalid_meter_scale_type(invalid_multilevel_sensor_type: Node):
    """Test receiving an invalid meter scale type."""
    node = invalid_multilevel_sensor_type

    # Create value with an invalid scale ID
    metadata = MetaDataType(
        ccSpecific={CC_SPECIFIC_METER_TYPE: 1, CC_SPECIFIC_SCALE: -1}
    )
    value_data = ValueDataType(
        commandClass=CommandClass.METER,
        commandClassName="Meter",
        endpoint=0,
        property="value",
        propertyKey=9999999,
        metadata=metadata,
    )
    value = Value(node, value_data)
    with pytest.raises(UnknownValueData):
        get_meter_scale_type(value)


async def test_get_multilevel_sensor_type(multisensor_6: Node):
    """Test get_multilevel_sensor_type function."""
    node = multisensor_6

    value_id = get_value_id(node, CommandClass.SENSOR_BINARY, "Any")
    with pytest.raises(InvalidCommandClass):
        get_multilevel_sensor_type(node.values.get(value_id))

    value_id = get_value_id(node, CommandClass.SENSOR_MULTILEVEL, "Air temperature")
    assert (
        get_multilevel_sensor_type(node.values.get(value_id))
        == MultilevelSensorType.AIR_TEMPERATURE
    )


async def test_get_invalid_multilevel_sensor_type(invalid_multilevel_sensor_type: Node):
    """Test receiving an invalid multilevel sensor type."""
    node = invalid_multilevel_sensor_type

    value_id = get_value_id(
        node, CommandClass.SENSOR_MULTILEVEL, "UNKNOWN (0x00)", endpoint=2
    )
    with pytest.raises(UnknownValueData):
        get_multilevel_sensor_type(node.values.get(value_id))