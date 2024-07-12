import pygame

class Food:
    def __init__(self, x, y, radius=5, color=(255, 255, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)
        self.image = pygame.image.load('food1.png')
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))

    def draw(self, screen):
        return screen.blit(self.image, (self.x, self.y))
