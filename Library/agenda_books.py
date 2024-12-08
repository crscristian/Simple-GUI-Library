from kivy.metrics import dp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
import csv
from kivy.clock import Clock
import message

Window.size = (1200, 600)

class LibraryTable(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"


        with open('books.csv', "r") as file:
            reader = csv.reader(file)
            row_info = [tuple(row) for row in reader]#transform each row csv file in tuple
            self.nr_old_rows=len(row_info)#save nr_row existed when app was open


        row_data = [(str(i + 1),) + row for i, row in enumerate(row_info)]
        #Create table
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("Nr.", dp(25)),
                ("Title of the book", dp(60),self.sort_on_title),
                ("Author", dp(50)),
                ("Year_app", dp(20)),
                ("Publisher", dp(30)),
                ("Nr_page", dp(30)),
            ],
            row_data=row_data,
            sorted_on="Nr_page",#shows us the data already sorted by a column
            sorted_order="ASC",
            elevation=2,
            rows_num=10,
        )

        screen = MDScreen()
        screen.add_widget(self.data_tables)

        # Add the two buttons
        remove_book_button = MDFlatButton(text="Remove Book")
        refresh_button = MDFlatButton(text="Refresh")
        update_button=MDFlatButton(text="Update")

        # Set the position of the buttons
        remove_book_button.pos_hint = {"x": 0.2, "y": 0.01}
        refresh_button.pos_hint = {"x": 0.05, "y": 0.01}
        update_button.pos_hint={"x": 0.379,"y": 0.01}
        #set the functionality of the button
        remove_book_button.bind(on_press=self.remove_row)
        refresh_button.bind(on_press=self.add_rows)
        update_button.bind(on_press=self.update_row)

        screen.add_widget(remove_book_button)
        screen.add_widget(refresh_button)
        screen.add_widget(update_button)


        return screen


    def add_rows(self, instance):
        with open('books.csv', "r") as file:
            reader = csv.reader(file)
            content_file= list(reader)
            self.nr_new_rows = len(content_file)  # save nr_row existed when app was open

        if(self.nr_old_rows==self.nr_new_rows):
            print(content_file)
            print(self.nr_new_rows)
            print(self.nr_old_rows)
            pass
        else:
            try:
                # print(nr_row)
                selected_rows = [tuple(row) for row in content_file[self.nr_old_rows:]]
                # print(selected_rows)
                last_num_row = int(self.data_tables.row_data[-1][0])

                for row in selected_rows:
                    last_num_row += 1
                    self.data_tables.add_row((str(last_num_row),) + row)

                self.nr_old_rows = self.nr_new_rows
            except Exception as e:
                print(f"A apărut o excepție:{e}")

        self.nr_old_rows=self.nr_new_rows

    def remove_row(self, instance):
        def deselect_rows(*args):
            self.data_tables.table_data.select_all("normal")

        for data in self.data_tables.get_row_checks():
            self.data_tables.remove_row(tuple(data))
            data.pop(0)

            filename = 'books.csv'

            with open(filename, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)

            rows = [row for row in rows if row != data]
            print(rows)
            with open(filename, 'w', newline='\n') as f:
                writer = csv.writer(f)
                writer.writerows(rows)


        Clock.schedule_once(deselect_rows)

    def sort_on_title(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))


    class EditRowModal(ModalView):
        def __init__(self, row_data, **kwargs):
            super().__init__(**kwargs)
            self.row_data = row_data

            layout = FloatLayout()
            background = '#160c0c'

            book_icon = Image(source='Images/book_icon.png',
                              allow_stretch=False,
                              keep_ratio=True,
                              size_hint=(None, None),
                              size=(200, 120))
            book_icon.pos = (350, 460)
            layout.add_widget(book_icon)

            label1 = Label(text='Title book:',
                           size_hint=(None, None),
                           size=(100, 35), pos=(245, 400),
                           font_size=22,
                           color=get_color_from_hex('#f7d85d'),
                           bold=True)
            layout.add_widget(label1)

            label2 = Label(text='Name author:', size_hint=(None, None),
                           size=(100, 35),
                           pos=(230, 350),
                           font_size=22,
                           color=get_color_from_hex('#f7d85d'),
                           bold=True)
            layout.add_widget(label2)

            label3 = Label(text='Publication:', size_hint=(None, None),
                           size=(100, 35),
                           pos=(230, 300),
                           font_size=22,
                           color=get_color_from_hex('#f7d85d'),
                           bold=True)
            layout.add_widget(label3)

            label4 = Label(text='Publisher:', size_hint=(None, None),
                           size=(100, 35),
                           pos=(230, 250),
                           font_size=22,
                           color=get_color_from_hex('#f7d85d'),
                           bold=True)
            layout.add_widget(label4)

            label5 = Label(text='Nr_pages:', size_hint=(None, None),
                           size=(100, 35),
                           pos=(230, 200),
                           font_size=22,
                           color=get_color_from_hex('#f7d85d'),
                           bold=True)
            layout.add_widget(label5)

            self.input1 = TextInput(size_hint=(None, None), size=(350, 35), pos=(350, 400),
                                    font_size=20,
                                    foreground_color=get_color_from_hex('#ffffff'),
                                    background_color=get_color_from_hex('#404040'),
                                    text=self.row_data[1])
            layout.add_widget(self.input1)

            self.input2 = TextInput(size_hint=(None, None), size=(350, 35), pos=(350, 350),
                                    font_size=20,
                                    foreground_color=get_color_from_hex('#ffffff'),
                                    background_color=get_color_from_hex('#404040'),
                                    text=self.row_data[2])
            layout.add_widget(self.input2)

            self.input3 = TextInput(size_hint=(None, None), size=(350, 35), pos=(350, 300),
                                    font_size=20,
                                    foreground_color=get_color_from_hex('#ffffff'),
                                    background_color=get_color_from_hex('#404040'),
                                    text=self.row_data[3])
            layout.add_widget(self.input3)

            self.input4 = TextInput(size_hint=(None, None), size=(350, 35), pos=(350, 250),
                                    font_size=20,
                                    foreground_color=get_color_from_hex('#ffffff'),
                                    background_color=get_color_from_hex('#404040'),
                                    text=self.row_data[4])
            layout.add_widget(self.input4)

            self.input5 = TextInput(size_hint=(None, None), size=(350, 35), pos=(350, 200),
                                    font_size=20,
                                    foreground_color=get_color_from_hex('#ffffff'),
                                    background_color=get_color_from_hex('#404040'),
                                    text=self.row_data[5])
            layout.add_widget(self.input5)

            update_book = Button(text="Update Info", pos=(415, 105),
                              size_hint=(None, None), size=(130, 45))
            update_book.bind(on_press=self.save_changes)
            layout.add_widget(update_book)

            self.add_widget(layout)


        def save_changes(self, instance):
            # Obține valorile actualizate din widget-urile de editare
            self.row_data[1] = self.input1.text
            self.row_data[2] = self.input2.text
            self.row_data[3] = self.input3.text
            self.row_data[4] = self.input4.text
            self.row_data[5] = self.input5.text


            self.dismiss()



    def update_row(self, instance):
        def deselect_rows(*args):
            self.data_tables.table_data.select_all("normal")

        selected_rows = self.data_tables.get_row_checks()
        if selected_rows:
            if len(selected_rows) == 1:
                selected_row = selected_rows[0]
                selected_row_number = selected_row[0]
                #find index for row cheked
                self.index = next((i for i, row in enumerate(self.data_tables.row_data) if row[0] == selected_row_number), None)
                if self.index is not None:
                    self.row_update = list(self.data_tables.row_data[self.index])
                    edit_modal = self.EditRowModal(self.row_update)
                    edit_modal.bind(on_dismiss=self.on_modal_dismissed)
                    edit_modal.open()

                    # Așteptăm până când fereastra modală este închisă
                    new_data = [self.row_update[0], edit_modal.input1.text, edit_modal.input2.text,
                                edit_modal.input3.text,edit_modal.input4.text,edit_modal.input5.text]
                else:
                    print("Selected row not found in the data table.")
            else:
                message.warning("Too many lines checked", "A single checked row!")
        else:
            message.warning("No checked row", "Need to check a row!")

        Clock.schedule_once(deselect_rows)

    def on_modal_dismissed(self, modal):
        def deselect_rows(*args):
            self.data_tables.table_data.select_all("normal")

        new_data = [self.row_update[0], modal.input1.text, modal.input2.text, modal.input3.text,modal.input4.text,modal.input5.text]
        self.data_tables.row_data[self.index] = new_data
        csv_data=[modal.input1.text, modal.input2.text, modal.input3.text,modal.input4.text,modal.input5.text]
        message.update_csv_row(self.index,csv_data)

        Clock.schedule_once(deselect_rows)



class Library(App):
    def build(self):
        layout = FloatLayout()
        background ='#160c0c'

        book_icon = Image(source='Images/book_icon.png',
                          allow_stretch=False,
                          keep_ratio=True,
                          size_hint=(None, None),
                          size=(120, 120))
        book_icon.pos = (130, 460)
        layout.add_widget(book_icon)

        label1 = Label(text='Title book:',
                       size_hint=(None, None),
                       size=(100, 35), pos=(45, 400),
                       font_size=22,
                       color=get_color_from_hex('#f7d85d'),
                       bold=True)
        layout.add_widget(label1)

        label2 = Label(text='Name author:', size_hint=(None, None),
                       size=(100, 35),
                       pos=(30, 350),
                       font_size=22,
                       color=get_color_from_hex('#f7d85d'),
                       bold=True)
        layout.add_widget(label2)

        label3 = Label(text='Publication:', size_hint=(None, None),
                       size=(100, 35),
                       pos=(30, 300),
                       font_size=22,
                       color=get_color_from_hex('#f7d85d'),
                       bold=True)
        layout.add_widget(label3)

        label4 = Label(text='Publisher:', size_hint=(None, None),
                       size=(100, 35),
                       pos=(30, 250),
                       font_size=22,
                       color=get_color_from_hex('#f7d85d'),
                       bold=True)
        layout.add_widget(label4)

        label5 = Label(text='Nr_pages:', size_hint=(None, None),
                       size=(100, 35),
                       pos=(30, 200),
                       font_size=22,
                       color=get_color_from_hex('#f7d85d'),
                       bold=True)
        layout.add_widget(label5)

        self.input1 = TextInput(size_hint=(None, None), size=(200, 35), pos=(150, 400),
                                font_size=20,
                                foreground_color=get_color_from_hex('#ffffff'),
                                background_color=get_color_from_hex('#404040'))
        layout.add_widget(self.input1)

        self.input2 = TextInput(size_hint=(None, None), size=(200, 35), pos=(150, 350),
                                font_size=20,
                                foreground_color=get_color_from_hex('#ffffff'),
                                background_color=get_color_from_hex('#404040'))
        layout.add_widget(self.input2)

        self.input3 = TextInput(size_hint=(None, None), size=(200, 35), pos=(150, 300),
                                font_size=20,
                                foreground_color=get_color_from_hex('#ffffff'),
                                background_color=get_color_from_hex('#404040'))
        layout.add_widget(self.input3)

        self.input4 = TextInput(size_hint=(None, None), size=(200, 35), pos=(150, 250),
                                font_size=20,
                                foreground_color=get_color_from_hex('#ffffff'),
                                background_color=get_color_from_hex('#404040'))
        layout.add_widget(self.input4)

        self.input5 = TextInput(size_hint=(None, None), size=(200, 35), pos=(150, 200),
                                font_size=20,
                                foreground_color=get_color_from_hex('#ffffff'),
                                background_color=get_color_from_hex('#404040'))
        layout.add_widget(self.input5)

        new_book = Button(background_normal='Images/button_new-book_up.png', pos=(155, 105),
                          size_hint=(None, None), size=(130, 45))
        new_book.bind(on_press=self.add_new_book)
        layout.add_widget(new_book)

        right_widget = BoxLayout(orientation='vertical', size_hint=(None, None), size=(750, 500))
        right_widget.pos = (400, 50)


        library_table=LibraryTable()
        table_widget = library_table.build()
        right_widget.add_widget(table_widget)

        layout.add_widget(right_widget)



        return layout

    def add_new_book(self, obj):
        obj.background_down = 'Images/button_new-book_down.png'
        self.val = message.save_book(self.input1.text, self.input2.text, self.input3.text, self.input4.text,
                                self.input5.text)

        if self.val:
            self.input1.text = ''
            self.input2.text = ''
            self.input3.text = ''
            self.input4.text = ''
            self.input5.text = ''
        else:
            pass

    def valoare(self,obj):
        return self.val


if __name__ == '__main__':
    Library().run()