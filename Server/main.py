# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
import os
import json

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


class MITMServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class MITMServerFactory(protocol.Factory):
    protocol = MITMServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class MITMServerApp(App):
    label = None
    textbox = None

    # Initializing the server
    def build(self):
        self.label = Label(text="server started\n")
        #reactor.listenTCP(25565, MITMServerFactory(self))
        reactor.listenTCP(8000, MITMServerFactory(self))
        return self.label

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    # Handling the messages sent by the client
    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.label.text = "received:  {}\n".format(msg)
        msg = json.loads(msg)
        response = "failure"

        # Checking for keywords from input
        if msg['command'] == "login":
            self.print_message("Starting Login Process")
            response = self.auth_login(msg)

        # Checking for registration
        if msg['command'] == "register":
            self.print_message("Starting Registration Process")
            response = self.auth_regi(msg)

        self.label.text += "responded: {}\n".format(response)
        return response.encode('utf-8')

    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)

    # Defining the authentication function
    def auth_login(self, msg):
        
        # Check the parsed phrases for exact matches in the file system.
        if os.path.isfile("accounts.txt"):
            with open("accounts.txt", "r") as f:
                r = f.read().split(",")
                if msg["username"] in r:
                    # Username found, checking for password
                    self.print_message(f"Found Username {msg['username']} in the database")
                else:
                    self.print_message(f"Username {msg['username']} is not in the database")

        # if d[1] not in users['Email'].unique():
        #   popFunc() --> Add this funtion to the client app side to review popups
        msg = "Return: True\n"
        return msg

    # Defining the registration function
    def auth_regi(self, msg):

        # Checking for pre-existing account by Email
        if os.path.isfile("accounts.txt"):
            with open("accounts.txt", "r") as f:
                r = f.read().split(",")
                if msg["email"] in r:
                    response = "An account is already associated with the provided email"
                    self.print_message(response)
                    return response
                    
        # Writing the new account to the database
        with open("accounts.txt", "w") as f:
            f.write(f"{msg['email']},{msg['username']},{msg['name']}")

        msg = "Registered!"
        return msg



if __name__ == '__main__':
    MITMServerApp().run()
