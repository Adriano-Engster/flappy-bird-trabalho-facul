import pygame
import random
from game.buildings import create_building_silhouette, create_building_top

class Pipe:
    def __init__(self, x, screen_height, gap_size=200):
        self.x = x
        self.screen_height = screen_height
        self.gap_size = gap_size
        self.gap_y = random.randint(100, screen_height - 100 - gap_size)
        self.width = random.randint(60, 100)  # Largura variável para os prédios
        self.speed = 3
        self.passed = False
        
        # Criar prédios (superior e inferior)
        self.top_height = self.gap_y
        self.bottom_height = screen_height - (self.gap_y + gap_size)
        
        # Criar o prédio superior (de cabeça para baixo)
        self.top_building = create_building_silhouette(self.width, self.top_height)
        self.top_building = pygame.transform.flip(self.top_building, False, True)
        
        # Adicionar topo ao prédio superior
        top_detail_height = min(50, self.top_height // 4)
        top_detail = create_building_top(self.width, top_detail_height)
        top_detail = pygame.transform.flip(top_detail, False, True)
        self.top_building.blit(top_detail, (0, 0))
        
        # Criar o prédio inferior
        self.bottom_building = create_building_silhouette(self.width, self.bottom_height)
        
        # Adicionar topo ao prédio inferior
        bottom_detail_height = min(50, self.bottom_height // 4)
        bottom_detail = create_building_top(self.width, bottom_detail_height)
        self.bottom_building.blit(bottom_detail, (0, 0))
        
        # Criar retângulos para colisão
        self.top_rect = pygame.Rect(x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(x, self.gap_y + gap_size, self.width, self.bottom_height)
    
    def update(self):
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def draw(self, screen):
        # Desenhar o prédio superior
        screen.blit(self.top_building, (self.x, 0))
        
        # Desenhar o prédio inferior
        screen.blit(self.bottom_building, (self.x, self.gap_y + self.gap_size))
    
    def is_off_screen(self):
        return self.x + self.width < 0
    
    def check_collision(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)