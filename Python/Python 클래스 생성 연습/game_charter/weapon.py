from abc import ABC, abstractmethod

class Weapon(ABC):
    def __init__(self, name, equip_class):
        self.name = name
        self.equip_class = equip_class
    
    @abstractmethod
    def weapon_skill():
        pass

class Sword(Weapon):
    def weapon_skill(self):
        print("반격 스킬 사용")

class Staff(Weapon):
    def weapon_skill(self):
        print("마나 회복 스킬 사용")
    