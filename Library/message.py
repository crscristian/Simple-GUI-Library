import csv
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App

def close_windows(instance):
    App.get_running_app().stop()


def close_popup(popup):
    popup.dismiss()

def window_popup():
    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text="Something is wrong!!"))

    # create button Close
    btn_close = Button(text='Close', size_hint=(None, None), size=(100, 50))

    # Create the layouts for the button
    layout_close = AnchorLayout(anchor_x='center', anchor_y='center')

    layout_close.add_widget(btn_close)


    btn_layout = BoxLayout(orientation='horizontal')
    btn_layout.add_widget(layout_close)
    content.add_widget(btn_layout)


    popup = Popup(title='Warning!',
                  content=content,
                  size_hint=(None, None), size=(300, 200))

    btn_close.bind(on_release=lambda instance: close_popup(popup))

    popup.open()

def close_window():
    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text='Do you want to close the window?'))

    btn_yes = Button(text='Yes', size_hint=(None, None), size=(100, 50))
    btn_no = Button(text='No', size_hint=(None, None), size=(100, 50))

    # Create the layouts for the buttons
    layout_yes = AnchorLayout(anchor_x='left', anchor_y='center')
    layout_no = AnchorLayout(anchor_x='right', anchor_y='center')

    layout_yes.add_widget(btn_yes)
    layout_no.add_widget(btn_no)

    btn_layout = BoxLayout(orientation='horizontal')
    btn_layout.add_widget(layout_yes)
    btn_layout.add_widget(layout_no)

    content.add_widget(btn_layout)


    popup = Popup(title='Close Window',
                  content=content,
                  size_hint=(None, None), size=(300, 200))

    btn_no.bind(on_release=lambda instance: close_popup(popup))
    btn_yes.bind(on_release=close_windows)

    popup.open()



#verify if email and password match
def login(email,password):
    if(email=="crisucristi13@gmail.com" and password=="0734120774A.X.L"):
        print(email)
        print(password)
        return True
    else:
        return False

def warning(sir1,sir2):

    sir2=str(sir2)
    content = BoxLayout(orientation='vertical')
    # content.add_widget(Label(text="E_mail or password is WRONG!!"))
    content.add_widget(Label(text=sir2))

    # create button Close
    btn_close = Button(text='Close', size_hint=(None, None), size=(100, 50))

    # Create the layouts for the button
    layout_close = AnchorLayout(anchor_x='center', anchor_y='center')

    layout_close.add_widget(btn_close)

    btn_layout = BoxLayout(orientation='horizontal')
    btn_layout.add_widget(layout_close)
    content.add_widget(btn_layout)

    sir1=str(sir1)
    popup = Popup(title=sir1,
                  content=content,
                  size_hint=(None, None), size=(300, 200))

    btn_close.bind(on_release=lambda instance: close_popup(popup))

    popup.open()

def incorrect_items(publication,nr_page):
    if publication.isdigit() and nr_page.isdigit():
        pass
        if int(publication)>0 and int(nr_page)>0:
            return 1
        else:
            window_popup()
            return 0
    else:
        window_popup()
        return 0



def save_book(n_book,n_author,publication,editura,nr_page):
        val=incorrect_items(publication,nr_page)
        if(val==True):

            info_save=[]
            info_save.append(n_book)
            info_save.append(n_author)
            info_save.append(publication)
            info_save.append(editura)
            info_save.append(nr_page)

            #save info book in  a tuple
            add_row=(n_book,n_author,publication,editura,nr_page)
            with open("books.csv","a",newline='\n') as file:
                #create an object for to write CSV file
                writer_csv=csv.writer(file)
                writer_csv.writerow(info_save)
                return add_row
        else:
            return 0


def update_csv_row(row_index, new_values):
    with open("books.csv", 'r') as file:
        rows = list(csv.reader(file))

    if row_index < len(rows):
        rows[row_index] = new_values

    with open("books.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)











