# Import the required modules
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import socket
import json
import threading
import random

# Define the main window class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.setWindowTitle("UDP Chatroom")
        self.setGeometry(300, 300, 600, 400)
        self.client = client
        self.join = False
        self.register = False
        self.run = True

        # Set the timeout to 5 seconds
        self.client.settimeout(5)

        # Create a thread for receiving messages from the server
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        # Create the main widget and set it as the central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout for the main widget
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Create a text area for displaying messages
        self.text_area = QtWidgets.QTextEdit(self.central_widget)
        self.text_area.setReadOnly(True)
        self.main_layout.addWidget(self.text_area)

        # Create a layout for the input controls
        self.input_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Create a line edit for inputting commands
        self.command_input = QtWidgets.QLineEdit(self.central_widget)
        self.command_input.returnPressed.connect(self.send)
        self.input_layout.addWidget(self.command_input)

        # Create a button for sending the input
        self.send_button = QtWidgets.QPushButton("Send", self.central_widget)
        self.send_button.clicked.connect(self.send)
        self.input_layout.addWidget(self.send_button)

        # Add the input
