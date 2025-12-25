from kivy.app import App
from ui_kivy import MainWindow


class LeitnerApp(App):
    def build(self):
        return MainWindow()


def main():
    app = LeitnerApp()
    app.run()


if __name__ == "__main__":
    main()
