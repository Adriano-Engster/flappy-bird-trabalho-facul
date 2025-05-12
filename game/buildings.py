import pygame
import random

def create_building_silhouette(width, height, windows=True):
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

def create_building_top(width, height):
    """Cria o topo de um prédio com detalhes"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Cor base do topo
    top_color = (40, 40, 50, 220)
    
    # Desenhar a base do topo
    pygame.draw.rect(surface, top_color, (0, 0, width, height))
    
    # Adicionar detalhes ao topo (antenas, torres, etc)
    detail_color = (60, 60, 70, 240)
    
    # Tipo de topo aleatório
    top_type = random.randint(0, 3)
    
    if top_type == 0:  # Antena central
        antenna_width = max(4, width // 10)
        antenna_height = height // 2
        pygame.draw.rect(surface, detail_color, 
                        (width // 2 - antenna_width // 2, 0, 
                         antenna_width, antenna_height))
    
    elif top_type == 1:  # Várias antenas pequenas
        num_antennas = random.randint(2, 5)
        antenna_width = max(2, width // 20)
        for i in range(num_antennas):
            x_pos = width * (i + 1) // (num_antennas + 1) - antenna_width // 2
            antenna_height = random.randint(height // 4, height // 2)
            pygame.draw.rect(surface, detail_color, 
                            (x_pos, 0, antenna_width, antenna_height))
    
    elif top_type == 2:  # Topo arredondado
        pygame.draw.ellipse(surface, detail_color, 
                           (width // 4, height // 3, width // 2, height // 2))
    
    else:  # Topo plano com borda
        border_size = max(2, height // 10)
        pygame.draw.rect(surface, detail_color, 
                        (0, 0, width, border_size))
    
    return surface