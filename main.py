import os
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

class GlitchBackground(FloatLayout):
    """Arka planda kırmızı-siyah efektler üreten katman."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(0.8, 0.05, 0.05, 1) # Ana Kırmızı
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update, pos=self._update)

    def _update(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

class CustomBorderBox(Label):
    """Özel çerçeveli metin kutuları oluşturur."""
    def __init__(self, bg_color=(0, 0, 0, 1), border_color=(1, 1, 1, 1), border_width=2, **kwargs):
        super().__init__(**kwargs)
        self.bg_color_val = bg_color
        self.border_color_val = border_color
        self.border_width_val = border_width

        with self.canvas.before:
            self.bg_color = Color(*self.bg_color_val)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.border_color = Color(*self.border_color_val)
            self.border_line = Line(rectangle=(self.x, self.y, self.width, self.height), width=self.border_width_val)

        self.bind(size=self._update_graphics, pos=self._update_graphics)

    def _update_graphics(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)

class A90RansomSimulator(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 1. ARKA PLAN
        self.bg = GlitchBackground()
        self.add_widget(self.bg)

        # 2. ÜST BAŞLIK (YOUR ITEMS HAVE BEEN ENCRYPTED)
        self.title_box = CustomBorderBox(
            bg_color=(0.85, 0.05, 0.05, 1),
            border_color=(0, 0, 0, 1),
            border_width=3,
            text="[b]YOUR ITEMS\nHAVE BEEN\nENCRYPTED[/b]",
            markup=True,
            font_size='30sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(0.95, 0.28),
            pos_hint={'center_x': 0.5, 'top': 0.98}
        )
        self.add_widget(self.title_box)

        # 3. A-90 YÜZ GÖRSELİ (Üst başlığın soluna yerleştirme simülasyonu)
        self.head_icon = Image(
            source='a90_image.png',
            size_hint=(0.25, 0.22),
            pos_hint={'x': 0.05, 'top': 0.95}
        )
        self.add_widget(self.head_icon)

        # 4. ORTA SİYAH UYARI ÇERÇEVESİ
        self.warning_box = CustomBorderBox(
            bg_color=(0, 0, 0, 1),
            border_color=(1, 1, 1, 1),
            border_width=2,
            text="[b]IF YOU DO NOT PAY THIS RANSOM BEFORE\nTHE TIMER ENDS, YOUR ITEMS WILL BE\n[color=ff2222]UNRECOVERABLE BY ANY MEANS.[/color][/b]",
            markup=True,
            font_size='15sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(0.95, 0.22),
            pos_hint={'center_x': 0.5, 'center_y': 0.52}
        )
        self.add_widget(self.warning_box)

        # 5. ALT SOL: COIN PANELDİ (500)
        self.coin_box = CustomBorderBox(
            bg_color=(0, 0, 0, 1),
            border_color=(1, 0.8, 0, 1), # Altın Çerçeve
            border_width=2,
            text="[b]500  ⬢[/b]",
            markup=True,
            font_size='28sp',
            color=(1, 0.85, 0, 1),
            size_hint=(0.38, 0.16),
            pos_hint={'x': 0.025, 'y': 0.12}
        )
        self.add_widget(self.coin_box)

        # 6. ALT SAĞ: ZAMAN SAYACI (TIME: 01:29)
        self.time_remaining = 89  # 1 Dakika 29 Saniye
        self.timer_box = CustomBorderBox(
            bg_color=(0.9, 0.1, 0.1, 1),
            border_color=(0, 0, 0, 1),
            border_width=2,
            text="[b]TIME:    01:29[/b]",
            markup=True,
            font_size='26sp',
            color=(0, 0, 0, 1),
            size_hint=(0.54, 0.16),
            pos_hint={'right': 0.975, 'y': 0.12}
        )
        self.add_widget(self.timer_box)

        # 7. EKRANDA SEKEN VE TELEPORT OLAN A-90 KAFASI
        self.bouncing_a90 = Image(
            source='a90_image.png',
            size_hint=(None, None),
            size=(160, 160),
            pos=(100, 100)
        )
        self.add_widget(self.bouncing_a90)

        # Hareket Değişkenleri
        self.velocity_x = 10
        self.velocity_y = 10
        self.teleport_timer = 0

        # 8. SES DOSYASINI YÜKLE
        self.sound_file = 'Ransom (a-90) theme roblox doors.mp3'
        self.sound = None
        self.init_sound()

        # ZAMANLAYICI DÖNGÜLERİ
        Clock.schedule_interval(self.update_timer, 1.0)
        Clock.schedule_interval(self.update_movement, 1.0 / 60.0) # 60 FPS
        Clock.schedule_interval(self.glitch_effect, 0.1) # Yanıp sönme efekti

        # KLAVYE/DOKUNMA DİNLEYİCİSİ
        Window.bind(on_keyboard=self.on_keyboard)
        self.bind(on_touch_down=self.on_screen_touch)

    def init_sound(self):
        if os.path.exists(self.sound_file):
            self.sound = SoundLoader.load(self.sound_file)
            if self.sound:
                self.sound.loop = True
                self.sound.play()

    def update_timer(self, dt):
        """Saniyede bir geri sayımı günceller."""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            mins, secs = divmod(self.time_remaining, 60)
            self.timer_box.text = f"[b]TIME:    {mins:02d}:{secs:02d}[/b]"
        else:
            self.timer_box.text = "[b]TIME EXPIRED![/b]"

    def update_movement(self, dt):
        """A-90 nesnesini ekranda sektirir ve rastgele ışınlar."""
        x, y = self.bouncing_a90.pos
        x += self.velocity_x
        y += self.velocity_y

        # Ekran Sınırları
        win_w, win_h = Window.size
        img_w, img_h = self.bouncing_a90.size

        # Duvarlara Çarpma Kontrolü
        if x <= 0 or x + img_w >= win_w:
            self.velocity_x *= -1
        if y <= 0 or y + img_h >= win_h:
            self.velocity_y *= -1

        # Rastgele Teleport / Sıçrama (A-90 Mekaniği)
        self.teleport_timer += dt
        if self.teleport_timer > 3.0: # Her 3 saniyede bir rastgele konuma sıçrar
            x = random.randint(10, max(11, int(win_w - img_w - 10)))
            y = random.randint(10, max(11, int(win_h - img_h - 10)))
            self.teleport_timer = 0

        self.bouncing_a90.pos = (x, y)

    def glitch_effect(self, dt):
        """Ekrandaki kırmızı alanların tonunu değiştirerek bozulma efekti verir."""
        if random.random() > 0.85:
            r = random.uniform(0.6, 0.95)
            self.bg.bg_color.rgb = (r, 0.02, 0.02)
        else:
            self.bg.bg_color.rgb = (0.8, 0.05, 0.05)

    def on_screen_touch(self, instance, touch):
        """Telefonda ekrana tıklandığında sanal klavyeyi açar."""
        Window.show_keyboard()

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Klavyeden 'X' veya 'x' basıldığında uygulamayı kapatır."""
        if codepoint in ['x', 'X']:
            if self.sound:
                self.sound.stop()
            App.get_running_app().stop()
            return True
        return False

class MainA90App(App):
    def build(self):
        return A90RansomSimulator()

if __name__ == '__main__':
    MainA90App().run()