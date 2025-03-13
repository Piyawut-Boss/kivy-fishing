from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image

class MenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (300, 80)
        self.font_size = '30sp'
        self.background_normal = ''
        self.background_color = (0.2, 0.6, 1, 0.8)  # Ocean blue
        
        # Hover effect
        self.bind(on_press=self.on_hover_enter)
        self.bind(on_release=self.on_hover_leave)

    def on_hover_enter(self, *args):
        self.background_color = (0.3, 0.7, 1, 1)
        
    def on_hover_leave(self, *args):
        self.background_color = (0.2, 0.6, 1, 0.8)

class AboutPopup(Popup):
    def __init__(self):
        super().__init__()
        self.title = 'About The Game'
        self.size_hint = (0.6, 0.6)
        self.content = Label(text='Deep Sea Fishing Game\n6710110169\n6710110257\n6710110264\nPress spacebar to fish!')

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # ✅ พื้นหลังแบบเต็มหน้าจอ (ปรับอัตโนมัติ)
        background = Image(
            source='images/background.png', 
            allow_stretch=True, 
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(background)

        # 🎣 ชื่อเกม
        title = Label(
            text='Deep Sea\nFishing',
            font_size=100,
            bold=True,
            color=(1, 0.8, 0, 1),  # Gold
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            halign='center'
        )

        # 🎮 ปุ่มเมนู
        start_btn = MenuButton(text='Start Fishing', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        start_btn.bind(on_release=self.start_game)

        about_btn = MenuButton(text='About', pos_hint={'center_x': 0.5, 'center_y': 0.35})
        about_btn.bind(on_release=self.show_about)

        exit_btn = MenuButton(text='Exit', pos_hint={'center_x': 0.5, 'center_y': 0.2})
        exit_btn.bind(on_release=self.exit_game)

        # ✅ จัดลำดับการวาง Widget ให้พื้นหลังอยู่ด้านหลัง
        layout.add_widget(title)
        layout.add_widget(start_btn)
        layout.add_widget(about_btn)
        layout.add_widget(exit_btn)

        self.add_widget(layout)

    def start_game(self, *args):
        self.manager.current = 'game'

    def show_about(self, *args):
        AboutPopup().open()

    def exit_game(self, *args):
        from kivy.app import App
        App.get_running_app().stop()
