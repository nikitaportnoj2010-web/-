from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from random import uniform

from kivy_garden.webview import WebView

Window.clearcolor = (0, 0, 0, 1)

class Star:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = uniform(0, self.width)
        self.y = uniform(0, self.height)
        self.size = uniform(1, 3)
        self.speed = uniform(1, 5)

class StarsCanvas(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stars = [Star(Window.width, Window.height) for _ in range(300)]
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0)
            Rectangle(size=Window.size, pos=(0, 0))
            Color(1, 1, 1)
            for star in self.stars:
                Ellipse(pos=(star.x, star.y), size=(star.size, star.size))
                star.y -= star.speed
                star.x += star.speed / 4
                if star.y < 0 or star.x > Window.width:
                    star.reset()
                    star.y = Window.height

class NVWebApp(App):
    def build(self):
        root = FloatLayout()

        self.bg_canvas = StarsCanvas(size=Window.size)
        root.add_widget(self.bg_canvas)

        self.search_box = BoxLayout(
            orientation='horizontal',
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        self.search_input = TextInput(
            hint_text="Введите запрос или URL",
            multiline=False,
            size_hint_x=0.8
        )
        search_btn = Button(text="Поиск", size_hint_x=0.2)
        search_btn.bind(on_press=self.on_search)
        self.search_input.bind(on_text_validate=self.on_search)
        self.search_box.add_widget(self.search_input)
        self.search_box.add_widget(search_btn)
        root.add_widget(self.search_box)

        self.tabs = TabbedPanel(do_default_tab=False, size_hint=(1, 0.3), pos_hint={'x': 0, 'y': 0})
        self.add_home_tab()
        root.add_widget(self.tabs)

        return root

    def add_home_tab(self):
        tab = TabbedPanelItem(text="Home")
        box = BoxLayout(orientation='vertical')
        label = Label(
            text="Добро пожаловать в nVweb\nВведите запрос сверху",
            halign="center",
            valign="middle"
        )
        box.add_widget(label)
        tab.add_widget(box)
        self.tabs.add_widget(tab)
        self.tabs.default_tab = tab

    def add_search_tab(self, url, title):
        short_title = title if len(title) < 15 else title[:12] + "..."
        tab = TabbedPanelItem(text=short_title)
        web = WebView(url=url)
        tab.add_widget(web)
        self.tabs.add_widget(tab)
        self.tabs.switch_to(tab)

    def on_search(self, instance):
        query = self.search_input.text.strip()
        if not query:
            return

        if "." in query and " " not in query:
            url = query if query.startswith("http") else f"https://{query}"
        else:
            url = f"https://duckduckgo.com/?q={query}"

        self.add_search_tab(url, query)
        self.search_input.text = ""

if __name__ == "__main__":
    NVWebApp().run()
