from abc import *;

class Monster(metaclass=ABCMeta):
    @abstractmethod
    def move(self, deltaTime):
        pass;
    
    @abstractmethod
    def draw(self, screen):
        pass;

    @abstractmethod
    def offScreen(self):
        pass;