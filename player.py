import pygame

class Player:
    def __init__(self, x, y, width, height, vel=5, color=(255,0,0), deaths=0, checkpoints=[]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color
        self.deaths = deaths
        self.rect = pygame.Rect(x, y, width, height)
        self.checkpoints = checkpoints
        self.current_checkpoint = (x, y)
        self.food_collected = 0
        self.food_collected_at_checkpoint = 0  
        self.food_remaining_at_checkpoint = []  

        self.image = pygame.image.load('icecube1.png')
        self.image = pygame.transform.scale(self.image, (width, height))

    def move(self, keys, walls):
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.vel
        if keys[pygame.K_RIGHT]:
            dx = self.vel
        if keys[pygame.K_DOWN]:
            dy = self.vel
        if keys[pygame.K_UP]:
            dy = -self.vel

        self.rect.x += dx
        if self.check_collision(walls):
            self.rect.x -= dx

        self.rect.y += dy
        if self.check_collision(walls):
            self.rect.y -= dy

        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, screen):
        #pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        return screen.blit(self.image, (self.x, self.y))

    def reset(self, foods):
        self.x, self.y = self.current_checkpoint
        self.rect.x = self.x
        self.rect.y = self.y
        self.food_collected = self.food_collected_at_checkpoint
        return self.food_remaining_at_checkpoint[:] 

    def check_collision(self, walls):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                return True
        return False

    def update_checkpoint(self, checkpoints, foods):
        for checkpoint in checkpoints:
            if self.rect.colliderect(checkpoint.rect):
                self.current_checkpoint = (checkpoint.x + checkpoint.width // 2, checkpoint.y + checkpoint.height // 2)
                self.food_collected_at_checkpoint = self.food_collected  
                self.food_remaining_at_checkpoint = foods[:]  
                return True
        return False
