import pygame
import random

def create_city_background(screen_width, screen_height):
    """Cria um fundo de cidade com silhuetas de prédios distantes"""
    surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    # Cor do céu (gradiente)
    for y in range(screen_height):
        # Criar um gradiente de cor do céu (mais escuro no topo, mais claro embaixo)
        color_value = 20 + int(y / screen_height * 60)
        color = (color_value // 2, color_value, color_value * 2, 100)
        pygame.draw.line(surface, color, (0, y), (screen_width, y))
    
    # Desenhar silhuetas de prédios distantes
    num_buildings = screen_width // 30
    for i in range(num_buildings):
        x = i * 30
        height = random.randint(50, 150)
        width = random.randint(20, 40)
        y = screen_height - height
        
        # Cor mais escura para prédios distantes
        building_color = (10, 10, 30, 150)
        pygame.draw.rect(surface, building_color, (x, y, width, height))
        
        # Adicionar algumas janelas
        window_color = (255, 255, 150, 50)
        window_size = 3
        for wx in range(x + 5, x + width - 5, 7):
            for wy in range(y + 10, y + height - 10, 10):
                if random.random() > 0.5:
                    pygame.draw.rect(surface, window_color, (wx, wy, window_size, window_size))
    
    return surface