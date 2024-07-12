import pygame

class Wall:
    def __init__(self, x, y, xfinal, yfinal, width=1, color=(0, 0, 0)):
        self.x1 = x
        self.y1 = y
        self.x2 = xfinal
        self.y2 = yfinal
        self.width = width
        self.color = color
        # Crear un rectángulo que cubra la línea de la pared
        if x == xfinal:
            self.rect = pygame.Rect(x - width // 2, min(y, yfinal), width, abs(yfinal - y))
        else:
            self.rect = pygame.Rect(min(x, xfinal), y - width // 2, abs(xfinal - x), width)

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), self.width)
