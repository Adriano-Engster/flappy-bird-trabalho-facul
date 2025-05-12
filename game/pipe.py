import pygame
import random

class Pipe:
    def __init__(self, x, screen_height):
        self.x = x
        self.width = 70
        self.gap = 200  # Mantendo o mesmo tamanho do gap
        self.speed = 3
        
        # Altura aleatória para o gap
        self.gap_y = random.randint(150, screen_height - 150 - self.gap)  # Ajustado para ter mais espaço nas bordas
        
        # Retângulos para os canos
        self.top_pipe = pygame.Rect(x, 0, self.width, self.gap_y)
        self.bottom_pipe = pygame.Rect(x, self.gap_y + self.gap, 
                                     self.width, screen_height)
        
    def update(self):
        self.x -= self.speed
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.top_pipe)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom_pipe)