from kivy.core.audio import SoundLoader

class SoundManager:
    def __init__(self):
        self.background_music = SoundLoader.load("sound/game-music-loop-7-145285.mp3")
        
        if self.background_music:
            self.background_music.loop = True  # เล่นซ้ำ
            self.background_music.volume = 0.5  # ปรับเสียง

    def play_music(self):
        if self.background_music and not self.background_music.state == 'play':
            self.background_music.play()

    def stop_music(self):
        if self.background_music:
            self.background_music.stop()