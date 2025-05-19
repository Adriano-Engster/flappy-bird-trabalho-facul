import pygame

class Bird:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.velocity = 0
        self.gravity = 0.5  # Reduzido de 0.7 para tornar mais fácil
        self.jump_strength = -8  # Aumentado para facilitar o controle
    
    def update(self):
        # Aplicar gravidade
        self.velocity += self.gravity
        self.y += self.velocity
        
        # Limitar a velocidade máxima de queda
        if self.velocity > 10:
            self.velocity = 10
    
    def jump(self):
        self.velocity = self.jump_strength
    
    def draw(self, screen):
        # Obter o personagem atual (estático ou animado)
        current_character = self.game.update_animated_character(self.game.settings['personagem'])
        screen.blit(current_character, (self.x, self.y))