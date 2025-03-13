from kivy.core.audio import SoundLoader

class SoundManager:
    def __init__(self):
        # โหลดเสียงพื้นหลัง
        self.background_music = SoundLoader.load("sound/game-music-loop-7-145285.mp3")
        if self.background_music:
            self.background_music.loop = True  # เล่นซ้ำ
            self.background_music.volume = 0.25  # ปรับเสียง

        # โหลดเสียงเมื่อจับปลาได้
        self.fish_catch_sound = SoundLoader.load("sound/zapsplat_multimedia_game_sound_finish_complete_success_bright_warm_synth_004_60691.mp3")
        if self.fish_catch_sound:
            self.fish_catch_sound.volume = 0.25  # ตั้งค่าเสียงเริ่มต้น

    def play_music(self):
        if self.background_music and self.background_music.state != 'play':
            self.background_music.play()

    def stop_music(self):
        if self.background_music:
            self.background_music.stop()

    def play_fish_catch_sound(self):
        """ เล่นเสียงเมื่อจับปลาได้ """
        if self.fish_catch_sound:
            self.fish_catch_sound.play()