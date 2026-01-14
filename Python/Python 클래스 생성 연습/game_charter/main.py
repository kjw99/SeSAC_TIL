from charter import Charter
from job import Warrior, Wizard
from weapon import Sword, Staff

sword = Sword("철검", ["전사", "용사"])
staff = Staff("질 좋은 나무봉", ["마법사", "용사"])

arthur = Charter("아더", Warrior())

arthur.attack_action()
arthur.weapon_equipment(staff)
arthur.weapon_equipment(sword)
arthur.attack_action()