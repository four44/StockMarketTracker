from kivy.app import App
from kivy.properties import NumericProperty,ReferenceListProperty, ObjectProperty, StringProperty, DictProperty
from kivy.clock import Clock
import yfinance as yf
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition, ScreenManager, Screen, FadeTransition, NoTransition
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
import mysql.connector
#import smtplib
#import os
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp, sp
from kivymd.uix.list import OneLineIconListItem
import math
import operator
from kivy.lang import Builder

Builder.load_string('''#:import Factory kivy.factory.Factory
<Login_Empty>:
    text: "Username And PassWord Required"
    title: 'Password Remainder'
    title_align: 'center'
    size_hint: None, None
    size_hint: 0.6 , 0.5
<Login_Error>:
    text: "Username or PassWord is Wrong"
    title: 'Password Remainder'
    title_align: 'center'
    size_hint: None, None
    size_hint: 0.6 , 0.5
<Signup_Empty>:
    text: "Username,PassWord and Email Required"
    title: 'Password Remainder'
    title_align: 'center'
    size_hint: None, None
    size_hint: 0.6 , 0.5
<Signup_Error>:
    text: "Username is Already Taken or Email is Already Registered"
    title: 'Password Remainder'
    title_align: 'center'
    size_hint: None, None
    size_hint: 0.6 , 0.5
<IconListItem>
    IconLeftWidget:
        icon: root.icon
<Forgot_Password>
    title: 'Password Remainder'
    title_align: 'center'
    size_hint: None, None
    size_hint: 0.6 , 0.5
    MDFloatLayout:
        MDTextField:
            id: username
            hint_text: "Username"
            icon_right: "account"
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
        MDTextField:
            id: email
            hint_text: "E-mail"
            icon_right: "at"
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
        MDFillRoundFlatIconButton:
            text: "Send   "
            fon_size: 12
            icon: "send"
            line_color: 1, 1, 1, 1
            on_press: root.send()
            pos_hint: {"center_x": 0.5, "center_y": 0.2}

<LoginWindow>
    FloatLayout:
        Image:
            source: 'b.png'
            pos_hint: {"center_x": 0.5, "center_y": 0.8}
            size_hint: 0.6, 0.6
    FloatLayout:
        size_hint: None, None
        size: 300, 400
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        MDIcon:
            id: welcome_label
            font_size: 60
            pos_hint: {"center_x": 0.9, "center_y": 0.9}
            icon: "account-arrow-right"
        MDTextField:
            id: user
            hint_text: "Username"
            icon_right: "account"
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
        MDTextField:
            id: password
            hint_text: "Password"
            icon_right: "eye-off"
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            password: True
        MDFillRoundFlatIconButton:
            id: login
            text: "Log-In   "
            fon_size: 12
            icon: "account-arrow-right"
            pos_hint: {"center_x": 0.75, "center_y": 0.35}
            on_press: root.login(user.text,password.text)
        MDFillRoundFlatIconButton:
            text: "Clear      "
            fon_size: 12
            icon: "close-circle-multiple-outline"
            pos_hint: {"center_x": 0.25, "center_y": 0.35}
            on_press: root.clear()
        MDFillRoundFlatIconButton:
            text: "Forgot   "
            fon_size: 12
            icon: "lock-question"
            pos_hint: {"center_x": 0.25, "center_y": 0.2}
            on_press: Factory.Forgot_Password().open()
        MDFillRoundFlatIconButton:
            text: "Sign-Up "
            fon_size: 12
            icon: "account-plus"
            pos_hint: {"center_x": 0.75, "center_y": 0.2}
            on_press: root.sign_up('Signup')
        Label:
            text: "Tech Software Financial Services"
            font_size: 8
            pos_hint: {"center_x": 0.5, "center_y": 0.0001}

<RegisterWindow>
    MDFloatLayout:
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {'center_x': 0.9, 'center_y': 0.95}
            on_press:
                root.manager.current = 'Login'
    FloatLayout:
        Image:
            source: 'b.png'
            pos_hint: {"center_x": 0.5, "center_y": 0.8}
            size_hint: 0.6, 0.6
    FloatLayout:
        size_hint: None, None
        size: 300, 400
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        MDIcon:
            id: welcome_label
            font_size: 60
            pos_hint: {"center_x": 0.9, "center_y": 0.9}
            icon: "account-plus"
        MDTextField:
            id: user
            hint_text: "Username"
            icon_right: "account"
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
        MDTextField:
            id: password
            hint_text: "Password"
            icon_right: "eye-off"
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            password: True
        MDTextField:
            id: email
            hint_text: "E-mail"
            icon_right: "at"
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5, "center_y": 0.40}
        MDFillRoundFlatIconButton:
            text: "Clear      "
            fon_size: 12
            icon: "close-circle-multiple-outline"
            pos_hint: {"center_x": 0.25, "center_y": 0.2}
            on_press: root.clear()
        MDFillRoundFlatIconButton:
            text: "Register"
            fon_size: 12
            icon: "file-account-outline"
            pos_hint: {"center_x": 0.75, "center_y": 0.2}
            on_press: root.register()
        Label:
            text: "Tech Software Financial Services"
            font_size: 8
            pos_hint: {"center_x": 0.5, "center_y": 0.0001}

<MainWindow>
    MDBottomNavigation:
        MDBottomNavigationItem:
            name: "monitor-eye"
            icon: "monitor-eye"
            MDFloatLayout:
                MDIconButton:
                    icon: "head-question-outline"
                    pos_hint: {"center_x": 0.9, "center_y": 0.95}
                Image:
                    source: 'b.png'
                    pos_hint: {"center_x": 0.1, "center_y": 0.95}
                    size_hint: 0.15, 0.15
                MDCard:
                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    size_hint: 0.95, 0.9
                    pos_hint: {"center_x": 0.5, "center_y": 0.45}
                    orientation: 'vertical'
                    MDBoxLayout:
                        size_hint_y: 0.35
                        orientation: "vertical"
                        MDBoxLayout:
                            size_hint_y:0.3
                        MDTextField:
                            id: screen_input
                            hint_text: "Symbols"
                            icon_right: "cash-multiple"
                            icon_right_color: 1,1,1,1
                            size_hint_x: 0.7
                            font_size: 18
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            helper_text: ""
                            helper_text_mode: "persistent"
                        MDFloatLayout:
                            MDFillRoundFlatIconButton:
                                text: "Add      "
                                fon_size: 12
                                icon: "eye-plus-outline"
                                pos_hint: {'center_x': 0.35, 'center_y': 0.5}
                                on_press: root.add()
                            MDFillRoundFlatIconButton:
                                text: "Delete   "
                                fon_size: 12
                                icon: "eye-minus-outline"
                                pos_hint: {'center_x': 0.65, 'center_y': 0.5}
                                on_press: root.delete_row_of_screener()

                        MDBoxLayout:
                            cols: 5
                            spacing: 15
                            padding: 15
                            MDLabel:
                                text: "Symbol"
                                font_name: 'Timesbd'
                            MDLabel:
                                text: "Name"
                                font_name: 'Timesbd'
                            MDLabel:
                                text: "Value"
                                font_name: 'Timesbd'
                            MDLabel:
                                text: "Day Gain"
                                font_name: 'Timesbd'
                            MDLabel:
                                text: "Choices"
                                font_name: 'Timesbd'

                        MDSeparator:
                            height: "3dp"
                            color: 1, 1, 1, 1
                    MDScrollViewRefreshLayout:
                        id: screneer_scroll_view
                        do_scroll_x: False
                        do_scroll_y: True
                        refresh_callback: root.refresh_callback
                        root_layout: root
                        MDGridLayout:
                            id: screener
                            cols: 1
                            row_force_default : True
                            row_default_height: 30
                            spacing: 15
                            padding: 15

        MDBottomNavigationItem:
            name: "bell-ring-outline"
            icon: "bell-ring-outline"
            MDFloatLayout:
                MDIconButton:
                    icon: "head-question-outline"
                    pos_hint: {"center_x": 0.9, "center_y": 0.95}
                Image:
                    source: 'b.png'
                    pos_hint: {"center_x": 0.1, "center_y": 0.95}
                    size_hint: 0.15, 0.15
                MDCard:
                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    size_hint: 0.95, 0.9
                    pos_hint: {"center_x": 0.5, "center_y": 0.45}
                    orientation: 'vertical'
                    MDBoxLayout:
                        size_hint_y: 0.6
                        orientation: "vertical"
                        MDBoxLayout:
                            size_hint_y: 0.10
                        MDTextField:
                            id: signal_textınput
                            hint_text: "Symbols"
                            icon_right: "cash-multiple"
                            icon_right_color: 1,1,1,1
                            size_hint_x: 0.7
                            font_size: 18
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            helper_text: ""
                            helper_text_mode: "persistent"
                        MDBoxLayout:
                            orientation: 'horizontal'
                            cols:2
                            MDFloatLayout:
                                MDTextField:
                                    id: set_number
                                    hint_text: "Set Number"
                                    icon_right: "bell-ring-outline"
                                    icon_right_color: 1,1,1,1
                                    size_hint_x: 0.7
                                    font_size: 18
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.75}
                                    helper_text: ""
                                    helper_text_mode: "persistent"
                                MDFillRoundFlatIconButton:
                                    text: "Set Signal  "
                                    fon_size: 12
                                    icon: "bell-ring-outline"
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                                    on_press: root.set_signal()
                            MDFloatLayout:
                                MDTextField:
                                    id: choice_signal
                                    hint_text: "Selection"
                                    icon_right: "bell-ring-outline"
                                    icon_right_color: 1,1,1,1
                                    size_hint_x: 0.7
                                    font_size: 18
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.75}
                                    helper_text: ""
                                    helper_text_mode: "persistent"
                                    on_focus: if self.focus: root.menu_signal.open()
                                MDFillRoundFlatIconButton:
                                    text: "Signals     "
                                    fon_size: 12
                                    icon: "bell-ring-outline"
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                                    on_press: root.choice_signals()

                        MDBoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: 0.35
                            spacing: 15
                            padding: 25
                            MDLabel:
                                text: "Alarm Setup"
                                font_name: 'Timesbd'
                            MDFloatLayout:
                                MDIconButton:
                                    icon: "delete-empty"
                                    on_press: root.delete_row_of_signal()
                                    pos_hint: {'center_x': 0.85, 'center_y': 0.5}
                        MDSeparator:
                            height: "3dp"
                            color: 1, 1, 1, 1
                    ScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        MDGridLayout:
                            id: signal_view
                            size_hint_y: 1.25
                            cols: 1
                            row_force_default : True
                            row_default_height: 30
                            spacing: 15
                            padding: 25

        MDBottomNavigationItem:
            name: "filter-outline"
            icon: "filter-outline"
            MDFloatLayout:
                MDIconButton:
                    icon: "head-question-outline"
                    pos_hint: {"center_x": 0.9, "center_y": 0.95}
                Image:
                    source: 'b.png'
                    pos_hint: {"center_x": 0.1, "center_y": 0.95}
                    size_hint: 0.15, 0.15
                MDCard:
                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    size_hint: 0.95, 0.9
                    pos_hint: {"center_x": 0.5, "center_y": 0.45}
                    orientation: 'vertical'
                    MDBoxLayout:
                        size_hint_y: 0.6
                        orientation: "vertical"
                        MDBoxLayout:
                            size_hint_y: 0.10
                        MDTextField:
                            id: filter_symbol_textınput
                            hint_text: "Symbols"
                            icon_right: "cash-multiple"
                            icon_right_color: 1,1,1,1
                            size_hint_x: 0.7
                            font_size: 18
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            helper_text: ""
                            helper_text_mode: "persistent"
                        MDFloatLayout:
                            MDFillRoundFlatIconButton:
                                text: "Add     "
                                fon_size: 12
                                icon: "eye-plus-outline"
                                pos_hint: {'center_x': 0.25, 'center_y': 0.5}
                                on_press: root.filter_add()
                            MDFillRoundFlatIconButton:
                                text: "Clear     "
                                fon_size: 12
                                icon: "close-circle-multiple-outline"
                                pos_hint: {'center_x': 0.75, 'center_y': 0.5}
                                on_press: root.clear_filter()
                        MDFloatLayout:
                            id: dropdown_place
                            MDTextField:
                                id: choice_filter
                                hint_text: "Choice"
                                icon_right: "filter-outline"
                                icon_right_color: 1,1,1,1
                                size_hint_x: 0.45
                                font_size: 18
                                pos_hint: {'center_x': 0.25, 'center_y': 0.5}
                                on_focus: if self.focus: root.menu_filter.open()
                            MDTextField:
                                id: selection_filter
                                hint_text: "Selection"
                                icon_right: "filter-outline"
                                icon_right_color: 1,1,1,1
                                size_hint_x: 0.45
                                font_size: 18
                                pos_hint: {'center_x': 0.75, 'center_y': 0.5}
                                on_focus: if self.focus: root.menu_selection.open()
                        MDFloatLayout:
                            MDFillRoundFlatIconButton:
                                text: "Filter  "
                                fon_size: 12
                                icon: "filter-outline"
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_press: root.filter_function_button()
                        MDBoxLayout:
                            size_hint_y: 0.55
                            spacing: 15
                            padding: 20
                            orientation: 'horizontal'
                            MDLabel:
                                text: "Symbols"
                                font_name: 'Timesbd'
                            MDLabel:
                                id: filter_future
                                text: "Futures"
                                font_name: 'Timesbd'

                        MDSeparator:
                            height: "3dp"
                            color: 1, 1, 1, 1
                    ScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        MDGridLayout:
                            id: filter
                            size_hint_y: 1.25
                            cols: 1
                            row_force_default : True
                            row_default_height: 30
                            spacing: 15
                            padding: 20


        MDBottomNavigationItem:
            name: "magnify"
            icon: "magnify"
            MDFloatLayout:
                MDIconButton:
                    icon: "head-question-outline"
                    pos_hint: {"center_x": 0.9, "center_y": 0.95}
                Image:
                    source: 'b.png'
                    pos_hint: {"center_x": 0.1, "center_y": 0.95}
                    size_hint: 0.15, 0.15
                MDCard:
                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    size_hint: 0.95, 0.9
                    pos_hint: {"center_x": 0.5, "center_y": 0.45}
                    orientation: 'vertical'
                    MDBoxLayout:
                        size_hint_y: 0.35
                        orientation: "vertical"
                        MDBoxLayout:
                            size_hint_y:0.3
                        MDTextField:
                            id: search_textınput
                            hint_text: "Symbols"
                            icon_right: "cash-multiple"
                            icon_right_color: 1,1,1,1
                            size_hint_x: 0.7
                            font_size: 18
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            helper_text: ""
                            helper_text_mode: "persistent"
                        MDFloatLayout:
                            MDFillRoundFlatIconButton:
                                text: "Profile    "
                                fon_size: 12
                                icon: "magnify"
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_press: root.search_profile()
                            MDFillRoundFlatIconButton:
                                text: "Clear      "
                                fon_size: 12
                                icon: "close-circle-multiple-outline"
                                pos_hint: {'center_x': 0.8, 'center_y': 0.5}
                                on_press: root.clear_search()
                            MDFillRoundFlatIconButton:
                                text: "Statistic"
                                fon_size: 12
                                icon: "magnify"
                                pos_hint: {'center_x': 0.2, 'center_y': 0.5}
                                on_press: root.search_statistic()
                        MDBoxLayout:
                            spacing: 15
                            padding: 25
                            MDLabel:
                                text: "Data of the Symbol"
                                font_name: 'Timesbd'
                        MDSeparator:
                            height: "3dp"
                            color: 1, 1, 1, 1
                    ScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        MDGridLayout:
                            id: search
                            cols: 1
                            row_force_default : True
                            row_default_height: 30
                            spacing: 15
                            padding: 25


        MDBottomNavigationItem:
            name: "setting"
            icon: "cogs"
            MDFloatLayout:
                MDIconButton:
                    icon: "head-question-outline"
                    pos_hint: {"center_x": 0.8, "center_y": 0.95}
                MDIconButton:
                    icon: "logout"
                    pos_hint: {'center_x': 0.9, 'center_y': 0.95}
                    on_press:
                        root.manager.current = 'Login'
                        root.log_out()
                Image:
                    source: 'b.png'
                    pos_hint: {"center_x": 0.1, "center_y": 0.95}
                    size_hint: 0.15, 0.15
                MDCard:
                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    size_hint: 0.95, 0.9
                    pos_hint: {"center_x": 0.5, "center_y": 0.45}
                    MDBoxLayout:
                        orientation: "vertical"
                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: 15
                            padding: 25
                            MDBoxLayout:
                                size_hint_x: None
                                size_hint_x: 0.75
                                MDLabel:
                                    text: "Username"
                                    font_name: 'Timesbd'
                            MDBoxLayout:
                                size_hint_x: None
                                size_hint_x: 0.2
                                MDLabel:
                                    text: ":"
                                    font_name: 'Timesbd'
                            MDLabel:
                                id: setting_username
                                font_name: 'Timesbd'
                        MDBoxLayout:
                            spacing: 15
                            padding: 25
                            orientation: "horizontal"
                            MDBoxLayout:
                                size_hint_x: None
                                size_hint_x: 0.75
                                MDLabel:
                                    text: "E-mail"
                                    font_name: 'Timesbd'
                            MDBoxLayout:
                                size_hint_x: None
                                size_hint_x: 0.2
                                MDLabel:
                                    text: ":"
                                    font_name: 'Timesbd'
                            MDLabel:
                                id: setting_mail
                                font_name: 'Timesbd'
                        MDBoxLayout:
                            spacing: 15
                            padding: 25
                            orientation: "horizontal"
                            MDBoxLayout:
                                size_hint_x: None
                                size_hint_x: 0.75
                                MDLabel:
                                    text: "Password Change"
                                    font_name: 'Timesbd'
                            MDBoxLayout:
                                size_hint_x: None
                                size_hint_x: 0.2
                                MDLabel:
                                    text: ":"
                                    font_name: 'Timesbd'
                            MDFloatLayout:
                                orientation: "horizontal"
                                MDTextField:
                                    id: setting_input
                                    hint_text: "New Password"
                                    icon_right: "eye-off"
                                    icon_right_color: 1,1,1,1
                                    font_size: 18
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                MDIconButton:
                                    icon: "delta"
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.1}
                                    on_press: root.change_password()
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: 15
                            padding: 25
                            MDLabel:
                                text: "New Password"
                                font_name: 'Timesbd'
                                halign: "center"
                            MDLabel:
                                text: "Password Change"
                                font_name: 'Timesbd'
                                halign: "center"
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: 15
                            padding: 25
                            size_hint_y: None
                            size_hint_y: 0.75
<MyScreenManager>
    id: screen_manager
    screen_one: screen_one
    screen_two: screen_two
    screen_three: screen_three
    LoginWindow:
        id: screen_one
        name: 'Login'
        manager: screen_manager
    RegisterWindow:
        id: screen_two
        name: 'Signup'
        manager: screen_manager
    MainWindow:
        id: screen_three
        name: 'Home'
        manager: screen_manager
''')

globalid = StringProperty('')

class LoginWindow(Screen):

    def sign_up(self,screen_value):
        self.manager.current = screen_value

    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""

    def login(self,username,password):
        global globalid
        val = [username,password]
        records = mydatabase().get_user_info()
        if username == '' or password == '':
            Login_Empty().open()
        else:
            y = 0
            for row in records:
                if list(row) == val:
                    y=+1
                    globalid = val[0]
                    self.sign_up('Home')
                    self.ids.user.text = ""
                    self.ids.password.text = ""

            if y == 0:
                Login_Error().open()


class Forgot_Password(Popup):
    def send(self):
        pass
        #Email_Address = os.environ.get('**********')
        #Email_Password = os.environ.get('********')

        # with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        #     smtp.ehlo()
        #     smtp.starttls()
        #     smtp.ehlo()
        #     smtp.login(Email_Address, Email_Password)
        #     subject = 'Password Remainder'
        #     body = 'Password goes here'
        #     msg = f'Subject: {subject}\n\n{body} '
        #     smtp.sendmail(Email_Address, '*************', msg)


class Login_Empty(Popup):
    pass
class Login_Error(Popup):
    pass
class Signup_Empty(Popup):
    pass
class Signup_Error(Popup):
    pass
class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class mydatabase:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            port="3306",
            username="root",
            passwd="**********",
            database="mydatabase"
        )
        self.mycursor = self.mydb.cursor()

    def get_user_info(self):
        query = ("SELECT username,password FROM usersinfo")
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def get_userS(self):
        query = ("SELECT username FROM usersinfo")
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def get_Passwords(self):
        query = ("SELECT password FROM usersinfo")
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def get_mail(self):
        query = ("SELECT email FROM usersinfo")
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def get_mail_of_globalid(self):
        self.mycursor.execute("SELECT email FROM usersinfo Where username= %s", (globalid,))
        return (self.mycursor.fetchone()[0]).split(',')[0]

    def signups(self,username,password,email):
        sql = "INSERT INTO usersinfo (username, password, email) VALUES (%s, %s,%s)"
        val = (username, password, email)
        self.mycursor.execute(sql,val)
        self.mydb.commit()
        default_screener = ["btc-usd"]
        sql1 = "INSERT INTO datainfo (username,screenerdata) VALUES (%s,%s)"
        val1 = [username,','.join(default_screener)]
        self.mycursor.execute(sql1, val1)
        self.mydb.commit()

    def get_screenerdata_from_datainfo(self):
        self.mycursor.execute("SELECT screenerdata FROM datainfo WHERE username= %s", (globalid,))
        return (self.mycursor.fetchone()[0]).split(',')

    def get_signaldata_from_datainfo(self):
        self.mycursor.execute("SELECT signaldata FROM datainfo WHERE username= %s", (globalid,))
        return self.mycursor.fetchone()

    def update_datainfo(self, screen_data):
        self.mycursor.execute("UPDATE datainfo SET screenerdata =(%s) WHERE username= (%s) ", (screen_data, globalid))
        self.mydb.commit()

    def update_password(self, password):
        self.mycursor.execute("UPDATE usersinfo SET password =(%s) WHERE username= (%s) ", (password, globalid))
        self.mydb.commit()

class RegisterWindow(Screen):

    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""
        self.ids.email.text = ""

    def register(self):
        db_answer = mydatabase().get_userS()
        db_answer3 = mydatabase().get_mail()
        username = self.ids.user.text
        password = self.ids.password.text
        email = self.ids.email.text
        Val = [username]
        Val3= email
        if username == '' or password == '' or email == '':
            Signup_Empty().open()
        else:
            x=0
            while True:
                for row in db_answer:
                    if list(row) == Val:
                        Signup_Error().open()
                        x=x+1
                        break
                if x==0:
                    for row3 in db_answer3:
                        if list(row3) == Val3:
                             Signup_Error().open()
                             x=x+1
                             break
                if x==0:
                    mydatabase().signups(username, password, email)
                    App.get_running_app().root.current = "Login"
                break


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Entrance Phase to Main Screen
    def on_enter(self, *args):
        self.mysql_data_default()
        self.ids.screener.size_hint_y = len(self.list_screener_symbol)/8
        self.ids.setting_username.text = globalid
        self.ids.setting_mail.text = mydatabase().get_mail_of_globalid()
        self.drop_down_active()
        self.drop_down_active_signal()
        Clock.schedule_interval(self.control_signal_set_number, 10)



# Screener Tab
    def refresh_callback(self, *args):
        def refresh_callback(interval):
            try:
                for symbol in self.dict_symbol_and_currentvalue_label_id.keys():
                    self.dict_symbol_and_currentvalue_label_id[symbol].text = self.get_stock_price(symbol)
                for symbol in self.dict_symbol_and_daily_change_label_id.keys():
                    self.dict_symbol_and_daily_change_label_id[symbol].text = self.daily_gain(symbol)[0]
                    self.dict_symbol_and_daily_change_label_id[symbol].text_color = self.daily_gain(symbol)[1]
                self.ids.screneer_scroll_view.refresh_done()
            except:
                pass
        Clock.schedule_once(refresh_callback, 1)

    def get_stock_price(self, stockname):
        stock = yf.Ticker(stockname)
        todays_data = stock.history(period='1d')
        CurrentValue = "{:.2f}".format(todays_data['Close'][0])
        return str(CurrentValue)

    def daily_gain(self, stockname):
        stock = yf.Ticker(stockname)
        data1 = stock.info
        todays_data = stock.history(period='1d')
        CurrentValue = todays_data['Close'][0]
        diffrences = CurrentValue - data1['open']
        if diffrences > 0:
            return "% +" + str("{:.2f}".format((diffrences / data1['open']) * 100)), (0, 100/255, 0, 1)
        else:
            return "% -" + str("{:.2f}".format((diffrences / data1['open']) * 100)), (139/255, 0, 0, 1)

    def get_stock_info(self, stockname):
        stock = yf.Ticker(stockname)
        name = stock.info.get('name')
        try:
            if name == None:
                return stock.info.get('shortName')
            else:
                return name
        except:
            print('error')

    dict_checkbox_id_and_boxlayout_id = {}
    dict_checkbox_id_and_symbol = {}
    dict_symbol_and_currentvalue_label_id = {}
    dict_symbol_and_daily_change_label_id = {}
    list_screener_symbol = []

    def add(self):
        self.symbol = str.upper(self.ids.screen_input.text)
        if self.symbol in self.list_screener_symbol:
            self.ids.screen_input.helper_text = 'Already exist'
        else:
            try:
                self.form_screener_label(self.symbol)
                self.ids.screen_input.helper_text = ''
                mydatabase().update_datainfo((','.join(self.list_screener_symbol)))
                self.ids.screener.size_hint_y = len(self.list_screener_symbol)/8
            except:
                self.ids.screen_input.helper_text = 'Write properly'
            self.ids.screen_input.text = ''

    def form_screener_label(self, symbol):
        # form the labels and checkbox
        self.symbol_label = MDLabel(text=symbol, theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.symbol_label.font_name = 'Timesi'
        self.symbol_name_label = MDLabel(text=self.get_stock_info(symbol), theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.symbol_name_label.font_name = 'Timesi'
        self.current_value_label = MDLabel(text=self.get_stock_price(symbol), theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.current_value_label.font_name = 'Timesi'
        self.daily_change_label = MDLabel(text=self.daily_gain(symbol)[0], theme_text_color= "Custom", text_color=self.daily_gain(symbol)[1])
        self.daily_change_label.font_name = 'Timesi'
        self.choice_checkbox = CheckBox()
        self.choice_checkbox.bind(active=self.on_checkbox_active)
        # form and add the box layout
        self.screen_list_row = MDBoxLayout(orientation='horizontal', spacing=15)
        self.ids.screener.add_widget(self.screen_list_row)
        # add widgets into box layout
        self.screen_list_row.add_widget(self.symbol_label)
        self.screen_list_row.add_widget(self.symbol_name_label)
        self.screen_list_row.add_widget(self.current_value_label)
        self.screen_list_row.add_widget(self.daily_change_label)
        self.screen_list_row.add_widget(self.choice_checkbox)
        # arrange the dictionaries of ids
        self.dict_checkbox_id_and_boxlayout_id.update({self.choice_checkbox: self.screen_list_row})
        self.dict_checkbox_id_and_symbol.update({self.choice_checkbox: symbol})
        self.dict_symbol_and_currentvalue_label_id.update({symbol: self.current_value_label})
        self.dict_symbol_and_daily_change_label_id.update({symbol: self.daily_change_label})
        self.list_screener_symbol.append(symbol)

    def mysql_data_default(self):
        try:
            if mydatabase().get_screenerdata_from_datainfo() == self.list_screener_symbol:
                pass
            else:
                for symbol in mydatabase().get_screenerdata_from_datainfo():
                    self.form_screener_label(symbol)
        except:
            pass

    check_box_ids_for_delete = []
    def on_checkbox_active(self, check, value):
        if value:
            self.check_box_ids_for_delete.append(check)
        else:
            self.check_box_ids_for_delete.remove(check)

    def delete_row_of_screener(self):
        for check_box_id in self.check_box_ids_for_delete:
            self.ids.screener.remove_widget(self.dict_checkbox_id_and_boxlayout_id[check_box_id])
            self.dict_checkbox_id_and_boxlayout_id.pop(check_box_id)
            symbol = self.dict_checkbox_id_and_symbol[check_box_id]
            self.dict_checkbox_id_and_symbol.pop(check_box_id)
            self.dict_symbol_and_currentvalue_label_id.pop(symbol)
            self.dict_symbol_and_daily_change_label_id.pop(symbol)
            self.list_screener_symbol.remove(symbol)
        self.check_box_ids_for_delete.clear()
        mydatabase().update_datainfo((','.join(self.list_screener_symbol)))
        self.ids.screener.size_hint_y = len(self.list_screener_symbol)/8


# Signal Tab
    dict_signal_order = {}
    dict_set_number = {}
    dict_checkboxid_and_boxlayoutid = {}
    dict_checkboxid_and_stockname = {}
    dict_stockname_and_inform_label = {}
    signal_choices = ['fiftyDayAverage', 'twoHundredDayAverage', 'dayHigh', 'dayLow', 'previousClose', 'open']

    def choice_signals(self):
        try:
            stockname = str.upper(self.ids.signal_textınput.text)
            stock = yf.Ticker(stockname)
            todays_data = stock.history(period='1d')
            currentvalue = float("{:.2f}".format(todays_data['Close'][0]))
            self.ids.signal_textınput.text_helper = ''
        except:
            self.ids.signal_textınput.text_helper = 'Invalid symbol'
        try:
            choice = self.ids.choice_signal.text
            self.ids.signal_textınput.text = ''
            self.ids.choice_signal.text = ''
            self.ids.choice_signal.text_helper = ''

        except:
            self.ids.choice_signal.text_helper = 'Invalid choice'
        choice_number = float(stock.info.get(choice))
        self.dict_signal_order.update({(stockname,choice_number): currentvalue})
        self.dict_set_number.update({(stockname, choice_number): choice})

        symbol_label = MDLabel(text=stockname, theme_text_color="Custom", text_color=(1, 1, 1, 1))
        symbol_label.font_name = 'Timesi'
        symbol_set_number_label = MDLabel(text=choice, theme_text_color="Custom", text_color=(1, 1, 1, 1))
        symbol_set_number_label.font_name = 'Timesi'
        symbol_inform_label = MDLabel(text=str('Setted Up '), theme_text_color="Custom", text_color=(139/255, 0, 0, 1))
        symbol_inform_label.font_name = 'Timesi'
        delete_checkbox = CheckBox()
        delete_checkbox.bind(active=self.on_delete_checkbox_active)
        signal_list_row = MDBoxLayout(orientation='horizontal', spacing=15)
        signal_list_row.add_widget(symbol_label)
        signal_list_row.add_widget(symbol_set_number_label)
        signal_list_row.add_widget(symbol_inform_label)
        signal_list_row.add_widget(delete_checkbox)
        self.ids.signal_view.add_widget(signal_list_row)

        self.dict_stockname_and_inform_label.update({(stockname, choice_number): symbol_inform_label})
        self.dict_checkboxid_and_boxlayoutid.update({delete_checkbox: signal_list_row})
        self.dict_checkboxid_and_stockname.update({delete_checkbox: (stockname, choice_number)})


    def set_signal(self):
        try:
            stockname = str.upper(self.ids.signal_textınput.text)
            stock = yf.Ticker(stockname)
            todays_data = stock.history(period='1d')
            currentvalue = float("{:.2f}".format(todays_data['Close'][0]))
            self.ids.signal_textınput.text_helper = ''
        except:
            self.ids.signal_textınput.text_helper = 'Invalid symbol'
        try:
            set_number = float(self.ids.set_number.text)
            self.ids.set_number.text_helper = ''
            self.ids.signal_textınput.text = ''
            self.ids.set_number.text = ''
        except:
            self.ids.set_number.text_helper = 'Invalid number'
        self.dict_signal_order.update({(stockname, set_number): currentvalue})
        self.dict_set_number.update({(stockname, set_number):'set_number'})

        symbol_label = MDLabel(text=stockname, theme_text_color="Custom", text_color=(1, 1, 1, 1))
        symbol_label.font_name = 'Timesi'
        symbol_set_number_label = MDLabel(text=str(set_number), theme_text_color="Custom", text_color=(1, 1, 1, 1))
        symbol_set_number_label.font_name = 'Timesi'
        symbol_inform_label = MDLabel(text=str('Setted Up '), theme_text_color="Custom", text_color=(139/255, 0, 0, 1))
        symbol_inform_label.font_name = 'Timesi'
        delete_checkbox = CheckBox()
        delete_checkbox.bind(active=self.on_delete_checkbox_active)
        signal_list_row = MDBoxLayout(orientation='horizontal', spacing=15)
        signal_list_row.add_widget(symbol_label)
        signal_list_row.add_widget(symbol_set_number_label)
        signal_list_row.add_widget(symbol_inform_label)
        signal_list_row.add_widget(delete_checkbox)
        self.ids.signal_view.add_widget(signal_list_row)

        self.dict_stockname_and_inform_label.update({(stockname, set_number): symbol_inform_label})
        self.dict_checkboxid_and_boxlayoutid.update({delete_checkbox: signal_list_row})
        self.dict_checkboxid_and_stockname.update({delete_checkbox: (stockname, set_number)})

    checkbox_ids_for_delete = []
    def on_delete_checkbox_active(self, check, value):
        if value:
            self.checkbox_ids_for_delete.append(check)
        else:
            self.checkbox_ids_for_delete.remove(check)

    def delete_row_of_signal(self):
        for check_box_id in self.checkbox_ids_for_delete:
            self.ids.signal_view.remove_widget(self.dict_checkboxid_and_boxlayoutid[check_box_id])
            self.dict_checkboxid_and_boxlayoutid.pop(check_box_id)
            symbol_list = self.dict_checkboxid_and_stockname[check_box_id]
            self.dict_checkboxid_and_stockname.pop(check_box_id)
            self.dict_stockname_and_inform_label.pop(symbol_list)
            self.dict_signal_order.pop(symbol_list)
            self.dict_set_number.pop(symbol_list)
        self.checkbox_ids_for_delete.clear()
        self.ids.signal_view.size_hint_y = len(self.dict_signal_order.keys())/8

    def control_signal_set_number(self, interval):
        for control_list in self.dict_signal_order.keys():
            if self.dict_set_number.get(control_list) == 'set_number':
                if self.dict_signal_order == {}:
                    pass
                elif self.dict_signal_order.get(control_list) > list(self.dict_signal_order.keys())[0][1]:
                    if list(self.dict_signal_order.keys())[0][1] >= float(self.get_stock_price(control_list[0])):
                        self.dict_stockname_and_inform_label.get(control_list).text = 'Alarm'
                        self.dict_stockname_and_inform_label.get(control_list).text_color = 0, 100/255, 0, 1
                    else:
                        pass
                else:
                    if float(self.get_stock_price(control_list[0])) >= list(self.dict_signal_order.keys())[0][1]:
                        self.dict_stockname_and_inform_label.get(control_list).text = 'Alarm'
                        self.dict_stockname_and_inform_label.get(control_list).text_color = 0, 100/255, 0, 1
                    else:
                        pass
            else:
                if self.dict_signal_order == {}:
                    pass
                elif self.dict_signal_order.get(control_list) > list(self.dict_signal_order.keys())[0][1]:
                    stock = yf.Ticker(list(self.dict_signal_order.keys())[0][0])
                    value = stock.info.get(self.dict_set_number.get(control_list))
                    if value >= float(self.get_stock_price(control_list[0])):
                        self.dict_stockname_and_inform_label.get(control_list).text = 'Alarm'
                        self.dict_stockname_and_inform_label.get(control_list).text_color = 0, 100/255, 0, 1
                    else:
                        pass
                else:
                    stock = yf.Ticker(list(self.dict_signal_order.keys())[0][0])
                    value = stock.info.get(self.dict_set_number.get(control_list))
                    if float(self.get_stock_price(control_list[0])) >= value:
                        self.dict_stockname_and_inform_label.get(control_list).text = 'Alarm'
                        self.dict_stockname_and_inform_label.get(control_list).text_color = 0, 100/255, 0, 1
                    else:
                        pass

    def drop_down_active_signal(self):
        selection_menu_items = [{"viewclass": "IconListItem",
                       "icon": "bell-ring-outline",
                       "height": dp(45),
                       "text": choice,
                       "on_release": lambda x=choice: self.set_signal_item(x), }
                      for choice in self.signal_choices]
        self.menu_signal = MDDropdownMenu(
            caller=self.ids.choice_signal,
            items=selection_menu_items,
            width_mult=4,
            max_height=dp(200)
        )

    def set_signal_item(self, text__item):
        self.ids.choice_signal.text = text__item
        self.menu_signal.dismiss()


# Filter Tab
    filter_list = []
    dict_sort_filter = {}
    selection_choices =['Increasing', 'Decreasing']
    filtering_choices = ['dividend yield', 'payout ratio', 'daily volume', 'beta', 'pe ratio', 'forward pe', 'market cap', 'profit margin', 'enterprise to revenue', 'enter prise to ebitda',
                         'shares outstanding', 'book value', 'shares short', 'shares percent shares out', 'last fiscalyear end', 'ınstitutions held', 'net ıncome to common', 'trailing eps',
                         'last dividend value', 'price to book', 'insiders held', 'next fiscal year end', 'most recent quarter', 'short ratio', 'shares short prev.', 'shares float',
                         'enterprise value', 'three year ave. return', 'last split date', 'last split factor', 'last dividend date', 'earning quarter growth', 'date short interest',
                         'peg ratio', 'short percent of float', 'shares short prior month']

    def filter_function_button(self):
        choice = self.ids.choice_filter.text
        selection = self.ids.selection_filter.text
        for symbol in self.filter_list:
            stock = yf.Ticker(symbol)
            data = stock.info
            stock_stats = {
                'dividend yield': data.get('trailingAnnualDividendYield'),
                'payout ratio': data.get('payoutRatio'),
                'daily volume': data.get('volume24Hr'),
                'beta': data.get('beta'),
                'pe ratio': data.get('trailingPE'),
                'forward pe': data.get('forwardPE'),
                'market cap': data.get('marketCap'),
                'profit margin': data.get('profitMargins'),
                'enterprise to revenue': data.get('enterpriseToRevenue'),
                'enter prise to ebitda': data.get('enterpriseToEbitda'),
                'shares outstanding': data.get('sharesOutstanding'),
                'book value': data.get('bookValue'),
                'shares short': data.get('sharesShort'),
                'shares percent shares out': data.get('sharesPercentSharesOut'),
                'last fiscalyear end': data.get('lastFiscalYearEnd'),
                'ınstitutions held': data.get('heldPercentInstitutions'),
                'net ıncome to common': data.get('netIncomeToCommon'),
                'trailing eps': data.get('trailingEps'),
                'last dividend value': data.get('lastDividendValue'),
                'price to book': data.get('priceToBook'),
                'insiders held': data.get('heldPercentInsiders'),
                'next fiscal year end': data.get('nextFiscalYearEnd'),
                'most recent quarter': data.get('mostRecentQuarter'),
                'short ratio': data.get('shortRatio'),
                'shares short prev.': data.get('sharesShortPreviousMonthDate'),
                'shares float': data.get('floatShares'),
                'enterprise value': data.get('enterpriseValue'),
                'three year ave. return': data.get('threeYearAverageReturn'),
                'last split date': data.get('lastSplitDate'),
                'last split factor': data.get('lastSplitFactor'),
                'last dividend date': data.get('lastDividendDate'),
                'earning quarter growth': data.get('earningsQuarterlyGrowth'),
                'date short interest': data.get('dateShortInterest'),
                'peg ratio': data.get('pegRatio'),
                'short percent of float': data.get('shortPercentOfFloat'),
                'shares short prior month': data.get('sharesShortPriorMonth'),
            }
            self.dict_sort_filter.update({symbol: []})
            try:
                if stock_stats.get(choice) == None:
                    if selection == 'Increasing':
                        self.dict_sort_filter[symbol].append(float(math.inf))
                    elif selection == 'Decreasing':
                        self.dict_sort_filter[symbol].append(float(0))
                else:
                    self.dict_sort_filter[symbol].append(float(stock_stats.get(choice)))
            except:
                print("Error occured; write the filter selection properly ")
        if selection == 'Increasing':
            sorted_list_filtered = sorted(self.dict_sort_filter.items(), key=operator.itemgetter(1))
        elif selection == 'Decreasing':
            sorted_list_filtered = sorted(self.dict_sort_filter.items(), key=operator.itemgetter(1), reverse=True)
        self.ids.filter.clear_widgets()
        for filter_row in sorted_list_filtered:
            filter_symbol_label = MDLabel(text=filter_row[0], theme_text_color="Custom", text_color=(1, 1, 1, 1))
            filter_symbol_label.font_name = 'Timesi'
            filter_value_label = MDLabel(text=str("{:.2f}".format(filter_row[1][0])), theme_text_color="Custom", text_color=(1, 1, 1, 1))
            filter_value_label.font_name = 'Timesi'
            filter_list_row = MDBoxLayout(orientation='horizontal', spacing=15)
            filter_list_row.add_widget(filter_symbol_label)
            filter_list_row.add_widget(filter_value_label)
            self.ids.filter.add_widget(filter_list_row)
        self.ids.filter_future.text = choice
        self.dict_sort_filter.clear()
        self.ids.choice_filter.text = ''
        self.ids.selection_filter.text = ''

    def drop_down_active(self):
        filter_menu_items = [{"viewclass": "IconListItem",
                       "icon": "filter-outline",
                       "height": dp(45),
                       "text": choice,
                       "on_release": lambda x=choice: self.set_filter_item(x), }
                      for choice in self.filtering_choices]
        self.menu_filter = MDDropdownMenu(
            caller=self.ids.choice_filter,
            items=filter_menu_items,
            width_mult=4,
            max_height=dp(200)
        )
        selection_menu_items = [{"viewclass": "IconListItem",
                       "icon": "filter-outline",
                       "height": dp(45),
                       "text": choice,
                       "on_release": lambda x=choice: self.set_selection_item(x), }
                      for choice in self.selection_choices]
        self.menu_selection = MDDropdownMenu(
            caller=self.ids.selection_filter,
            items=selection_menu_items,
            width_mult=3,
        )

    def set_filter_item(self, text__item):
        self.ids.choice_filter.text = text__item
        self.menu_filter.dismiss()

    def set_selection_item(self, text__item):
        self.ids.selection_filter.text = text__item
        self.menu_selection.dismiss()

    def filter_add(self):
        symbol = str.upper(self.ids.filter_symbol_textınput.text)
        if symbol in self.filter_list:
            self.ids.filter_symbol_textınput.helper_text = 'Already exist'
        else:
            try:
                stock = yf.Ticker(symbol).info
                self.filter_list.append(symbol)
                filter_symbol_label = MDLabel(text=symbol, theme_text_color="Custom", text_color=(1, 1, 1, 1))
                filter_symbol_label.font_name = 'Timesi'
                filter_list_row = MDBoxLayout(orientation='horizontal', spacing=15)
                filter_list_row.add_widget(filter_symbol_label)
                self.ids.filter.add_widget(filter_list_row)
                self.ids.filter_symbol_textınput.helper_text = ''
            except:
                self.ids.filter_symbol_textınput.helper_text = 'Write properly'
            self.ids.filter_symbol_textınput.text = ""

    def clear_filter(self):
        self.ids.filter.clear_widgets()
        self.filter_list = []
        self.ids.filter_future.text = 'Futures'


# Search Tab
    def clear_search(self):
        self.ids.search.clear_widgets()

    def search_profile(self):
        self.ids.search.clear_widgets()
        symbol = str.upper(self.ids.search_textınput.text)
        try:
            stock = yf.Ticker(symbol)
            data = stock.info
            stock_info = {
                'Ticker': data.get('symbol'),
                'Name': data.get('longName'),
                'Sector': data.get('sector'),
                'Employees': data.get('fullTimeEmployees'),
                'City': data.get('city'),
                'Phone': data.get('phone'),
                'State': data.get('state'),
                'Country': data.get('country'),
                'Website': data.get('website'),
                'Address': data.get('address1'),
                'Industry': data.get('industry'),
                'Market': data.get('market')
            }
            for key, value in stock_info.items():
                # forming the labels of key and value of the dict
                symbol_info = MDLabel(text=str(value), theme_text_color="Custom", text_color=(1, 1, 1, 1))
                symbol_info.font_name = 'Timesi'
                label = MDLabel(text=str.upper(key), theme_text_color="Custom", text_color=(1, 1, 1, 1))
                label.font_name = 'Timesi'
                # forming the box layout
                data_list_row = MDBoxLayout(orientation='horizontal', spacing=15)
                # adding the labels into the box layout
                data_list_row.add_widget(label)
                data_list_row.add_widget(symbol_info)
                # adding the box layout into grid layout named search in kivy
                self.ids.search.add_widget(data_list_row)
            self.ids.search_textınput.helper_text = ''
            self.ids.search.size_hint_y = 1.2
        except:
            self.ids.search_textınput.helper_text = 'Write properly'
        self.ids.search_textınput.text = ''

    def search_statistic(self):
        self.ids.search.clear_widgets()
        symbol = str.upper(self.ids.search_textınput.text)
        try:
            stock = yf.Ticker(symbol)
            data = stock.info
            stock_stats = {
                'Ticker': data.get('symbol'),
                'Name': data.get('longName'),
                'previous close': data.get('previousClose'),
                'market open': data.get('regularMarketOpen'),
                'dividend yield': data.get('trailingAnnualDividendYield'),
                'payout ratio': data.get('payoutRatio'),
                'daily volume': data.get('volume24Hr'),
                'day high': data.get('regularMarketDayHigh'),
                'day low': data.get('regularMarketDayLow'),
                'beta': data.get('beta'),
                'currency': data.get('currency'),
                'pe ratio': data.get('trailingPE'),
                'forward pe': data.get('forwardPE'),
                'market cap': data.get('marketCap'),
                'profit margin': data.get('profitMargins'),
                'enterprise to revenue': data.get('enterpriseToRevenue'),
                'enter prise to ebitda': data.get('enterpriseToEbitda'),
                'shares outstanding': data.get('sharesOutstanding'),
                'book value': data.get('bookValue'),
                'shares short': data.get('sharesShort'),
                'shares percent shares out': data.get('sharesPercentSharesOut'),
                'last fiscalyear end': data.get('lastFiscalYearEnd'),
                'ınstitutions held': data.get('heldPercentInstitutions'),
                'net ıncome to common': data.get('netIncomeToCommon'),
                'trailing eps': data.get('trailingEps'),
                'last dividend value': data.get('lastDividendValue'),
                'price to book': data.get('priceToBook'),
                'insiders held': data.get('heldPercentInsiders'),
                'next fiscal year end': data.get('nextFiscalYearEnd'),
                'most recent quarter': data.get('mostRecentQuarter'),
                'short ratio': data.get('shortRatio'),
                'shares short prev.': data.get('sharesShortPreviousMonthDate'),
                'shares float': data.get('floatShares'),
                'enterprise value': data.get('enterpriseValue'),
                'three year ave. return': data.get('threeYearAverageReturn'),
                'last split date': data.get('lastSplitDate'),
                'last split factor': data.get('lastSplitFactor'),
                'last dividend date': data.get('lastDividendDate'),
                'earning quarter growth': data.get('earningsQuarterlyGrowth'),
                'date short interest': data.get('dateShortInterest'),
                'peg ratio': data.get('pegRatio'),
                'short percent of float': data.get('shortPercentOfFloat'),
                'shares short prior month': data.get('sharesShortPriorMonth'),
                'regular market price': data.get('regularMarketPrice')
            }
            for key, value in stock_stats.items():
                # forming the labels of key and value of the dict
                symbol_info = MDLabel(text=str(value), theme_text_color="Custom", text_color=(1, 1, 1, 1))
                symbol_info.font_name = 'Timesi'
                label = MDLabel(text=str.upper(key), theme_text_color="Custom", text_color=(1, 1, 1, 1))
                label.font_name = 'Timesi'
                # forming the box layout
                data_list_row = MDBoxLayout(orientation='horizontal', spacing=15)
                # adding the labels into the box layout
                data_list_row.add_widget(label)
                data_list_row.add_widget(symbol_info)
                # adding the box layout into grid layout named search in kivy
                self.ids.search.add_widget(data_list_row)
            self.ids.search_textınput.helper_text = ''
            self.ids.search.size_hint_y = 4.2
        except:
            self.ids.search_textınput.helper_text = 'Write properly'
        self.ids.search_textınput.text = ''


# Setting Tab
    def change_password(self):
        if self.ids.setting_input.text == "":
            pass
        else:
            mydatabase().update_password(self.ids.setting_input.text)
            self.ids.setting_input.text = ''

    def log_out(self):
        self.ids.screener.clear_widgets()
        self.dict_checkbox_id_and_boxlayout_id = {}
        self.dict_checkbox_id_and_symbol = {}
        self.dict_symbol_and_currentvalue_label_id = {}
        self.dict_symbol_and_daily_change_label_id = {}
        self.list_screener_symbol = []
        self.check_box_ids_for_delete = []


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.screen_one = ObjectProperty(None)
        self.screen_two = ObjectProperty(None)
        self.screen_three = ObjectProperty(None)


class Financeapp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        return MyScreenManager()


Financeapp().run()

