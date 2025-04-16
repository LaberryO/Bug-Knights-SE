from ..System.PathLoader import imageLoader;
from ..System.ImageEditor import rescale;
from .Monster import Monster;

# 파리 (몬스터)
class MobFly(Monster):
    # 초기값 설정
    def __init__(self):
        super().__init__();

        # Image
        self.image = [
            rescale(imageLoader("mobFly_0.png"), self.size),
            rescale(imageLoader("mobFly_1.png"), self.size)
        ];
    
    def move(self, deltaTime):
        self.dy += self.accSpeed;
        self.y += self.dy * deltaTime;

        super().move(deltaTime);
    
    def draw(self, screen):
        super().draw(screen);
    
    def offScreen(self):
        return super().offScreen();

    def takeHit(self, bullets):
        return super().takeHit(bullets);
