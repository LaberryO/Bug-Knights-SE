from pygame.image import load;
from pygame.transform import scale;

def rescale(img, size):
    return scale(load(img), (size, size));