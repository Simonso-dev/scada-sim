from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusDeviceContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSparseDataBlock
import logging

class CustomBlock(ModbusSparseDataBlock):
    def setValues(self, address, values):
        super().setValues(address, values)
        log.warning(f"Client wrote {values} at address {address}")

# Enable logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Simulate coils: coil 0 = fan and coil 1 = pump
store = ModbusDeviceContext(
    co=CustomBlock({0: False, 1: True}),
    hr=CustomBlock({0: 25, 1: 25, 2: 25})
)

# log.debug(msg=store)

context = ModbusServerContext(devices=store, single=True)

StartTcpServer(context, address=("172.25.213.130", 5020))