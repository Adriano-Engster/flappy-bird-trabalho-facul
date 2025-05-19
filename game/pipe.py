import pygame
import random

class Pipe:
    def __init__(self, x, screen_height, gap_size=200):
        self.x = x
        self.screen_height = screen_height
        self.gap_size = gap_size
        self.gap_y = random.randint(150, screen_height - 150 - gap_size)  # Posição mais favorável
        self.width = random.randint(60, 100)  # Largura variável para os prédios
        self.speed = 3  # Velocidade padrão
        self.passed = False
        
        # Criar prédios (superior e inferior)
        self.top_height = self.gap_y
        self.bottom_height = screen_height - (self.gap_y + gap_size)
        
        # Criar o prédio superior (de cabeça para baixo)
        self.top_building = self.create_building_silhouette(self.width, self.top_height)
        self.top_building = pygame.transform.flip(self.top_building, False, True)
        
        # Criar o prédio inferior
        self.bottom_building = self.create_building_silhouette(self.width, self.bottom_height)
        
        # Criar retângulos para colisão
        self.top_rect = pygame.Rect(x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(x, self.gap_y + gap_size, self.width, self.bottom_height)
    
    def create_building_silhouette(self, width, height, windows=True):
        """Cria uma silhueta de prédio com janelas opcionais"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Cor do prédio (silhueta escura)
        building_color = (30, 30, 40, 200)
        
        # Desenhar o prédio
        pygame.draw.rect(surface, building_color, (0, 0, width, height))
        
        # Adicionar janelas
        if windows:
            window_color = (255, 255, 150, 100)  # Janelas amareladas
            window_size = max(5, width // 10)
            window_margin = max(3, window_size // 2)
            
            for x in range(window_margin, width - window_margin, window_size * 2):
                for y in range(window_margin, height - window_margin, window_size * 2):
                    # Algumas janelas acesas, outras apagadas
                    if random.random() > 0.3:
                        pygame.draw.rect(surface, window_color, 
                                        (x, y, window_size, window_size))
        
        return surface
    
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