class Settings:
    def __init__(self):
        self.theme = 'default'
        self.sound_enabled = True
        self.music_volume = 1.0
        self.sfx_volume = 1.0
        self.fullscreen = False
        
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))