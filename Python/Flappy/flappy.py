from kivy.app import App
from kivy.uix.widget import Widget


class FlappyGame(Widget):
    pass


class FlappyApp(App):
    def build(self):
        return FlappyGame()


if __name__ == '__main__':
    PongApp().run()