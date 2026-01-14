class Charter:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        self.weapon_equip = ""
        print(f"{self.name} 탄생!")
    def attack_action(self):
        if self.weapon_equip:
            print("1. attack, 2. first_skill, 3. second_skill")
            print("사용할 행동을 입력해주세요 : ")
            action = input()
            if action in ["attack", "first_skill", "second_skill"]:
                result = getattr(self.job, action)
                print(f"{self.name}가 {result}")
            else:
                print("행동 입력에 실패하였습니다.")
        else:
            print("장착한 무기가 없습니다!")
    def weapon_skill(self):
        if self.weapon_equip:
            self.weapon_equip.weapon_skill()
        else:
            print("장착한 무기가 없습니다!")
    def weapon_equipment(self, weapon):
        if self.job.job_class in weapon.equip_class:
            self.weapon_equip = weapon
            print("무기를 장착했습니다.")
        else:
            print("직업군에 맞지 않는 무기 타입입니다.")


