from abc import ABC, abstractmethod

class Protocol(ABC):
    @abstractmethod
    def communication_start(self):
        pass

class WiFiProtocol(Protocol):
    def communication_start(self):
        print("WiFi로 연결을 시도합니다.")

class ZigbeeProtocol(Protocol):
    def communication_start(self):
        print("Zigbee망을 구성합니다.")

class BluetoothProtocol(Protocol):
    def communication_start(self):
        print("Bluetooth로 연결을 시도합니다.")
