from ..Data.Screen import Screen;
from ..System.PathLoader import ImageLoader;
from .Monster import Monster;
import random, pygame;

# 파리 (몬스터)
class MobFly(Monster):
    # 초기값 설정
    def __init__(self):
        self.x = random.randint(0, Screen().getWidth()-32);
        self.y = -100;
        self.dy = 0.1;

        # Image
        self.image = [
            pygame.image.load(ImageLoader("mobFly_0.png")),
            pygame.image.load(ImageLoader("mobFly_1.png"))
        ];
    def move(self, deltaTime):
        self.dy += 0.15 * deltaTime;
        self.y += self.dy;
    def draw(self, screen):
        screen.blit(self.image[0], (self.x, self.y));
    def offScreen(self):
        return self.y > Screen().getHeight();