from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from matplotlib.figure import Figure
from kivy.base import EventLoop
from matplotlib.backends.backend_agg import FigureCanvasAgg
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import numpy as np
from controllers_kivy import LeitnerController
# ---------------- Controller (همان PyQt) ----------------


# ---------------- Main Window ----------------
class MainWindow(BoxLayout):
    controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=5, **kwargs)
        self.controller = LeitnerController(self)
        self.init_ui()

    def init_ui(self):
        # ---------- Top Buttons ----------
        buttons = BoxLayout(size_hint_y=0.1, spacing=5)
        for text, fn in [
            ("Import CSV", self.controller.import_csv),
            ("Add Item", self.controller.add_item_manually),
            ("Export CSV", self.controller.export_csv),
            ("Save Project", self.controller.save_project),
            ("Load Project", self.controller.load_project),
        ]:
            b = Button(text=text, font_size=14)
            b.bind(on_press=fn)
            buttons.add_widget(b)

        # ---------- User / Add To Box ----------
        top = BoxLayout(size_hint_y=0.1, spacing=5)
        top.add_widget(Label(text="User Name:", size_hint_x=0.12))
        self.user_edit = TextInput(text="User1", multiline=False, size_hint_x=0.2)

        self.add_to_box_btn = Button(text="Add to Box", disabled=True, size_hint_x=0.15)
        self.add_to_box_btn.bind(on_press=self.controller.add_words_to_box)

        self.combo_add_words = Spinner(
            text="10",
            values=["5", "10", "20", "50", "100", "All"],
            disabled=True,
            size_hint_x=0.12,
        )

        self.dictionary_label = Label(
            text=" No item left in dictionary ",
            size_hint_x=0.3
        )

        self.start_btn = Button(text="Start", size_hint_x=0.1)
        self.start_btn.bind(on_press=self.controller.start_session)

        top.add_widget(self.user_edit)
        top.add_widget(Widget(size_hint_x=1))   # Stretch
        top.add_widget(self.add_to_box_btn)
        top.add_widget(self.combo_add_words)
        top.add_widget(self.dictionary_label)
        top.add_widget(Widget(size_hint_x=1))   # Stretch
        top.add_widget(self.start_btn)

        # ---------- Item Panel ----------
        self.item_panel = BoxLayout(orientation="vertical", size_hint_y=0.3)        
        header = BoxLayout(size_hint_y=0.2)
        self.id_label = Label(text="")
        self.level_label = Label(text="")
        header.add_widget(self.id_label)
        header.add_widget(self.level_label)

        self.item_label = Label(
            text="Word will appear here",
            font_size=24,
            halign="center",
            valign="middle"
        )
        self.item_label.bind(size=self.item_label.setter("text_size"))

        self.item_panel.add_widget(header)
        self.item_panel.add_widget(self.item_label)

        # ---------- Action Buttons ----------
        actions = BoxLayout(size_hint_y=0.1, spacing=5)
        self.show_answer_btn = Button(text="Show Answer", disabled=True)
        self.correct_btn = Button(text="Correct", disabled=True)
        self.wrong_btn = Button(text="Wrong", disabled=True)
        self.next_btn = Button(text="Next", disabled=True)
        self.delete_btn = Button(text="Delete", disabled=True)
        self.edit_btn = Button(text="Edit", disabled=True)
            # اضافه کردن دکمه‌ها به actions و وصل کردن به متدهای کنترلر
        self.show_answer_btn = Button(text="Show Answer", disabled=True)
        self.correct_btn = Button(text="Correct", disabled=True)
        self.wrong_btn = Button(text="Wrong", disabled=True)
        self.next_btn = Button(text="Next", disabled=True)
        self.delete_btn = Button(text="Delete", disabled=True)
        self.edit_btn = Button(text="Edit", disabled=True)

        # وصل کردن متدهای درست
        self.show_answer_btn.bind(on_press=self.controller.show_answer)
        self.correct_btn.bind(on_press=self.controller.mark_correct)
        self.wrong_btn.bind(on_press=self.controller.mark_wrong)
        self.next_btn.bind(on_press=self.controller.next_word)
        self.delete_btn.bind(on_press=self.controller.delete_word)
        self.edit_btn.bind(on_press=self.controller.edit_word)

# اضافه کردن به layout
        for btn in [self.show_answer_btn, self.correct_btn, self.wrong_btn, self.next_btn,
                    self.delete_btn, self.edit_btn]:
            actions.add_widget(btn)


       
         


        

        # ---------- Assemble ----------
        self.add_widget(buttons)
        self.add_widget(top)
        self.add_widget(self.item_panel)
        self.add_widget(actions)

        # ---------- Graph ----------
        # self.graph = self.create_matplotlib_graph()
        # self.add_widget(self.graph)

    # ---------- Graph with matplotlib ----------
    # def create_matplotlib_graph(self):
    # # 1️⃣ ایجاد Figure و رسم نمودار
    #     fig = Figure(figsize=(6,3), dpi=100)
    #     ax = fig.add_subplot(111)
    #     ax.set_xlabel("Levels")
    #     ax.set_ylabel("Number of Words")
    #     ax.set_xticks([1,2,3,4,5,6])
    #     ax.set_xticklabels(["1 (1d)","2 (2d)","3 (4d)","4 (8d)","5 (16d)","Done"])
    #     ax.set_ylim(0,10)
    #     bars = [0,0,0,0,0,0]
    #     ax.bar(range(1,7), bars, color=['b','orange','g','r','purple','grey'])

    #     # 2️⃣ Canvas Agg
    #     canvas = FigureCanvasAgg(fig)
    #     canvas.draw()

    #     # 3️⃣ گرفتن buffer با استفاده از renderer
    #     buf, (w, h) = canvas.print_to_buffer()

    #     # 4️⃣ تبدیل به Texture Kivy
    #     texture = Texture.create(size=(w,h))
    #     texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    #     texture.flip_vertical()  # جهت درست تصویر

    #     img = Image(texture=texture, size_hint_y=0.3, allow_stretch=True)
    #     return img


    # ---------- Popup ----------
    def show_popup(self, msg):
        Popup(
            title="Info",
            content=Label(text=msg),
            size_hint=(0.6, 0.4)
        ).open()

    # ---------- Close Event (معادل closeEvent) ----------
    def on_request_close(self, *args):
        if not self.controller.saved_flag:
            self.show_popup("Please save before exit")
            return True
        return False

# ---------------- App ----------------
class LeitnerApp(App):
    def build(self):
        Window.size = (800, 600)
        Window.title = "Leitner Box"
        root = MainWindow()
        EventLoop.window.bind(on_request_close=root.on_request_close)
        return root

if __name__ == "__main__":
    LeitnerApp().run()
