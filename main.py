import pygame
import sys
from pygame.locals import *
from game.bird import Bird
from game.pipe import Pipe

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Flappy Bird Futuro')
        self.clock = pygame.time.Clock()
        
        # Inicializar o mixer de áudio
        pygame.mixer.init()
        
        # Cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.LIGHT_BLUE = (100, 180, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_BLUE = (0, 50, 150)
        
        # Estados do jogo
        self.current_state = 'lobby'
        
        # Inicializar backgrounds antes das configurações
        self.backgrounds = {}
        self.animated_backgrounds = {}
        self.animation_frames = {}
        self.current_frame = {}
        self.frame_delay = {}
        self.last_frame_time = {}
        
        # Lista de músicas disponíveis
        self.music_list = [
            'fight-for-the-future-336841.mp3',
            'lady-of-the-80x27s-128379.mp3',
            'platform-shoes-8-bit-chiptune-instrumental-336417.mp3'
        ]
        self.current_music_index = 0
        
        # Configurações
        self.settings = {
            'som': True,
            'volume': 0.7,
            'tela_cheia': False,
            'tema': 'claro',
            'background': 'background1',
            'personagem': 'bird',  # Adicionando personagem padrão
            'musica_atual': 0  # Índice da música atual na lista
        }
        
        # Carregar e iniciar a música de fundo
        try:
            pygame.mixer.music.load(self.music_list[self.settings['musica_atual']])
            pygame.mixer.music.set_volume(self.settings['volume'])
            pygame.mixer.music.play(-1)  # -1 significa repetir infinitamente
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
        
        # Carregar personagens
        self.characters = {}
        self.animated_characters = {}
        self.character_frames = {}
        self.character_current_frame = {}
        self.character_frame_delay = {}
        self.character_last_frame_time = {}
        
        try:
            # Lista de extensões suportadas
            supported_extensions = ['.gif', '.png', '.jpg']
            # Procurar por todos os arquivos de personagem
            import os
            character_files = os.listdir('imgs/person/')
            for file in character_files:
                name, ext = os.path.splitext(file)
                if ext.lower() not in supported_extensions:
                    continue
                
                # Primeiro tenta carregar como GIF
                if ext.lower() == '.gif':
                    path = f'imgs/person/{file}'
                    try:
                        from PIL import Image
                        gif = Image.open(path)
                        frames = []
                        
                        try:
                            while True:
                                frame = gif.convert('RGBA')
                                pygame_frame = pygame.image.fromstring(
                                    frame.tobytes(), frame.size, frame.mode
                                )
                                pygame_frame = pygame.transform.scale(
                                    pygame_frame, 
                                    (50, 50)  # Tamanho do personagem
                                )
                                frames.append(pygame_frame)
                                gif.seek(gif.tell() + 1)
                        except EOFError:
                            pass
                        
                        if frames:
                            self.animated_characters[name] = True
                            self.character_frames[name] = frames
                            self.character_current_frame[name] = 0
                            self.character_frame_delay[name] = gif.info.get('duration', 100) / 1000.0
                            self.character_last_frame_time[name] = pygame.time.get_ticks() / 1000.0
                            self.characters[name] = frames[0]
                    except Exception as e:
                        print(f"Erro ao carregar GIF do personagem {file}: {e}")
                        continue
                else:
                    # Carregar imagem estática (PNG ou JPG)
                    path = f'imgs/person/{file}'
                    try:
                        self.characters[name] = pygame.image.load(path)
                        self.characters[name] = pygame.transform.scale(
                            self.characters[name], 
                            (50, 50)  # Tamanho do personagem
                        )
                        self.animated_characters[name] = False
                    except Exception as e:
                        print(f"Erro ao carregar imagem do personagem {file}: {e}")
                        continue
        except Exception as e:
            print(f"Erro ao carregar personagens: {e}")
        
        # Garantir que pelo menos um personagem foi carregado
        if not self.characters:
            print("Erro: Nenhum personagem foi carregado!")
            pygame.quit()
            sys.exit()
        
        # Garantir que o personagem inicial existe
        if self.settings['personagem'] not in self.characters:
            self.settings['personagem'] = list(self.characters.keys())[0]

        # Carregar backgrounds
        try:
            # Lista de extensões suportadas
            supported_extensions = ['.gif', '.png', '.jpg']
            # Procurar por todos os arquivos de background
            import os
            background_files = os.listdir('imgs/backgrounds/')
            for file in background_files:
                name, ext = os.path.splitext(file)
                if ext.lower() not in supported_extensions:
                    continue
                # Primeiro tenta carregar como GIF
                if ext.lower() == '.gif':
                    path = f'imgs/backgrounds/{file}'
                    try:
                        from PIL import Image
                        gif = Image.open(path)
                        frames = []
                        try:
                            while True:
                                frame = gif.convert('RGBA')
                                pygame_frame = pygame.image.fromstring(
                                    frame.tobytes(), frame.size, frame.mode
                                )
                                pygame_frame = pygame.transform.scale(
                                    pygame_frame, 
                                    (self.screen_width, self.screen_height)
                                )
                                frames.append(pygame_frame)
                                gif.seek(gif.tell() + 1)
                        except EOFError:
                            pass
                        if frames:
                            self.animated_backgrounds[name] = True
                            self.animation_frames[name] = frames
                            self.current_frame[name] = 0
                            self.frame_delay[name] = gif.info.get('duration', 100) / 1000.0
                            self.last_frame_time[name] = pygame.time.get_ticks() / 1000.0
                            self.backgrounds[name] = frames[0]
                    except Exception as e:
                        print(f"Erro ao carregar GIF {file}: {e}")
                        continue
                else:
                    # Carregar imagem estática (PNG ou JPG)
                    path = f'imgs/backgrounds/{file}'
                    try:
                        self.backgrounds[name] = pygame.image.load(path)
                        self.backgrounds[name] = pygame.transform.scale(
                            self.backgrounds[name], 
                            (self.screen_width, self.screen_height)
                        )
                        self.animated_backgrounds[name] = False
                    except Exception as e:
                        print(f"Erro ao carregar imagem {file}: {e}")
                        continue
        except Exception as e:
            print(f"Erro ao carregar backgrounds: {e}")
            # Criar background preto como fallback
            black_surface = pygame.Surface((self.screen_width, self.screen_height))
            black_surface.fill(self.BLACK)
            self.backgrounds['background1'] = black_surface
            self.animated_backgrounds['background1'] = False

    def update_animated_background(self, bg_name):
        if not self.animated_backgrounds.get(bg_name, False):
            return self.backgrounds[bg_name]
            
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_frame_time[bg_name] > self.frame_delay[bg_name]:
            self.current_frame[bg_name] = (self.current_frame[bg_name] + 1) % len(self.animation_frames[bg_name])
            self.last_frame_time[bg_name] = current_time
            
        return self.animation_frames[bg_name][self.current_frame[bg_name]]

    def update_animated_character(self, char_name):
        if not self.animated_characters.get(char_name, False):
            return self.characters.get(char_name)
                
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.character_last_frame_time[char_name] > self.character_frame_delay[char_name]:
            self.character_current_frame[char_name] = (self.character_current_frame[char_name] + 1) % len(self.character_frames[char_name])
            self.character_last_frame_time[char_name] = current_time
                
        return self.character_frames[char_name][self.character_current_frame[char_name]]

    def run_game(self):
        # Inicializar objetos do jogo
        self.bird = Bird(100, self.screen_height // 2, self)  # Passando a referência do jogo
        self.pipes = []
        self.pipe_spawn_timer = 0
        self.score = 0
        self.game_over = False
        
        while True:
            # Desenhar o background atual
            current_bg = self.update_animated_background(self.settings['background'])
            self.screen.blit(current_bg, (0, 0))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if not self.game_over:
                            self.bird.jump()
                        else:
                            return
            
            if not self.game_over:
                # Atualizar pássaro
                self.bird.update()
                
                # Gerar novos canos
                self.pipe_spawn_timer += 1
                if self.pipe_spawn_timer > 120:  # Aumentado de 90 para 120 (2 segundos)
                    self.pipes.append(Pipe(self.screen_width, self.screen_height))
                    self.pipe_spawn_timer = 0
                
                # Atualizar e verificar colisões com canos
                for pipe in self.pipes[:]:
                    pipe.update()
                    
                    # Verificar colisão
                    if (pipe.top_pipe.collidepoint(self.bird.x, self.bird.y) or
                        pipe.bottom_pipe.collidepoint(self.bird.x, self.bird.y) or
                        self.bird.y < 0 or self.bird.y > self.screen_height):
                        self.game_over = True
                    
                    # Aumentar pontuação
                    if pipe.x + pipe.width < self.bird.x and not hasattr(pipe, 'counted'):
                        self.score += 1
                        pipe.counted = True
                    
                    # Remover canos que saíram da tela
                    if pipe.x < -pipe.width:
                        self.pipes.remove(pipe)
                
                # Desenhar elementos
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                self.bird.draw(self.screen)
                
                # Mostrar pontuação
                font = pygame.font.Font(None, 74)
                score_text = font.render(str(self.score), True, self.WHITE)
                self.screen.blit(score_text, (self.screen_width // 2, 50))
            
            else:
                # Tela de Game Over
                font = pygame.font.Font(None, 74)
                game_over_text = font.render('Game Over', True, self.WHITE)
                score_text = font.render(f'Score: {self.score}', True, self.WHITE)
                restart_text = font.render('Pressione Espaço', True, self.WHITE)
                
                self.screen.blit(game_over_text, 
                               (self.screen_width // 2 - game_over_text.get_width() // 2, 
                                self.screen_height // 2 - 100))
                self.screen.blit(score_text, 
                               (self.screen_width // 2 - score_text.get_width() // 2, 
                                self.screen_height // 2))
                self.screen.blit(restart_text, 
                               (self.screen_width // 2 - restart_text.get_width() // 2, 
                                self.screen_height // 2 + 100))
            
            pygame.display.flip()
            self.clock.tick(60)

    def run_map_selection(self):
        # Pegar apenas os backgrounds que foram carregados com sucesso
        available_maps = sorted(list(self.backgrounds.keys()))
        if not available_maps:
            return  # Retorna ao lobby se não houver mapas
            
        current_map_index = available_maps.index(self.settings['background'])
        
        while True:
            current_bg = available_maps[current_map_index]
            # Desenhar o background atual como preview
            self.screen.blit(self.backgrounds[current_bg], (0, 0))
            
            # Título
            font_title = pygame.font.Font(None, 72)
            title = font_title.render('Escolher Mapa', True, self.WHITE)
            title_rect = title.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Adicionar número total de mapas
            total_maps = len(available_maps)
            current_number = current_map_index + 1
            
            # Botões de navegação com numeração
            preview_text = f'Mapa {current_number}/{total_maps}'
            button_rect = self.draw_button(preview_text, self.screen_height // 2, True, True)
            
            # Botão Voltar
            voltar_rect = self.draw_button('Voltar', self.screen_height // 2 + 100)
            
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        current_map_index = max(0, current_map_index - 1)
                    elif event.key == K_RIGHT:
                        current_map_index = min(len(available_maps) - 1, current_map_index + 1)
                    elif event.key == K_RETURN:
                        self.settings['background'] = current_bg
                        return
                    
                if event.type == MOUSEBUTTONDOWN:
                    if isinstance(button_rect, tuple):
                        _, left_rect, right_rect = button_rect
                        if left_rect.collidepoint(mouse_pos):
                            current_map_index = max(0, current_map_index - 1)
                        elif right_rect.collidepoint(mouse_pos):
                            current_map_index = min(len(available_maps) - 1, current_map_index + 1)
                    
                    if voltar_rect.collidepoint(mouse_pos):
                        return
            
            pygame.display.flip()
            self.clock.tick(60)

    def run_lobby(self):
        buttons = [
            ('Iniciar Jogo', self.screen_height // 2 - 150),
            ('Escolher Personagem', self.screen_height // 2 - 75),
            ('Escolher Mapa', self.screen_height // 2),
            ('Configurações', self.screen_height // 2 + 75),
            ('Sair', self.screen_height // 2 + 150)
        ]
        
        while True:
            self.screen.fill(self.BLACK)
            
            # Título do jogo
            font_title = pygame.font.Font(None, 72)
            title = font_title.render('Flappy Bird Futuro', True, self.WHITE)
            title_rect = title.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(title, title_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    for button_text, y_pos in buttons:
                        button_rect = pygame.Rect(self.screen_width // 2 - 125, y_pos, 250, 50)
                        if button_rect.collidepoint(mouse_pos):
                            if button_text == 'Iniciar Jogo':
                                self.run_game()
                            elif button_text == 'Sair':
                                pygame.quit()
                                sys.exit()
                            elif button_text == 'Configurações':
                                self.run_settings()
                            elif button_text == 'Escolher Mapa':
                                self.run_map_selection()
                            elif button_text == 'Escolher Personagem':  # Adicionando este handler
                                self.run_character_selection()
            
            # Desenhar botões com efeito hover
            for button_text, y_pos in buttons:
                button_rect = pygame.Rect(self.screen_width // 2 - 125, y_pos, 250, 50)
                hovered = button_rect.collidepoint(mouse_pos)
                self.draw_button(button_text, y_pos, hovered)
            
            pygame.display.flip()
            self.clock.tick(60)

    def draw_button(self, text, y_pos, hovered=False, with_arrows=False):
        # Calcula o tamanho do texto para ajustar o botão
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, self.WHITE)
        text_width = text_surface.get_rect().width
        
        # Ajusta o tamanho do botão com base no texto (com margem extra)
        button_width = max(250, text_width + (100 if with_arrows else 40))  # Margem extra para as setas
        button_height = 50
        x = self.screen_width // 2 - button_width // 2
        
        # Sombra do botão
        shadow_rect = pygame.Rect(x + 3, y_pos + 3, button_width, button_height)
        pygame.draw.rect(self.screen, self.DARK_BLUE, shadow_rect, border_radius=10)
        
        # Corpo do botão
        button_rect = pygame.Rect(x, y_pos, button_width, button_height)
        color = self.LIGHT_BLUE if hovered else self.BLUE
        pygame.draw.rect(self.screen, color, button_rect, border_radius=10)
        
        # Borda do botão
        pygame.draw.rect(self.screen, self.WHITE, button_rect, 2, border_radius=10)
        
        # Texto do botão
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_pos + button_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Desenhar setas se necessário
        if with_arrows:
            # Seta esquerda
            left_arrow_rect = pygame.Rect(x - 30, y_pos + button_height // 4, 20, 20)
            pygame.draw.polygon(self.screen, self.WHITE, [
                (left_arrow_rect.right, left_arrow_rect.top),
                (left_arrow_rect.left, left_arrow_rect.centery),
                (left_arrow_rect.right, left_arrow_rect.bottom)
            ])
            
            # Seta direita
            right_arrow_rect = pygame.Rect(x + button_width + 10, y_pos + button_height // 4, 20, 20)
            pygame.draw.polygon(self.screen, self.WHITE, [
                (right_arrow_rect.left, right_arrow_rect.top),
                (right_arrow_rect.right, right_arrow_rect.centery),
                (right_arrow_rect.left, right_arrow_rect.bottom)
            ])
            
            return button_rect, left_arrow_rect, right_arrow_rect
        
        return button_rect

    def resize_backgrounds(self, new_width, new_height):
        # Redimensionar todos os backgrounds para a nova resolução
        for bg_name in self.backgrounds:
            if self.animated_backgrounds.get(bg_name, False):
                # Redimensionar cada frame do GIF animado
                resized_frames = []
                for frame in self.animation_frames[bg_name]:
                    resized_frame = pygame.transform.scale(frame, (new_width, new_height))
                    resized_frames.append(resized_frame)
                self.animation_frames[bg_name] = resized_frames
                self.backgrounds[bg_name] = resized_frames[0]
            else:
                # Redimensionar imagem estática
                self.backgrounds[bg_name] = pygame.transform.scale(
                    self.backgrounds[bg_name], 
                    (new_width, new_height)
                )

    def run_settings(self):
        # Lista de resoluções disponíveis
        resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1366, 768),
            (1920, 1080)
        ]
        
        # Encontrar resolução atual na lista
        current_res = (self.screen_width, self.screen_height)
        try:
            res_index = resolutions.index(current_res)
        except ValueError:
            res_index = 0
        
        # Obter nome da música atual (apenas o nome do arquivo, sem a extensão)
        current_music_name = self.music_list[self.settings['musica_atual']].split('.')[0]
        
        buttons = [
            ('Som: ' + ('Ligado' if self.settings['som'] else 'Desligado'), self.screen_height // 2 - 175),
            ('Volume: ' + str(int(self.settings['volume'] * 100)) + '%', self.screen_height // 2 - 125),
            ('Música: ' + current_music_name, self.screen_height // 2 - 75),
            ('Resolução: ' + f'{resolutions[res_index][0]}x{resolutions[res_index][1]}', self.screen_height // 2 - 25),
            ('Tela Cheia: ' + ('Sim' if self.settings['tela_cheia'] else 'Não'), self.screen_height // 2 + 25),
            ('Voltar', self.screen_height // 2 + 75)
        ]
        
        while True:
            self.screen.fill(self.BLACK)
            
            # Título
            font_title = pygame.font.Font(None, 72)
            title = font_title.render('Configurações', True, self.WHITE)
            title_rect = title.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(title, title_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    for i, (button_text, y_pos) in enumerate(buttons):
                        button_rect = pygame.Rect(self.screen_width // 2 - 125, y_pos, 250, 50)
                        if button_rect.collidepoint(mouse_pos):
                            if 'Som:' in button_text:
                                self.settings['som'] = not self.settings['som']
                                if self.settings['som']:
                                    pygame.mixer.music.unpause()
                                else:
                                    pygame.mixer.music.pause()
                            elif 'Volume:' in button_text:
                                self.settings['volume'] = min(1.0, self.settings['volume'] + 0.1)
                                if self.settings['volume'] > 0.9:
                                    self.settings['volume'] = 0.1
                                pygame.mixer.music.set_volume(self.settings['volume'])
                            elif 'Música:' in button_text:
                                # Mudar para a próxima música
                                new_music = self.change_music(next=True)
                                current_music_name = new_music.split('.')[0]
                            elif 'Resolução:' in button_text:
                                res_index = (res_index + 1) % len(resolutions)
                                new_width, new_height = resolutions[res_index]
                                if not self.settings['tela_cheia']:
                                    self.screen_width = new_width
                                    self.screen_height = new_height
                                    pygame.display.set_mode((new_width, new_height))
                                    # Redimensionar todos os backgrounds para a nova resolução
                                    self.resize_backgrounds(new_width, new_height)
                            elif 'Tela Cheia:' in button_text:
                                self.settings['tela_cheia'] = not self.settings['tela_cheia']
                                if self.settings['tela_cheia']:
                                    # Em tela cheia, usar a resolução do monitor
                                    info = pygame.display.Info()
                                    self.screen_width = info.current_w
                                    self.screen_height = info.current_h
                                    pygame.display.set_mode((self.screen_width, self.screen_height), FULLSCREEN)
                                    # Redimensionar backgrounds para resolução da tela cheia
                                    self.resize_backgrounds(self.screen_width, self.screen_height)
                                else:
                                    # Voltar para a resolução anterior
                                    self.screen_width, self.screen_height = resolutions[res_index]
                                    pygame.display.set_mode((self.screen_width, self.screen_height))
                                    # Redimensionar backgrounds para a resolução normal
                                    self.resize_backgrounds(self.screen_width, self.screen_height)
                            elif 'Voltar' in button_text:
                                return
            
            # Atualizar textos dos botões
            current_music_name = self.music_list[self.settings['musica_atual']].split('.')[0]
            buttons = [
                ('Som: ' + ('Ligado' if self.settings['som'] else 'Desligado'), self.screen_height // 2 - 175),
                ('Volume: ' + str(int(self.settings['volume'] * 100)) + '%', self.screen_height // 2 - 125),
                ('Música: ' + current_music_name, self.screen_height // 2 - 75),
                ('Resolução: ' + f'{resolutions[res_index][0]}x{resolutions[res_index][1]}', self.screen_height // 2 - 25),
                ('Tela Cheia: ' + ('Sim' if self.settings['tela_cheia'] else 'Não'), self.screen_height // 2 + 25),
                ('Voltar', self.screen_height // 2 + 75)
            ]
            
            # Desenhar botões com efeito hover
            for button_text, y_pos in buttons:
                button_rect = pygame.Rect(self.screen_width // 2 - 125, y_pos, 250, 50)
                hovered = button_rect.collidepoint(mouse_pos)
                self.draw_button(button_text, y_pos, hovered)
            
            pygame.display.flip()
            self.clock.tick(60)

    def run_character_selection(self):
        # Pegar apenas os personagens que foram carregados com sucesso
        available_chars = sorted(list(self.characters.keys()))
        if not available_chars:
            return  # Retorna ao lobby se não houver personagens
            
        current_char_index = available_chars.index(self.settings['personagem'])
        
        while True:
            self.screen.fill(self.BLACK)
            current_char = available_chars[current_char_index]
            
            # Título
            font_title = pygame.font.Font(None, 72)
            title = font_title.render('Escolher Personagem', True, self.WHITE)
            title_rect = title.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Mostrar preview do personagem
            current_char_img = self.characters[current_char]
            # Aumentar o tamanho do preview
            preview_size = (150, 150)
            preview_img = pygame.transform.scale(current_char_img, preview_size)
            preview_rect = preview_img.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
            self.screen.blit(preview_img, preview_rect)
            
            # Adicionar número total de personagens
            total_chars = len(available_chars)
            current_number = current_char_index + 1
            
            # Botões de navegação com numeração
            preview_text = f'Personagem {current_number}/{total_chars}'
            button_rect = self.draw_button(preview_text, self.screen_height // 2 + 100, True, True)
            
            # Botão Voltar
            voltar_rect = self.draw_button('Voltar', self.screen_height // 2 + 200)
            
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        current_char_index = (current_char_index - 1) % total_chars
                    elif event.key == K_RIGHT:
                        current_char_index = (current_char_index + 1) % total_chars
                    elif event.key == K_RETURN:
                        self.settings['personagem'] = current_char
                        return
                    
                if event.type == MOUSEBUTTONDOWN:
                    if isinstance(button_rect, tuple):
                        _, left_rect, right_rect = button_rect
                        if left_rect.collidepoint(mouse_pos):
                            current_char_index = (current_char_index - 1) % total_chars
                        elif right_rect.collidepoint(mouse_pos):
                            current_char_index = (current_char_index + 1) % total_chars
                    
                    if voltar_rect.collidepoint(mouse_pos):
                        return
            
            pygame.display.flip()
            self.clock.tick(60)

    def change_music(self, next=True):
        """Alterna para a próxima música ou a anterior na lista"""
        if next:
            self.settings['musica_atual'] = (self.settings['musica_atual'] + 1) % len(self.music_list)
        else:
            self.settings['musica_atual'] = (self.settings['musica_atual'] - 1) % len(self.music_list)
            
        try:
            pygame.mixer.music.load(self.music_list[self.settings['musica_atual']])
            pygame.mixer.music.set_volume(self.settings['volume'])
            pygame.mixer.music.play(-1)  # -1 significa repetir infinitamente
            return self.music_list[self.settings['musica_atual']]
        except Exception as e:
            print(f"Erro ao mudar música: {e}")
            return "Erro ao carregar música"

if __name__ == '__main__':
    game = Game()
    game.run_lobby()

    
    