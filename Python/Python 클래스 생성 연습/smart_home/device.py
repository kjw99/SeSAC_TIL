from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, model, device_type, protocol):
        self.model = model
        self.device_type = device_type
        self.switch = False
        self.protocol = protocol
    @abstractmethod
    def switch_on(self):
        self.switch = True
        print(f"{self.device_type} 모델명 : {self.model}의 전원을 키겠습니다.")
    @abstractmethod
    def switch_off(self):
        self.switch = False
        print(f"{self.device_type} 모델명 : {self.model}의 전원을 끄겠습니다.")
    @abstractmethod
    def state_check(self):
        print(f"기기 타입  : {self.device_type}")
        print(f"모델 명 : {self.model}")

class AirConditioner(Device):
    temperature = 22
    def switch_on(self):
        super().switch_on()
    def switch_off(self):
        super().switch_off()
    def state_check(self):
        super().state_check()
        if self.switch:
            print("전원 : ON")
            print(f"현재 온도 : {self.temperature}")
        else:
            print("전원 : OFF")        
    def temperature_control_up(self):
        self.temperature += 1
    def temperature_control_down(self):
        self.temperature -= 1

class Light(Device):
    Brightness = 2
    def switch_on(self):
        super().switch_on()
    def switch_off(self):
        super().switch_off()
    def state_check(self):
        super().state_check()
        if self.switch:
            print("전원 : ON")
            print(f"현재 밝기 : {self.Brightness}")
        else:
            print("전원 : OFF")
    def brightness_up(self):
        self.Brightness += 1
    def brightness_down(self):
        self.Brightness -= 1