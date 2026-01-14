class SmartHub:
    def __init__(self, name, protocol):
        # 딕셔너리가 어울릴 수도?
        self.device_dic = {}
        self.name = name
        self.protocol = protocol
    
    def register_device(self, device):
        # 디바이스를 입력받아서 디바이스 목록에 추가
        # 입력받은 device가 진짜 Device가 맞나?? 나중에 구현
        if type(device.protocol) == type(self.protocol):
            print("등록이 완료되었습니다.")
            self.device_dic[device.device_type] = device
        else:
            print("ERROR : 호환되지 않는 연결 방식입니다.")

    def switch_on_all(self):
        for device in self.device_dic.values():
            device.protocol.communication_start()
            device.switch_on()
    
    def switch_off_all(self):
        for device in self.device_dic.values():
            device.switch_off()
