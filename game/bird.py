import pygame

class Bird:
    def __init__(self, x, y, game_instance=None):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.rect = pygame.Rect(x, y, 50, 50)  # Ajustado para o tamanho do personagem
        self.game_instance = game_instance
    
    def jump(self):
        self.velocity = self.jump_strength
    
    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        # Atualizar a posição do retângulo de colisão
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        # Verificar se temos uma referência ao jogo
        if self.game_instance:
            try:
                # Obter o personagem atual do jogo
                current_char = self.game_instance.update_animated_character(self.game_instance.settings['personagem'])
                screen.blit(current_char, (self.x, self.y))
            except Exception as e:
                # Fallback para caso de erro - usar um círculo em vez de retângulo
                print(f"Erro ao desenhar personagem: {e}")
                pygame.draw.circle(screen, (100, 100, 255), (self.x + 25, self.y + 25), 25)
        else:
            # Fallback se não tiver referência ao jogo - usar um círculo em vez de retângulo
            pygame.draw.circle(screen, (100, 100, 255), (self.x + 25, self.y + 25), 25)