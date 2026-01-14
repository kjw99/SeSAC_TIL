from device import AirConditioner, Light
from smart_hub import SmartHub
from protocol import WiFiProtocol, BluetoothProtocol, ZigbeeProtocol

w_ac = AirConditioner("위니아 에어컨", "air_conditioner", ZigbeeProtocol())
p_light = Light("필립스 전등", "smart_light", WiFiProtocol())
e_light = Light("이케아 전등", "smart_light", ZigbeeProtocol())

myhub = SmartHub("샤오미 허브", ZigbeeProtocol())
myhub.register_device(w_ac)
myhub.register_device(p_light)
myhub.register_device(e_light)
myhub.switch_on_all()