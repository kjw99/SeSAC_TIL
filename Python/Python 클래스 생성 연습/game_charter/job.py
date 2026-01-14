from abc import ABC, abstractmethod

class Job(ABC):
    def __str__(self):
        return self.job_class

    @abstractmethod
    def attack(self):
        pass
    
    @abstractmethod
    def first_skill(self):
        pass
    
    @abstractmethod
    def second_skill(self):
        pass

class Warrior(Job):
    def __init__(self):
        self.job_class = "전사"
    
    @property
    def attack(self):
        return "검을 휘두릅니다"
    
    @property
    def first_skill(self):
        return "검을 매우 강하게 휘두릅니다."
    
    @property
    def second_skill(self):
        return "앞으로 돌진합니다."

class Wizard(Job):
    def __init__(self):
        self.job_class = "마법사"

    @property
    def attack(self):
        return "마력 탄환을 발사합니다."
    
    @property
    def first_skill(self):
        return "화염구를 발사합니다."
    
    @property
    def second_skill(self):
        return "실드를 생성합니다."