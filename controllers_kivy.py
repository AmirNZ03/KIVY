import pandas as pd
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.spinner import Spinner

import matplotlib.pyplot as plt
# from matplotlib.backends.backend_kivyagg import FigureCanvasKivyAgg

from model_kivy import Project, DictionaryItem, LeitnerItem
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

class LeitnerController:

    def __init__(self, ui):
        self.ui = ui
        self.project = Project()
        self.project_new = True
        self.current_day = 1
        self.current_item = None
        self.showing_answer = False
        self.dictionary_left = 0
        self.saved_flag = True
        self.filepath = None

        self._init_plot()

    def _init_plot(self):
        from kivy.graphics.texture import Texture
        from kivy.uix.image import Image
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg

        self.fig = Figure(figsize=(6,3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ui.graph_box = BoxLayout(size_hint_y=0.3)
        self.ui.add_widget(self.ui.graph_box)
        self.update_bar_plot()
    def update_bar_plot(self):
        levels = [0, 0, 0, 0, 0, 0]
        for item in self.project.box.values():
            levels[item.level - 1] += 1

        self.ax.clear()
        self.ax.bar(['1', '2', '3', '4', '5', 'Done'], levels)
        self.ax.set_ylim(0, max(levels) + 1 if levels else 1)

        from matplotlib.backends.backend_agg import FigureCanvasAgg
        canvas = FigureCanvasAgg(self.fig)
        canvas.draw()

        buf, (w, h) = canvas.print_to_buffer()
        texture = Texture.create(size=(w,h))
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        img = Image(texture=texture)
        self.ui.graph_box.clear_widgets()
        self.ui.graph_box.add_widget(img)
    # ---------------- Popup ----------------
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    # ---------------- Plot ----------------
    def _init_plot(self):
        self.fig = Figure(figsize=(6,3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ui.graph_box = BoxLayout(size_hint_y=0.3)  # مکانی برای نمودار
        self.ui.add_widget(self.ui.graph_box)
        self.update_bar_plot()

    def update_bar_plot(self):
    # پاک کردن محتوای قبلی نمودار
        self.ui.graph_box.clear_widgets()

        levels = [0, 0, 0, 0, 0, 0]
        for item in self.project.box.values():
            levels[item.level - 1] += 1

        self.ax.clear()
        self.ax.bar(
            range(1,7),
            levels,
            color=['b','orange','g','r','purple','grey']
        )
        self.ax.set_xticks([1,2,3,4,5,6])
        self.ax.set_xticklabels(["1 (1d)","2 (2d)","3 (4d)","4 (8d)","5 (16d)","Done"])
        self.ax.set_ylim(0, max(levels) + 1 if levels else 1)
        self.ax.set_xlabel("Levels")
        self.ax.set_ylabel("Number of Words")

        # Canvas Agg
        canvas = FigureCanvasAgg(self.fig)
        canvas.draw()
        buf, (w, h) = canvas.print_to_buffer()

        # Texture Kivy
        texture = Texture.create(size=(w,h))
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        img = Image(texture=texture, allow_stretch=True)
        self.ui.graph_box.add_widget(img)

    # ---------------- CSV ----------------
    def import_csv(self, *_):
        chooser = FileChooserIconView()
        popup = Popup(title="Select CSV", content=chooser, size_hint=(0.9, 0.9))

        def load(*_):
            if not chooser.selection:
                return
            try:
                df = pd.read_csv(chooser.selection[0], header=None)
                if df.shape[1] < 2:
                    self.show_popup("Error", "CSV must have at least 2 columns")
                    return
                if self.project.dictionary:
                    from kivy.uix.checkbox import CheckBox
                    from kivy.uix.gridlayout import GridLayout
                    layout = BoxLayout(orientation='vertical')
                    msg_label = Label(text="Dictionary not empty. Add to existing?")
                    btn_yes = Button(text="Yes")
                    btn_no = Button(text="No")
                    layout.add_widget(msg_label)
                    layout.add_widget(btn_yes)
                    layout.add_widget(btn_no)
                    popup2 = Popup(title="Import Options", content=layout, size_hint=(0.6,0.4))
                    def yes(*_):
                        start_id = max(self.project.dictionary.keys(), default=0) + 1
                        for i, row in df.iterrows():
                            self.project.dictionary[start_id + i] = DictionaryItem(
                                start_id + i, str(row[0]), str(row[1])
                            )
                        popup2.dismiss()
                        self.saved_flag = False
                        self.update_dictionary_label()
                    def no(*_):
                        self.project.dictionary = {}
                        self.project.box = {}
                        start_id = 1
                        for i, row in df.iterrows():
                            self.project.dictionary[start_id + i] = DictionaryItem(
                                start_id + i, str(row[0]), str(row[1])
                            )
                        popup2.dismiss()
                        self.saved_flag = False
                        self.update_dictionary_label()
                    btn_yes.bind(on_press=yes)
                    btn_no.bind(on_press=no)
                    popup2.open()
                else:
                # دیکشنری خالی است، اضافه کن
                    start_id = 1
                    for i, row in df.iterrows():
                        self.project.dictionary[start_id + i] = DictionaryItem(
                            start_id + i, str(row[0]), str(row[1])
                        )
                    self.saved_flag = False
                    self.update_dictionary_label()
                popup.dismiss()
            except Exception as e:
                self.show_popup("Error", str(e))

        chooser.bind(on_submit=lambda *_: load())
        popup.open()

    # def export_csv(self, *_):
    #     chooser = FileChooserIconView()
    #     popup = Popup(title="Save CSV", content=chooser, size_hint=(0.9, 0.9))

    #     def save(*_):
    #         if chooser.selection:
    #             df = pd.DataFrame(
    #                 [[i.word, i.translation] for i in self.project.dictionary.values()]
    #             )
    #             df.to_csv(chooser.selection[0], index=False, header=False)
    #             popup.dismiss()

    #     chooser.bind(on_submit=lambda *_: save())
    #     popup.open()
    def export_csv(self, *_):
        chooser = FileChooserIconView(path='.', dirselect=True)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        filename_input = TextInput(
            hint_text="File name (without .csv)",
            size_hint_y=None,
            height=40,
            multiline=False
        )

        export_btn = Button(
            text="Export CSV",
            size_hint_y=None,
            height=45
        )

        layout.add_widget(chooser)
        layout.add_widget(filename_input)
        layout.add_widget(export_btn)

        popup = Popup(
            title="Export CSV",
            content=layout,
            size_hint=(0.95, 0.95)
        )

        def do_export(*_):
            if not chooser.path:
                self.show_popup("Error", "Please select a folder")
                return

            filename = filename_input.text.strip() or "dictionary"
            filepath = f"{chooser.path}/{filename}.csv"

            try:
                df = pd.DataFrame([
                    [item.word, item.translation]
                    for item in self.project.dictionary.values()
                ])
                df.to_csv(filepath, index=False, header=False)
                popup.dismiss()
                self.show_popup("Success", f"CSV exported to:\n{filepath}")
            except Exception as e:
                self.show_popup("Error", str(e))

        export_btn.bind(on_press=do_export)
        popup.open()


    # ---------------- Manual Add ----------------
    def add_item_manually(self, *_):
        layout = BoxLayout(orientation='vertical')
        w = TextInput(hint_text='Word', multiline=False)
        t = TextInput(hint_text='Translation', multiline=False)
        btn = Button(text='Add')

        layout.add_widget(w)
        layout.add_widget(t)
        layout.add_widget(btn)

        popup = Popup(title="Add Item", content=layout, size_hint=(0.6, 0.5))

        def add(*_):
            if w.text and t.text:
                new_id = max(self.project.dictionary.keys(), default=0) + 1
                self.project.dictionary[new_id] = DictionaryItem(new_id, w.text, t.text)
                self.saved_flag = False
                self.update_dictionary_label()
                popup.dismiss()

        btn.bind(on_press=add)
        popup.open()

    # ---------------- Save / Load ----------------
    # def save_project(self, *_):
    #     chooser = FileChooserIconView()
    #     popup = Popup(title="Save Project", content=chooser, size_hint=(0.9, 0.9))

    #     def save(*_):
    #         if chooser.selection:
    #             self.project.user_name = self.ui.user_edit.text or "Sanaz"
    #             if self.project_new:
    #                 self.project.create_date = datetime.now().date()
    #                 self.project_new = False
    #             self.project.save_to_file(chooser.selection[0])
    #             self.saved_flag = True
    #             popup.dismiss()

    #     chooser.bind(on_submit=lambda *_: save())
    #     popup.open()
    def save_project(self, *_):
        chooser = FileChooserIconView(path='.', dirselect=True)
        layout = BoxLayout(orientation='vertical')
        filename_input = TextInput(
            hint_text="File name (without .json)",
            size_hint_y=None,
            height=40,
            multiline=False
        )
        save_btn = Button(text="Save", size_hint_y=None, height=40)

        layout.add_widget(chooser)
        layout.add_widget(filename_input)
        layout.add_widget(save_btn)

        popup = Popup(
            title="Save Project",
            content=layout,
            size_hint=(0.9, 0.9)
        )

        def save(*_):
            if not chooser.path:
                return

            filename = filename_input.text.strip() or "leitner_project"
            filepath = f"{chooser.path}/{filename}.json"

            self.project.user_name = self.ui.user_edit.text or "Sanaz"
            if self.project_new:
                self.project.create_date = datetime.now().date()
                self.project_new = False

            self.project.save_to_file(filepath)
            self.saved_flag = True
            popup.dismiss()

            self.show_popup("Saved", f"Project saved to:\n{filepath}")

        save_btn.bind(on_press=save)
        popup.open()

    # def load_project(self, *_):
    #     if not self.saved_flag:
    #         from kivy.uix.boxlayout import BoxLayout
    #         layout = BoxLayout(orientation='vertical')
    #         layout.add_widget(Label(text="Current project not saved. Save before loading?"))
    #         btn_yes = Button(text="Yes")
    #         btn_no = Button(text="No")
    #         layout.add_widget(btn_yes)
    #         layout.add_widget(btn_no)
    #         popup_save = Popup(title="Save Project?", content=layout, size_hint=(0.6,0.4))
    #         def save_now(*_):
    #             self.save_project()
    #             popup_save.dismiss()
    #         def dont_save(*_):
    #             popup_save.dismiss()
    #         btn_yes.bind(on_press=save_now)
    #         btn_no.bind(on_press=dont_save)
    #         popup_save.open()

    #     chooser = FileChooserIconView()
    #     popup = Popup(title="Load Project", content=chooser, size_hint=(0.9, 0.9))

    #     def load(*_):
    #         if chooser.selection:
    #             self.project = Project.load_from_file(chooser.selection[0])
    #             today = datetime.now().date()
    #             self.current_day = (today - self.project.create_date).days + 1
    #             self.ui.user_edit.text = self.project.user_name
    #             self.project_new = False
    #             self.update_dictionary_label()
    #             self.update_bar_plot()
    #             popup.dismiss()
    #             today_words = sum(
    #             1 for item in self.project.box.values()
    #             if item.day <= self.current_day - (2 ** (item.level-1))
    #             )
    #         self.show_popup(
    #             "Welcome Back",
    #             f"Hi {self.project.user_name}. Welcome Back 😊.\n"
    #             f"Today is Day {self.current_day} of your project.\n"
    #             f"You have {today_words} items to review today."
    #         )

    #     chooser.bind(on_submit=lambda *_: load())
    def load_project(self, *_):

        def open_loader():
            chooser = FileChooserIconView(filters=["*.json"])
            popup = Popup(title="Load Project", content=chooser, size_hint=(0.9, 0.9))

            def load(*_):
                if not chooser.selection:
                    return

                try:
                    filepath = chooser.selection[0]
                    self.project = Project.load_from_file(filepath)
                    self.project_new = False
                    self.saved_flag = True

                    # محاسبه روز جاری
                    today = datetime.now().date()
                    self.current_day = (today - self.project.create_date).days + 1

                    # بروزرسانی UI
                    self.ui.user_edit.text = self.project.user_name
                    self.update_dictionary_label()
                    self.update_bar_plot()

                    # محاسبه لغات امروز
                    today_words = sum(
                        1 for item in self.project.box.values()
                        if item.day <= self.current_day - (2 ** (item.level - 1))
                    )

                    popup.dismiss()

                    self.show_popup(
                    "Welcome Back",
                    f"Hi {self.project.user_name} 😊\n"
                    f"Day {self.current_day}\n"
                    f"{today_words} words to review today"
                )

                except Exception as e:
                    self.show_popup("Error", str(e))

            chooser.bind(on_submit=load)
            popup.open()

    # اگر پروژه ذخیره نشده
        if not self.saved_flag:
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
            layout.add_widget(Label(text="Current project is not saved.\nDo you want to save it?"))

            btns = BoxLayout(size_hint_y=None, height=40, spacing=10)
            btn_yes = Button(text="Save")
            btn_no = Button(text="Don't Save")
            btns.add_widget(btn_yes)
            btns.add_widget(btn_no)

            layout.add_widget(btns)
            popup_confirm = Popup(
                title="Save Project?",
                content=layout,
                size_hint=(0.7, 0.4)
            )

            def save_then_load(*_):
                popup_confirm.dismiss()
                self.save_project()
                open_loader()

            def dont_save_then_load(*_):
                popup_confirm.dismiss()
                open_loader()

            btn_yes.bind(on_press=save_then_load)
            btn_no.bind(on_press=dont_save_then_load)
            popup_confirm.open()
        else:
            open_loader()



    # ---------------- Leitner Logic ----------------
    def add_words_to_box(self, *_):
        if not self.project.dictionary:
            return

        val = self.ui.combo_add_words.text
        count = len(self.project.dictionary) if val == "All" else int(val)

        added = 0
        for item in self.project.dictionary.values():
            if item.id not in self.project.box:
                self.project.box[item.id] = LeitnerItem(item)
                added += 1
                if added >= count:
                    break

        self.saved_flag = False
        self.update_dictionary_label()
        self.ui.show_answer_btn.disabled = False
        self.ui.correct_btn.disabled = False
        self.ui.wrong_btn.disabled = False
        self.ui.next_btn.disabled = False
        self.ui.edit_btn.disabled = False
        self.ui.delete_btn.disabled = False
        self.update_bar_plot()

    def start_session(self, *_):
        self.current_item = self.find_next_item()
        self.display_item(self.current_item)
        # self.ui.show_answer_btn.disabled = True
        # self.ui.correct_btn.disabled = True
        # self.ui.wrong_btn.disabled = True
        # self.ui.next_btn.disabled = True
        # self.ui.edit_btn.disabled = True
        # self.ui.delete_btn.disabled = True
        # if self.current_item:
        #     self.ui.show_answer_btn.disabled = False
    def find_next_item(self):
        for lvl in range(1, 6):
            interval = 2 ** (lvl - 1)
            for item in self.project.box.values():
                if item.level == lvl and (
                    item.day == 0 or item.day <= self.current_day - interval
                ):
                    return item
        return None

    def display_item(self, item):
        self.showing_answer = False
        self.ui.item_label.canvas.before.clear()
        if item:
            self.ui.item_label.text = item.word
            self.ui.id_label.text = f"ID: {item.id}"
            self.ui.level_label.text = f"Level: {item.level}"
            self.ui.show_answer_btn.disabled = False
            self.ui.correct_btn.disabled = False
            self.ui.wrong_btn.disabled = False
            self.ui.next_btn.disabled = True
            self.ui.edit_btn.disabled = False
            self.ui.delete_btn.disabled = False
         
        else:
            self.ui.item_label.text = "No word to review"
            self.ui.id_label.text = ""
            self.ui.level_label.text = ""

            self.ui.show_answer_btn.disabled = True
            self.ui.correct_btn.disabled = True
            self.ui.wrong_btn.disabled = True
            self.ui.next_btn.disabled = True
            self.ui.edit_btn.disabled = True
            self.ui.delete_btn.disabled = True

    def show_answer(self, *_):
        if not self.current_item:
            return
        if not self.showing_answer:
            self.ui.item_label.text = f"{self.current_item.word}\n\n{self.current_item.translation}"
            
        else:
            self.ui.item_label.text = self.current_item.word
            
            
        self.showing_answer = not self.showing_answer


    def mark_correct(self, *_):
        if not self.current_item:
             return
        self.current_item.level = min(6, self.current_item.level + 1)
        self.current_item.day = self.current_day
        self.saved_flag = False
        self.ui.item_label.color = (1,1,1,1)  # متن سیاه
        self.ui.item_label.canvas.before.clear()
        with self.ui.item_label.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(0, 1, 0, 0.3)  # سبز روشن
                self.bg_rect = Rectangle(pos=self.ui.item_label.pos, size=self.ui.item_label.size)
        self.ui.correct_btn.disabled = True
        self.ui.wrong_btn.disabled = True
        self.ui.show_answer_btn.disabled = True
        self.ui.next_btn.disabled = False
        self.update_bar_plot()

    def mark_wrong(self, *_):
        if not self.current_item:
            return
        self.current_item.level = 1
        self.current_item.day = self.current_day
        self.saved_flag = False
        self.ui.item_label.color = (1,1,1, 1)
        self.ui.item_label.canvas.before.clear()
        with self.ui.item_label.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 0, 0, 0.3)  # قرمز روشن
            self.bg_rect = Rectangle(pos=self.ui.item_label.pos, size=self.ui.item_label.size)
            self.ui.correct_btn.disabled = True
            self.ui.wrong_btn.disabled = True
            self.ui.show_answer_btn.disabled = True
            self.ui.next_btn.disabled = False
        self.update_bar_plot()

    def next_word(self, *_):
        self.current_item = self.find_next_item()
        self.display_item(self.current_item)

    # ---------------- Delete / Edit ----------------
    def delete_word(self, *_):
        if not self.current_item:
            return
        del self.project.box[self.current_item.id]
        del self.project.dictionary[self.current_item.id]
        self.current_item = self.find_next_item()
        self.display_item(self.current_item)
        self.saved_flag = False
        self.update_dictionary_label()
        self.update_bar_plot()

    def edit_word(self, *_):
        layout = BoxLayout(orientation='vertical')
        w = TextInput(text=self.current_item.word)
        t = TextInput(text=self.current_item.translation)
        btn = Button(text='Apply')

        layout.add_widget(w)
        layout.add_widget(t)
        layout.add_widget(btn)

        popup = Popup(title="Edit Word", content=layout, size_hint=(0.6, 0.5))

        def apply(*_):
            self.current_item.word = w.text
            self.current_item.translation = t.text
            self.project.dictionary[self.current_item.id].word = w.text
            self.project.dictionary[self.current_item.id].translation = t.text
            self.saved_flag = False
            popup.dismiss()
            self.display_item(self.current_item)

        btn.bind(on_press=apply)
        popup.open()

    # ---------------- Dictionary ----------------
    def update_dictionary_label(self):
        self.dictionary_left = len(self.project.dictionary) - len(self.project.box)
        if self.dictionary_left > 0:
            self.ui.dictionary_label.text = f"{self.dictionary_left} items left"
            self.ui.add_to_box_btn.disabled = False
            self.ui.combo_add_words.disabled = False
        else:
            self.ui.dictionary_label.text = "No items left"
            self.ui.add_to_box_btn.disabled = True
            self.ui.combo_add_words.disabled = True