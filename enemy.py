import pygame
import math

class Enemy:
    def __init__(self, x, y, width, height, vel=5, color=(0,0,255), movement_type='linear', **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color
        self.movement_type = movement_type
        self.right = True

        self.image = pygame.image.load('ball.png')
        self.image = pygame.transform.scale(self.image, ((width+2)*2, (height+2)*2))
        
        if(self.movement_type == 'linearx' or self.movement_type == 'lineary'):
            self.b1 = kwargs.get('b1')
            self.b2 = kwargs.get('b2')

        if self.movement_type == 'circle':
            self.radius = kwargs.get('radius', 50)
            self.angle = kwargs.get('angle', 0)
            self.center_x = x
            self.center_y = y
            self.angle_vel = kwargs.get('angle_vel', 0.1)

        if self.movement_type == 'pattern':
            self.pattern = kwargs.get('pattern', [(x, y)])
            self.current_target = 0

    def draw(self, screen):
        #pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.width+2, self.height+2)
        return screen.blit(self.image, (self.x - self.width - 2, self.y - self.height - 2))

    def move(self, bound_x1=None, bound_x2=None):
        if self.movement_type == 'linearx':
            self.move_linearx(bound_x1, bound_x2)
        elif self.movement_type == 'lineary':
            self.move_lineary(bound_x1, bound_x2)
        elif self.movement_type == 'circle':
            self.move_circle()
        elif self.movement_type == 'pattern':
            self.move_pattern()

    def move_linearx(self, bound_x1, bound_x2):
        if bound_x1 is None or bound_x2 is None:
            return
        if self.x + self.width < bound_x1 or self.x + self.vel - self.width> bound_x2:
            self.right = not self.right
        if self.right:
            self.x += self.vel
        else:
            self.x -= self.vel

    def move_lineary(self, bound_y1, bound_y2):
        if bound_y1 is None or bound_y2 is None:
            return
        if self.y + self.height < bound_y1 or self.y + self.vel - self.height> bound_y2:
            self.right = not self.right
        if self.right:
            self.y += self.vel
        else:
            self.y -= self.vel

    def move_circle(self):
        self.angle += self.vel
        angle_radians = math.radians(self.angle % 360)  
        self.x = self.center_x + int(self.radius * math.cos(angle_radians))
        self.y = self.center_y + int(self.radius * math.sin(angle_radians))

    def move_pattern(self):
        if self.pattern:
            target_x, target_y = self.pattern[self.current_target]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist < self.vel:
                self.x, self.y = target_x, target_y
                self.current_target = (self.current_target + 1) % len(self.pattern)
            else:
                self.x += self.vel * dx / dist
                self.y += self.vel * dy / dist
