import sys
import json
import pickle
import copy
from Demos.win32gui_menu import MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QGridLayout, QLineEdit, QMessageBox, QFileDialog, QColorDialog
from PyQt6.QtGui import QBrush, QPalette, QIcon
from PyQt6.QtCore import QSize, QObject, pyqtSignal
import shutil
import os
from PyQt6.QtCore import Qt, QObject, QUrl
from PyQt6.uic.properties import QtWidgets
from Tools.demo.mcast import receiver
from Tools.scripts.cleanfuture import recurse
from blinker import Signal
from click import confirm
import socket
import threading
from jupyter_client.session import Session
from psutil import users
from pyexpat.errors import messages
from pygments.styles.dracula import foreground
import sqlite3
from enum import unique
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from werkzeug.serving import select_address_family


class User:
    def __init__(self, username: str, password: str, phone_number: str, picture_pro = None):
        self.__username = username
        self.__password = password
        self.__phone_number = phone_number
        self.color_profile = None
        self.picture_pro = picture_pro   # "C:\Final_Project\kingB.png"
        self.bio_graph = None
        self.contacts = []
        self.message = {}
        if self not in users:
            users.append(self)
    def get_info(self):
        return {"username": self.__username, "password": self.__password, "phon number": self.__phone_number}
    def change_info(self, username, phone_number, password):
        self.__username = username
        self.__password = password
        self.__phone_number = phone_number


#Create a new table with SQlite:
Base = declarative_base()
engine = create_engine("sqlite:///bvbvbvbvnvx.db")
class UserSqlite(Base):
    __tablename__ = "users QT6 sql3"
    username: Mapped[str] = mapped_column(primary_key = True)
    password: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    picture_pro: Mapped[str] = mapped_column(nullable = True)
    color_profile: Mapped[str] = mapped_column(nullable = True)
    bio_graph: Mapped[str] = mapped_column(nullable = True)
    contacts: Mapped[str] = mapped_column()
    message: Mapped[str] = mapped_column()

# Create session:
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind= engine)
session = SessionLocal()
session.commit()

# Load date:
users = []
usersSQl = session.query(UserSqlite).all()
for user in usersSQl:
    new_user = User(user.username, user.password, user.phone_number, user.picture_pro)
    new_user.color_profile = user.color_profile
    new_user.bio_graph = user.bio_graph
    message = json.loads(user.message)
    new_user.message = message
    new_user.contacts = json.loads(user.contacts)


for user in users:
    contacts = []
    for username in user.contacts:
        for user1 in users:
            if user1.get_info()['username'] == username:
                contacts.append(user1)
    user.contacts = contacts



class EntryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.resize(600, 600)
        self.picture = QPixmap("C:\Final_Project\Intro.jpg")
        self.label0 = QLabel(self)
        self.label0.resize(600 ,600)
        self.label0.setPixmap(self.picture)
        self.label0.setScaledContents(True)
        self.overlay_widget = QWidget(self)
        self.overlay_widget.resize(600, 600)
        self.overlay_lay = QGridLayout(self.overlay_widget)
        self.overlay_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.qline1 = QLineEdit()
        self.qline2 = QLineEdit()
        self.label1 = QLabel("Username:")
        self.label2 = QLabel("Password:")
        self.empty_label = QLabel("")
        self.button1 = QPushButton("Sign In")
        self.button1.clicked.connect(self.go_to_sign_in)
        self.button2 = QPushButton("Go to Sign Up")
        self.button2.clicked.connect(self.sign_up)
        self.overlay_lay.addWidget(self.label1, 0, 1)
        self.overlay_lay.addWidget(self.qline1, 1, 1)
        self.overlay_lay.addWidget(self.label2, 2, 1)
        self.overlay_lay.addWidget(self.qline2, 3, 1)
        self.overlay_lay.addWidget(self.button1, 4, 0)
        self.overlay_lay.addWidget(self.button2, 4, 2)
        self.overlay_lay.addWidget(self.empty_label, 5, 1)

    def sign_up(self):
        self.window_sign_up = SignUp()
        self.window_sign_up.show()

    def go_to_sign_in(self):
        user_name = self.qline1.text()
        password = self.qline2.text()
        self.main_user = None
        if user_name and password:
            for user in users:
                if user.get_info()["username"] == user_name and user.get_info()["password"] == password:
                    self.main_user = user
                    self.messenger_window = MessengerPanel(self.main_user)
                    self.messenger_window.show()
                    break
            if not self.main_user:
                self.empty_label.setText("Error: <<The information is not correct>>")
        else:
            self.empty_label.setText("Error: <<Please enter both username and password>>")
        self.empty_label.setStyleSheet("color: red; font-size: 13px;")


class SignUp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.resize(600, 600)
        self.picture = QPixmap("C:\Final_Project\Intro.jpg")
        self.label0 = QLabel(self)
        self.label0.resize(600, 600)
        self.label0.setPixmap(self.picture)
        self.label0.setScaledContents(True)
        self.overlay_widget = QWidget(self)
        self.overlay_widget.resize(600 ,600)
        self.overlay_lay = QGridLayout(self.overlay_widget)
        self.overlay_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.qline1 = QLineEdit()
        self.qline2 = QLineEdit()
        self.qline3 = QLineEdit()
        self.qline4 = QLineEdit()
        self.label1 = QLabel("Phone Number:")
        self.label2 = QLabel("User name:")
        self.overlay_lay.addWidget(self.qline1, 1, 0)
        self.label3 = QLabel("Password:")
        self.label4 = QLabel("Confirm Password:")
        self.overlay_lay.addWidget(self.label4, 6, 0)
        self.empty_label = QLabel("")
        self.select_picture_bt = QPushButton("Select picture")
        self.select_picture_bt.clicked.connect(self.select_picture)
        self.button1 = QPushButton("Sign Up")
        self.button1.clicked.connect(self.sign_up)
        self.button2 = QPushButton("Go to Sign In")
        self.button2.clicked.connect(self.go_to_sign_in)
        self.label5 = QLabel("Write your bio: ")
        self.qline5 = QLineEdit()
        self.overlay_lay.addWidget(self.label1, 0, 0)
        self.overlay_lay.addWidget(self.label2, 2, 0)
        self.overlay_lay.addWidget(self.label3, 4, 0)
        self.overlay_lay.addWidget(self.qline2, 3, 0)
        self.overlay_lay.addWidget(self.qline3, 5, 0)
        self.overlay_lay.addWidget(self.qline4, 7, 0)
        self.overlay_lay.addWidget(self.label5, 8, 0)
        self.overlay_lay.addWidget(self.qline5, 9, 0)
        self.overlay_lay.addWidget(self.select_picture_bt, 10, 0)
        self.overlay_lay.addWidget(self.button1, 11, 0)
        self.overlay_lay.addWidget(self.button2, 11, 1)
        self.overlay_lay.addWidget(self.empty_label, 12, 0)
        self.picture_select = ""

    def sign_up(self):
        phone_number = self.qline1.text()
        user_name = self.qline2.text()
        password = self.qline3.text()
        confirm_password = self.qline4.text()
        bio = self.qline5.text()
        if phone_number and user_name and password:
            if password == confirm_password:
                is_existing = 0
                for user in users:
                    if user_name == user.get_info()["username"] or phone_number == user.get_info()["phon number"]:
                        self.empty_label.setText("Error: <<The phone number or user name has used before it>>")
                        is_existing = 1
                if not is_existing:
                    if "C" in self.picture_select:
                        new_user = User(user_name, password, phone_number, self.picture_select)
                    else:
                        new_user = User(user_name, password, phone_number)
                        new_user.color_profile = "white"
                    new_user.bio_graph = bio
                    self.new_user = new_user
                    self.empty_label.setText("<<Sign Up is Successfully!>>")
            else:
                self.empty_label.setText("Error: <<The password not equal by confirm password>>")
        else:
            self.empty_label.setText("Error: <<Please enter your information complete>>")
        self.empty_label.setStyleSheet("color: red; font-size: 13px;")

    def go_to_sign_in(self):
        self.window_sign_up = EntryWindow()
        self.window_sign_up.show()

    def select_picture(self):
        self.picture_select, _ = QFileDialog.getOpenFileName(self, "Select the Picture of Profile", "",
                                                 "All Files (*);; Image (*.png, *jpg)")
        print(self.picture_select)

    def update_new_user(self):
        pass


class MessengerPanel(QMainWindow):
    messages_rec = pyqtSignal(str)
    picture_rec = pyqtSignal(str)
    pdf_rec = pyqtSignal(str)
    def __init__(self, main_user):
        super().__init__()
        self.main_user = main_user
        self.setWindowTitle(f"Welcome {self.main_user.get_info()['username']}")
        self.resize(800, 800)
        self.move(400, 0)
        self.picture_blue = QPixmap(r"C:\Final_Project\Intro.jpg")
        self.picture_green = QPixmap(r"C:\Final_Project\Back3.jpg")
        self.l0 = QVBoxLayout()  # Main Layout
        # set the background picture
        self.lb0 = QLabel(self)
        self.lb0.setPixmap(self.picture_blue)
        self.lb0.resize(800, 800)
        self.lb0.setScaledContents(True)
        self.l0.addWidget(self.lb0)
        # New Widget
        self.wg1 = QWidget(self)
        self.wg1.setGeometry(310, 15, 485, 700)
        # set the picture for wg1
        self.wg1.lb1 = QLabel(self.wg1)
        self.wg1.lb1.setPixmap(self.picture_green)
        self.wg1.lb1.setFixedSize(485, 700)
        self.wg1.lb1.setScaledContents(True)
        # widget on widget
        self.wg1.wg11 = QWidget(self.wg1)
        self.wg1.wg11.resize(485, 700)
        self.wg1.wg11.ly = QGridLayout(self.wg1.wg11)
        self.wg1.wg11.ly.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wg1.wg11.setLayout(self.wg1.wg11.ly)
        self.wg0 = QWidget(self)
        self.wg0.ly = QGridLayout()
        self.wg0.resize(485, 50)
        self.wg0.move(310, 730)
        self.qline1 = QLineEdit()
        self.button01 = QPushButton("Send")
        self.button2 = QPushButton("Picture")
        self.button_pdf = QPushButton("PDF")
        self.button01.clicked.connect(self.send_button)
        self.button2.clicked.connect(self.send_picture)
        self.button_pdf.clicked.connect(self.send_file_PDF)
        self.button2.setStyleSheet("background-color: red")
        self.button01.setStyleSheet("background-color: green")
        self.button_pdf.setStyleSheet("background-color: yellow")
        self.wg0.ly.addWidget(self.qline1, 0, 0)
        self.wg0.ly.addWidget(self.button01, 0, 1)
        self.wg0.ly.addWidget(self.button2, 0, 2)
        self.wg0.ly.addWidget(self.button_pdf, 0, 3)
        self.wg0.setLayout(self.wg0.ly)
        self.l0.addWidget(self.wg0)
        self.l0.addWidget(self.wg1)
        # New Widget
        self.wg2 = QWidget(self)
        self.wg2.resize(300, 650)
        self.wg2.move(5, 90)
        self.wg2.background = QLabel(self.wg2)
        self.picture_lightblue = QPixmap("C:\Final_Project\Back2.jpg")
        self.wg2.background.setPixmap(self.picture_lightblue)
        self.wg2.background.resize(300, 650)
        self.wg2.background.setScaledContents(True)
        self.wg2.ly = QGridLayout()
        i = 0
        for contact in self.main_user.contacts:
            if contact.picture_pro:
                picture = QPixmap(contact.picture_pro)
                self.wg2.button = QPushButton()
                self.wg2.button.setIcon(QIcon(picture))
            else:
                color = contact.color_profile
                self.wg2.button = QPushButton(contact.get_info()["username"])
                self.wg2.button.setStyleSheet(f"background: {color};")
            self.wg2.button.setFixedSize(60, 60)
            self.wg2.button.setIconSize(QSize(60, 60))
            self.wg2.ly.addWidget(self.wg2.button, i, 0)
            self.wg2.username = QLabel(f"{contact.get_info()['username']}")
            self.wg2.username.setStyleSheet("color: white; font-size: 14px;")
            self.wg2.ly.addWidget(self.wg2.username, i, 1)
            self.wg2.button.clicked.connect(lambda checked=False, c = contact: self.open_chat(c))
            i += 1
        self.wg2.ly.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wg2.setLayout(self.wg2.ly)
        self.l0.addWidget(self.wg2)
        # add buttons for profile and setting
        self.picture_setting = QPixmap(r"C:\Final_Project\setting.png")
        self.button1 = QPushButton("", self)
        self.button1.setIcon(QIcon(self.picture_setting))
        self.button1.setIconSize(QSize(60, 60))
        self.button1.setGeometry(5, 5, 60, 60)
        self.button1.clicked.connect(self.setting)
        self.l0.addWidget(self.button1)
        #
        if self.main_user.picture_pro != None:
            self.button2 = QPushButton("", self)
            self.button2.setIcon(QIcon(self.main_user.picture_pro))
            self.button2.setIconSize(QSize(60, 60))
        else:
            color = self.main_user.color_profile
            self.button2 = QPushButton(f"{self.main_user.get_info()['username']}", self)
            self.button2.setStyleSheet(f"background-color: {color};")
        self.button2.setGeometry(85, 5, 60, 60)
        self.l0.addWidget(self.button2)
        self.button2.clicked.connect(self.view_profile)
        #
        self.contact_picture = QPixmap(r"C:\Final_Project\Contact.png")
        self.button3 = QPushButton("", self)
        self.button3.setIcon(QIcon(self.contact_picture))
        self.button3.setIconSize(QSize(60, 60))
        self.button3.setGeometry(165, 5, 60, 60)
        self.button3.clicked.connect(self.add_contact)
        self.l0.addWidget(self.button3)
        #
        self.setLayout(self.l0)
        # SOCKET:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 12345))
        # THREAD:
        self.receive_thread = threading.Thread(target= self.receive_msg, daemon= True)
        self.receive_thread.start()
        # create a signal for add message to chat widget:
        self.messages_rec.connect(self.add_message_to_chat)
        # create a signal for add picture to chat widget:
        self.picture_rec.connect(self.add_picture_to_chat)
        # create a signal for add pdf to chat widget:
        self.pdf_rec.connect(self.add_pdf_to_chat)
        # reloading messages for each contact's page according to contact's messages:
        try:
            for contact in self.main_user.contacts:
                if len(self.main_user.message[contact.get_info()['username']]) < len(contact.message[self.main_user.get_info()['username']]):
                    self.main_user.message[contact.get_info()['username']] = copy.deepcopy(contact.message[self.main_user.get_info()['username']])
                    # To correct sender and receiver sections:
                    for message_ in range(len(self.main_user.message[contact.get_info()['username']])):
                        if "=" not in self.main_user.message[contact.get_info()['username']][message_]:     #  if not been picture
                            if self.main_user.message[contact.get_info()['username']][message_].endswith("(Me)"):
                                message_list = self.main_user.message[contact.get_info()['username']][message_].split("(")
                                self.main_user.message[contact.get_info()['username']][message_] = message_list[0][:-1] + f" ({contact.get_info()['username']}) ->{self.main_user.get_info()['username']}"
                            if self.main_user.message[contact.get_info()['username']][message_].endswith(f"->{contact.get_info()['username']}"):
                                message_list = self.main_user.message[contact.get_info()['username']][message_].split("(")
                                self.main_user.message[contact.get_info()['username']][message_] = message_list[0][:-2] + "  (Me)"
                        else:   # if been a picture
                            if self.main_user.message[contact.get_info()['username']][message_].endswith("=Me= "):
                                message_list = self.main_user.message[contact.get_info()['username']][message_].split("=")
                                self.main_user.message[contact.get_info()['username']][message_] = message_list[0] + f"={contact.get_info()['username']}=>{self.main_user.get_info()['username']}"
                            if self.main_user.message[contact.get_info()['username']][message_].endswith(f"=>{contact.get_info()['username']}"):
                                message_list = self.main_user.message[contact.get_info()['username']][message_].split("=")
                                self.main_user.message[contact.get_info()['username']][message_] = message_list[0] + "=Me= "
        except:
            pass

    def view_profile(self):
        self.view_profile_window = ViewProfile(self.main_user)
        self.view_profile_window.show()

    def setting(self):
        self.setting_window = SettingPanel(self.main_user, self)
        self.setting_window.show()

    def add_contact(self):
        self.contact_window = ContactPanel(self.main_user, self)
        self.contact_window.show()

    def open_chat(self, contact):
        self.contact = contact
        for i in reversed(range(self.wg1.wg11.ly.count())):
            label = self.wg1.wg11.ly.itemAt(i).widget()
            if label:
                label.deleteLater()
        i = 0
        for message in self.main_user.message[f"{contact.get_info()['username']}"]:
            if "=" not in message:        # if you want sent message or pdf:
                message_split = message.split("(")
                if message_split[0].endswith("pdf  "):   # if sent a pdf
                    self.add_pdf_to_chat(message)
                    i += 1
                else:     # if sent a message
                    new_label = QLabel(message)
                    new_label.setStyleSheet("color: white; font-size: 24;")
                    self.wg1.wg11.ly.addWidget(new_label, i, 0)
                    i += 1
            else:        # if you want sent picture:
                new_label_picture = QLabel("")
                new_label_contact = QLabel("")
                addr, contact, rec = message.split("=")
                new_label_contact.setText(contact)
                new_label_contact.setStyleSheet("color: white; font-size: 25;")
                picture = QPixmap(addr)
                new_label_picture.setPixmap(picture)
                new_label_picture.setFixedSize(120, 120)
                new_label_picture.setScaledContents(True)
                self.wg1.wg11.ly.addWidget(new_label_picture, i, 0)
                self.wg1.wg11.ly.addWidget(new_label_contact, i, 1)
                i += 1

    def add_message_to_chat(self, message):
        self.new_msg = QLabel(message)
        self.new_msg.setStyleSheet("color: white; font-size: 25")
        count_of_message = len(self.main_user.message[f"{self.contact.get_info()['username']}"])
        self.wg1.wg11.ly.addWidget(self.new_msg, count_of_message, 0)

    def add_pdf_to_chat(self, message):
        self.new_msg = QLabel(message)
        self.new_msg.setStyleSheet("color: white; font-size: 25")
        count_of_message = len(self.main_user.message[f"{self.contact.get_info()['username']}"])
        self.wg1.wg11.ly.addWidget(self.new_msg, count_of_message, 0)
        self.open_pdf = QPushButton("open")
        self.open_pdf.clicked.connect(lambda _, m=message: self.open_pdf_url(m))
        self.open_pdf.setStyleSheet("background-color: lightgreen; font-size: 25")
        self.wg1.wg11.ly.addWidget(self.open_pdf, count_of_message, 1)


    def add_picture_to_chat(self, addr_picture_sender):
        self.label_new_picture = QLabel("")
        addr_picture, sender, rec = addr_picture_sender.split("=")
        self.new_picture = QPixmap(addr_picture)
        new_sender_label = QLabel(sender)
        new_sender_label.setStyleSheet("color: white; font-size: 25")
        self.label_new_picture.setPixmap(self.new_picture)
        self.label_new_picture.setFixedSize(120, 120)
        self.label_new_picture.setScaledContents(True)
        count_of_message = len(self.main_user.message[f"{self.contact.get_info()['username']}"])
        self.wg1.wg11.ly.addWidget(self.label_new_picture, count_of_message, 0)
        self.wg1.wg11.ly.addWidget(new_sender_label, count_of_message, 1)

    def send_button(self):
        try:
            message = self.qline1.text()
            self.qline1.clear()
            self.contact.message[f"{self.main_user.get_info()['username']}"].append(message + f"  ({self.main_user.get_info()['username']})")
            self.main_user.message[f"{self.contact.get_info()['username']}"].append(message + "  (Me)")
            self.client_socket.send((message + f"  ({self.main_user.get_info()['username']}) ->{self.contact.get_info()['username']}").encode())
            self.add_message_to_chat(message + "  (Me)")
        except:
            label = QLabel("Error: Your contact don't have you in the his contact list!")
            label.setStyleSheet("color: red; font-size: 25")
            self.wg1.wg11.ly.addWidget(label, 0, 0)

    def receive_msg(self):
        while 1:
            msg = self.client_socket.recv(1024).decode()
            if "=" not in msg:    # if sent a message or a pdf:
                msg_split = msg.split("(")
                if msg_split[0].endswith("pdf  "):    # if sent a pdf file
                    sender_msg = msg.split("(")[1]
                    sender_msg = sender_msg.split(")")[0]
                    reciever_msg = msg.split(">")[1]
                    for user in users:
                        if user.get_info()['username'] == sender_msg:
                            sender_msg = user
                    if self.main_user.get_info()['username'] == reciever_msg:
                        self.main_user.message[f"{sender_msg.get_info()['username']}"].append(msg)
                        if sender_msg == self.contact:
                            self.pdf_rec.emit(msg)

                else:       # if sent a messgae
                    sender_msg = msg.split("(")[1]
                    sender_msg = sender_msg.split(")")[0]
                    reciever_msg = msg.split(">")[1]
                    for user in users:
                        if user.get_info()['username'] == sender_msg:
                            sender_msg = user
                    if self.main_user.get_info()['username'] == reciever_msg:
                        self.main_user.message[f"{sender_msg.get_info()['username']}"].append(msg)
                        if sender_msg == self.contact:
                            self.messages_rec.emit(msg)


            else:       # if sent a picture :
                addr, sender, reciever = msg.split("=")
                reciever_msg = reciever[1:]
                for user in users:
                    if user.get_info()['username'] == sender:
                        sender_msg = user
                print(f"{sender_msg.get_info()['username']} sent a picture or pdf")
                if self.main_user.get_info()['username'] == reciever_msg:
                    self.main_user.message[f"{sender_msg.get_info()['username']}"].append(msg)
                    if sender == self.contact.get_info()['username']:
                        print(addr + f"{sender}")
                        self.picture_rec.emit(addr + f"={sender}= ")


    def send_picture(self):
        try:
            self.picture_sendly, _ = QFileDialog.getOpenFileName(self, "Select the Picture of Profile", "",
                                                             "All Files (*);; Image (*.png, *jpg)")
            self.contact.message[f"{self.main_user.get_info()['username']}"].append(self.picture_sendly + f"={self.main_user.get_info()['username']}= ")
            self.main_user.message[f"{self.contact.get_info()['username']}"].append(self.picture_sendly + "=Me= ")
            self.picture_rec.emit(self.picture_sendly + "=Me= ")
            self.client_socket.send((self.picture_sendly + f"={self.main_user.get_info()['username']}=>{self.contact.get_info()['username']}").encode())
        except:
            label = QLabel("Error: Your contact don't have you in the his contact list!")
            label.setStyleSheet("color: red; font-size: 21;")
            self.wg1.wg11.ly.addWidget(label, 0, 0)


    def send_file_PDF(self):
        try:
            self.file_sendly, _ = QFileDialog.getOpenFileName(self, "Select the PDF for send", "", "All Files (*);; ODF Files (*pdf)")
            self.contact.message[f"{self.main_user.get_info()['username']}"].append(
                self.file_sendly + f"  ({self.main_user.get_info()['username']})")
            self.main_user.message[f"{self.contact.get_info()['username']}"].append(self.file_sendly + "  (Me)")
            self.client_socket.send((self.file_sendly + f"  ({self.main_user.get_info()['username']}) ->{self.contact.get_info()['username']}").encode())
            self.add_pdf_to_chat(self.file_sendly + "  (Me)")
        except:
            label = QLabel("Error: Your contact don't have you in the his contact list!")
            label.setStyleSheet("color: red; font-size: 21;")
            self.wg1.wg11.ly.addWidget(label, 0, 0)


    def open_pdf_url(self, addr):
        addr = addr.split("(")[0][:-2]
        os.startfile(addr)



class ViewProfile(QMainWindow):
    def __init__(self, main_user):
        super().__init__()
        self.main_user = main_user
        self.setWindowTitle("Your Profile")
        self.setGeometry(550, 150, 400, 570)
        self.main_ly = QVBoxLayout()
        # backgrond:
        self.label1 = QLabel(self)
        self.picture_blue = QPixmap(r"C:\Final_Project\Intro.jpg")
        self.label1.setPixmap(self.picture_blue)
        self.label1.resize(400, 570)
        self.label1.setScaledContents(True)
        self.main_ly.addWidget(self.label1)
        #
        self.label2 = QLabel(self)
        if self.main_user.picture_pro != None:
            self.label2= QLabel(self)
            self.profile_picture = QPixmap(self.main_user.picture_pro)
            self.label2.setPixmap(self.profile_picture)
            self.label2.setScaledContents(True)
            self.label2.setGeometry(125, 30, 150, 150)
            self.main_ly.addWidget(self.label2)
        else:
            self.wg1 = QWidget(self)
            self.wg1.ly1 = QVBoxLayout()
            self.wg1.resize(150, 150)
            self.wg1.label2 = QLabel(f"{self.main_user.get_info()['username']}",self)
            self.wg1.label2.setStyleSheet("color: black; font-size: 34px; font-weight: bold;")
            self.wg1.setStyleSheet(f"background-color: {self.main_user.color_profile};")
            self.wg1.ly1.addWidget(self.wg1.label2)
            self.wg1.setLayout(self.wg1.ly1)
            self.wg1.move(125, 30)
            self.wg1.ly1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_ly.addWidget(self.wg1)
        self.wg2 = QWidget(self)
        self.wg2.resize(400, 150)
        self.wg2.move(0, 200)
        self.wg2.ly2 = QVBoxLayout()
        self.wg2.label3 = QLabel(f"User name: {self.main_user.get_info()['username']}", self)
        self.wg2.label3.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.wg2.label4 = QLabel(f"Phone number: {self.main_user.get_info()['phon number']}", self)
        self.wg2.label4.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.wg2.ly2.addWidget(self.wg2.label3)
        self.wg2.ly2.addWidget(self.wg2.label4)
        try:
            if self.main_user.bio_graph:
                self.wg2.label5 = QLabel(f"Bio: {self.main_user.bio_graph}")
                self.wg2.label5.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
                self.wg2.ly2.addWidget(self.wg2.label5)
        except:
            pass
        self.wg2.setLayout(self.wg2.ly2)
        self.wg2.ly2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_ly.addWidget(self.wg2)
        #
        self.setLayout(self.main_ly)


class SettingPanel(QMainWindow):
    def __init__(self, main_user, before_panel):
        super().__init__()
        self.main_user = main_user
        self.before_panel = before_panel
        self.setWindowTitle("Setting")
        self.resize(420, 670)
        # Set Background
        self.background_label = QLabel(self)
        self.red_picture = QPixmap("C:\Final_Project\Back4.jpg")
        self.background_label.setPixmap(self.red_picture)
        self.background_label.resize(420, 670)
        self.background_label.setScaledContents(True)
        self.main_lay = QVBoxLayout()
        #
        if self.main_user.picture_pro != None:
            self.label1= QLabel(self)
            self.profile_picture = QPixmap(self.main_user.picture_pro)
            self.label1.setPixmap(self.profile_picture)
            self.label1.setScaledContents(True)
            self.label1.setGeometry(135, 30, 150, 150)
            self.main_lay.addWidget(self.label1)
        else:
            self.wg1 = QWidget(self)
            self.wg1.ly1 = QVBoxLayout()
            self.wg1.resize(150, 150)
            self.wg1.label2 = QLabel(f"{self.main_user.get_info()['username']}",self)
            self.wg1.label2.setStyleSheet("color: black; font-size: 20px; font-weight: bold;")
            self.wg1.setStyleSheet(f"background-color: {self.main_user.color_profile};")
            self.wg1.ly1.addWidget(self.wg1.label2)
            self.wg1.setLayout(self.wg1.ly1)
            self.wg1.move(135, 30)
            self.wg1.ly1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_lay.addWidget(self.wg1)
        #
        self.wg2 = QWidget(self)
        self.wg2.ly2 = QGridLayout()
        self.wg2.resize(320, 400)
        self.wg2.move(50, 210)
        #self.wg2.setStyleSheet("background-color: white;")
        self.main_lay.addWidget(self.wg2)
        self.button1 = QPushButton("Change color", self)
        if self.main_user.picture_pro == None:
            self.button1.clicked.connect(self.change_color)
        self.button2 = QPushButton("Change Picture")
        if self.main_user.color_profile == None:
            self.button2.clicked.connect(self.change_picture)
        self.label2 = QLabel("User name:", self)
        self.label2.setStyleSheet("color: white; font-size: 12px")
        self.qline1 = QLineEdit()
        self.label3 = QLabel("Phone number:", self)
        self.label3.setStyleSheet("color: white; font-size: 12px")
        self.qline2 = QLineEdit()
        self.label4 = QLabel("New Password:", self)
        self.label4.setStyleSheet("color: white; font-size: 12px")
        self.qline3 = QLineEdit()
        self.label5 = QLabel("Confirm New Password:", self)
        self.label5.setStyleSheet("color: white; font-size: 12px")
        self.qline4 = QLineEdit()
        self.button3 = QPushButton("Save Changes:", self)
        self.button3.clicked.connect(self.save_change)
        self.label6 = QLabel("Bio:")
        self.label6.setStyleSheet("color: white; font-size: 12px")
        self.qline5 = QLineEdit()
        self.change_bio_bt = QPushButton("Change Bio")
        self.change_bio_bt.clicked.connect(self.change_bio)
        self.empty_label = QLabel("", self)
        self.empty_label.setStyleSheet("color: red; font-size: 13px; font-weight: bond;")
        self.wg2.ly2.addWidget(self.button1, 0, 0)
        self.wg2.ly2.addWidget(self.button2, 1, 0)
        self.wg2.ly2.addWidget(self.label2, 2, 0)
        self.wg2.ly2.addWidget(self.qline1, 3, 0)
        self.wg2.ly2.addWidget(self.label3, 4, 0)
        self.wg2.ly2.addWidget(self.qline2, 5, 0)
        self.wg2.ly2.addWidget(self.label4, 6, 0)
        self.wg2.ly2.addWidget(self.qline3, 7, 0)
        self.wg2.ly2.addWidget(self.label5, 8, 0)
        self.wg2.ly2.addWidget(self.qline4, 9, 0)
        self.wg2.ly2.addWidget(self.button3, 10, 0)
        self.wg2.ly2.addWidget(self.label6, 12, 0)
        self.wg2.ly2.addWidget(self.qline5, 13, 0)
        self.wg2.ly2.addWidget(self.change_bio_bt, 14, 0)
        self.wg2.ly2.addWidget(self.empty_label, 11, 0)
        self.wg2.setLayout(self.wg2.ly2)
        #
        self.setLayout(self.main_lay)
    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.wg1.setStyleSheet(f"background-color: {color.name()};")
            self.main_user.color_profile = color.name()
        self.before_panel.button2.setStyleSheet(f"background-color: {self.main_user.color_profile};")

    def change_picture(self):
        picture, _ = QFileDialog.getOpenFileName(self.wg2, "Select the Picture of Profile", "", "All Files (*);; Image (*.png, *jpg)")
        self.main_user.picture_pro = picture
        self.profile_picture = QPixmap(self.main_user.picture_pro)
        self.before_panel.button2.setIcon(QIcon(self.main_user.picture_pro))
        self.before_panel.button2.setIconSize(QSize(60, 60))
        self.label1.setPixmap(self.profile_picture)

    def save_change(self):
        before_username = self.main_user.get_info()['username']
        user_name = self.qline1.text()
        phone_number = self.qline2.text()
        password = self.qline3.text()
        confirm_password = self.qline4.text()
        if phone_number and user_name and password:
            if password == confirm_password:
                is_existing = 0
                for user in users:
                    if user_name == user.get_info()["username"] or phone_number == user.get_info()["phon number"]:
                        self.empty_label.setText("Error: phone number or user name has used before it")
                        is_existing = 1
                if not is_existing:
                    self.main_user.change_info(user_name, phone_number, password)
                    for contact in self.main_user.contacts:
                        try:                             # change the username in messages for contacts:
                            contact.message[user_name] = contact.message[before_username]
                            #
                            empty_list = []
                            for message in contact.message[user_name]:
                                if "=" not in message:
                                    message_split = message.split("(")
                                    if message_split[0].endswith("pdf  "):      # if that's pdf file
                                        pass

                                    else:            # if that's message
                                        split_message = message.split()
                                        correct_message = ""
                                        for word in split_message:
                                            if word == f"({before_username})":
                                                correct_message += f"({user_name})"
                                            else:
                                                correct_message += word
                                                correct_message += " "
                                        empty_list.append(correct_message)

                                else:
                                    split_message = message.split("=")
                                    correct_message = message
                                    if split_message[1] == before_username:
                                        correct_message = ""
                                        correct_message += split_message[0]
                                        correct_message += "="
                                        correct_message += user_name
                                        correct_message += "="
                                        correct_message += split_message[2]
                                    empty_list.append(correct_message)
                            contact.message[user_name] = empty_list
                            #
                        except: # if you not been contact for he:
                            pass
                    if not self.main_user.picture_pro:
                        self.wg1.label2.setText(f"{self.main_user.get_info()['username']}")
                        self.before_panel.button2.setText(f"{self.main_user.get_info()['username']}")
                    self.empty_label.setText("Change Information is Successfully!")
            else:
                self.empty_label.setText("Error: The password not equal by confirm password")
        else:
            self.empty_label.setText("Error: Please enter your information complete")

    def change_bio(self):
        self.main_user.bio_graph = self.qline5.text()
        self.qline5.clear()


class ContactPanel(QMainWindow):
    def __init__(self, main_user, before_panel):
        super().__init__()
        self.main_user = main_user
        self.before_panel = before_panel
        self.setWindowTitle("Add Contact")
        self.resize(380, 220)
        self.picture_brown = QPixmap(r"C:\Final_Project\Back5.jpg")
        self.background = QLabel(self)
        self.background.resize(380, 220)
        self.background.setPixmap(self.picture_brown)
        self.background.setScaledContents(True)
        self.main_lay = QVBoxLayout()
        self.wg1 = QWidget(self)
        self.wg1.resize(380, 220)
        self.wg1.ly1 = QVBoxLayout()
        self.wg1.label1 = QLabel("Username :", self)
        self.wg1.label1.setStyleSheet("color: white; font-size: 13px")
        self.wg1.qline1 = QLineEdit()
        self.wg1.label2 = QLabel("Phone Number :", self)
        self.wg1.label2.setStyleSheet("color: white; font-size: 13px")
        self.wg1.qline2 = QLineEdit()
        self.wg1.button1 = QPushButton("Add")
        self.wg1.button1.clicked.connect(self.add_contact)
        self.wg1.empty_label = QLabel("", self)
        self.wg1.empty_label.setStyleSheet("color: red; font-size: 13px")
        #
        self.wg1.ly1.addWidget(self.wg1.label1)
        self.wg1.ly1.addWidget(self.wg1.qline1)
        self.wg1.ly1.addWidget(self.wg1.label2)
        self.wg1.ly1.addWidget(self.wg1.qline2)
        self.wg1.ly1.addWidget(self.wg1.button1)
        self.wg1.ly1.addWidget(self.wg1.empty_label)
        #
        self.wg1.setLayout(self.wg1.ly1)
        #
        self.main_lay.addWidget(self.wg1)
        self.setLayout(self.main_lay)
        self.wg1.button1.setStyleSheet("background-color: lightgreen")

    def add_contact(self):
        username = self.wg1.qline1.text()
        phon_number = self.wg1.qline2.text()
        contact = None
        if username and phon_number:
            for user in users:
                if user.get_info()["username"] == username and user.get_info()["phon number"] == phon_number:
                    contact = user
            if contact and contact != self.main_user:
                self.main_user.contacts.append(contact)
                self.main_user.message[contact.get_info()['username']] = []
                self.wg1.empty_label.setText("<<Add contact successfully!>>")
                self.wg1.empty_label.setStyleSheet("color: blue; font-size: 13px")
                # Added picture of contact to  main Widget:
                if contact.picture_pro:
                    picture = QPixmap(contact.picture_pro)
                    self.before_panel.wg2.button = QPushButton()
                    self.before_panel.wg2.button.setIcon(QIcon(picture))
                else:
                    color = contact.color_profile
                    self.before_panel.wg2.button = QPushButton(contact.get_info()["username"])
                    self.before_panel.wg2.button.setStyleSheet(f"background: {color};")
                self.before_panel.wg2.button.setFixedSize(60, 60)
                self.before_panel.wg2.button.setIconSize(QSize(60, 60))
                self.before_panel.wg2.ly.addWidget(self.before_panel.wg2.button, len(self.main_user.contacts) + 1, 0)
                self.before_panel.wg2.username = QLabel(f"{contact.get_info()['username']}")
                self.before_panel.wg2.username.setStyleSheet("color: white; font-size: 14px;")
                self.before_panel.wg2.ly.addWidget(self.before_panel.wg2.username, len(self.main_user.contacts) + 1, 1)
                # open the chat for selected contact:
                self.before_panel.wg2.button.clicked.connect(lambda checked=False, c = contact: self.before_panel.open_chat(c))
            else:
                self.wg1.empty_label.setText("Error: <<Not exist a contact such this information>>")
                self.wg1.empty_label.setStyleSheet("color: red; font-size: 13px")
        else:
            self.wg1.empty_label.setText("Error: <<Enter the info complete>>")
            self.wg1.empty_label.setStyleSheet("color: red; font-size: 13px")


# open the app and entry window:
app = QApplication(sys.argv)
window0 = EntryWindow()
window0.show()
app.exec()

# clear all data from table
while 1:
    try:
        f = session.query(UserSqlite).first()
        session.delete(f)
        session.commit()
    except:
        break


# Add data of user to table:
for user in users:
    usersql1 = UserSqlite(username = user.get_info()['username'], password = user.get_info()['password'], phone_number = user.get_info()['phon number'], picture_pro = user.picture_pro)
    usersql1.color_profile = user.color_profile
    usersql1.bio_graph = user.bio_graph
    contact_usernames = []
    for contact in user.contacts:
        contact_usernames.append(contact.get_info()['username'])
    contact_usernames_str = json.dumps(contact_usernames)
    message = json.dumps(user.message)
    usersql1.contacts = contact_usernames_str
    usersql1.message = message
    session.add(usersql1)
    session.commit()


# Show data of users:
users_sql = session.query(UserSqlite).all()
print("All users:")
for user_sqlite in users_sql:
    print(f"Username: {user_sqlite.username}, Password: {user_sqlite.password}, Phone number: {user_sqlite.phone_number}")


