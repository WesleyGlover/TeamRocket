from __future__ import unicode_literals
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import os
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    # def dataReceived(self, data):
    #     self.factory.app.print_message(data.decode('utf-8'))


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    # def startedConnecting(self, connector):
    #     self.app.print_message('Started to connect.')
    #
    # def clientConnectionLost(self, connector, reason):
    #     self.app.print_message('Lost connection.')
    #
    # def clientConnectionFailed(self, connector, reason):
    #     self.app.print_message('Connection failed.')


class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        # Checking for pre-existing values
        if os.path.isfile("prev_detials.txt"):
            with open("prev_detials.txt", "r") as f:
                d = f.read().split(",")
                prev_username = d[0]
                prev_password = d[1]
        else:
            prev_username = ""
            prev_password = ""

        # Creating the IP widget and text input box
        self.add_widget(Label(text="Username:"))
        self.Username = TextInput(text=prev_username, multiline=False)
        self.add_widget(self.Username)

        # Creating the Port Widget and text input box
        self.add_widget(Label(text="Password:"))
        self.Password = TextInput(text=prev_password, multiline=False)
        self.add_widget(self.Password)

        # Creating the join button widget
        self.join = Button(text="Join")
        self.join.bind(on_press=self.join_button)
        # Emtpy label to move the button to the right
        self.add_widget(Label())
        self.add_widget(self.join)

    def join_button(self, instance):
        username = self.Username.text
        password = self.Password.text

        print(f"Attempting to join as {username} with {password}")
        self.send_message()

        with open("prev_detials.txt", "w") as f:
            f.write(f"{username},{password}")

    def send_message(self, *args):
        username = self.Username.text
        password = self.Password.text
        msg = f"auth_log,{username},{password}"
        if EpicApp.connection:
            EpicApp.connection.write(msg.encode('utf-8'))


class EpicApp(App):
    connection = None

    # Initializing the app
    def build(self):
        self.connect_to_server()
        return ConnectPage()

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        #self.print_message("Connected successfully!")
        self.connection = connection


if __name__ == "__main__":
    EpicApp().run()
