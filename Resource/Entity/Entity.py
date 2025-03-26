from abc import *;

class Entity(metaclass=ABCMeta):
    @abstractmethod
    def move(self, deltaTime):
        pass;
    
    @abstractmethod
    def draw(self, screen):
        pass;