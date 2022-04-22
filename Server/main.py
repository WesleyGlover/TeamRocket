# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
import os
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


# Class to handle the data sent from connection. Each instance is connection
class MITMServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


# Factory class to initialize new connections as MITMServer classes
class MITMServerFactory(protocol.Factory):
    protocol = MITMServer

    def __init__(self, app):
        self.app = app


# App that runs it all
class MITMServerApp(App):
    label = None
    textbox = None

    # Initializing the server
    def build(self):
        root = self.setup_gui()
        self.listen_for_client()
        return root

    # Setting up the gui
    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    # Waiting for client connection
    def listen_for_client(self):
        reactor.listenTCP(25565, MITMServerFactory(self))

    # Taking input from console line and processing it locally on server
    def send_message(self, *args):
        msg = self.textbox.text
        if msg:
            self.print_message(f"{msg}")
            self.textbox.text = ""
            return (msg.encode('utf-8'))

    # Handling the messages sent by the client
    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.print_message("\nreceived:  {}\n".format(msg))
        msg = json.loads(msg)
        response = "failure"

        # Checking for keywords from input
        if msg['command'] == "login":
            self.print_message("Starting Login Process")
            response = self.auth_login(msg)
            self.print_message(f"Response: {response['Account Status']}")

        # Checking for registration
        if msg['command'] == "register":
            self.print_message("Starting Registration Process")
            response = self.auth_regi(msg)

        # Checking for Creation of new meeting
        if msg['command'] == 'create_meeting':
            self.print_message("Starting New Meeting")

        self.label.text += "responded: {}\n".format(response)
        return (json.dumps(response).encode('utf-8'))

    # Print message to console on server
    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)

    # Defining the authentication function
    def auth_login(self, msg):
        # Setting up json message to send back
        response = {'command': 'login'}

        # Connect to database Here to check for account
        if os.path.isfile("accounts.txt"):
            with open("accounts.txt", "r") as f:
                r = f.read().split(",")
                if msg["username"] in r:
                    # Username found, checking for password
                    self.print_message(f"Found Username {msg['username']} in the database")
                    response['Account Status'] = "True"
                elif msg["email"] in r:
                    # Email found, Checking for password
                    self.print_message(f"Found Email {msg['email']} in the database")
                    response['Account Status'] = "True"
                else:
                    self.print_message(f"No account was found associated with Username/Email provided")
                    response['Account Status'] = "False"
        return response

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

    # Defining the new meeting creation function
    def new_meeting(self, msg):
        # Make new table entry in database
        # add user information from given login
        # Find other user and send invite by adding it to table in database
            # This may require on login/ random refresh for users to check for any invites.
        self.print_message("Inside new_meeting Function")



if __name__ == '__main__':
    MITMServerApp().run()
