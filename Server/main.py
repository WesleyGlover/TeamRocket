# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
import os
import mysql.connector

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

        # Checking for keywords from input
        if "auth_log" in msg.lower():
            self.print_message("Starting Login Process")
            msg = self.auth_login(msg)

        # Checking for registration
        if "register" in msg.lower():
            self.print_message("Starting Registration Process")
            msg = self.auth_regi(msg)

        self.label.text += "responded: {}\n".format(msg)
        return msg.encode('utf-8')

    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)

    # Defining the authentication function
    def auth_login(self, msg):
        self.print_message(f"Starting to parse: {msg}")
        d = msg.split(",")
        self.print_message(f"\nUsername: {d[1]}\nPassword: {d[2]}\n\n")

        # Check the parsed phrases for exact matches in the file system.
        if os.path.isfile("accounts.txt"):
            with open("accounts.txt", "r") as f:
                r = f.read().split(",")
                if d[1] in r:
                    # Username found, checking for password
                    self.print_message(f"Found Username {d[1]} in the database")
                else:
                    self.print_message(f"Username {d[1]} is not in the database")

        # if d[1] not in users['Email'].unique():
        #   popFunc() --> Add this funtion to the client app side to review popups
        msg = "Return: True\n"
        return msg

    # Defining the registration function
    def auth_regi(self, msg):
        self.print_message(f"Starting to parse: {msg}")
        d = msg.split(",")
        self.print_message(f"\nName: {d[1]}\nEmail: {d[2]}\nUsername: {d[3]}\nPassword: {d[4]}\n\n")

        # Checking for pre-existing account by Email
        if os.path.isfile("accounts.txt"):
            with open("accounts.txt", "r") as f:
                r = f.read().split(",")
                if d[2] in r:
                    msg = "An account is already associated with the provided email"
                    self.print_message(msg)
                    return msg
                    
        # Writing the new account to the database
        with open("accounts.txt", "w") as f:
            f.write(f"{d[1]},{d[2]},{d[3]}")

        msg = "Registered!"
        return msg

    # DB Auth

    def database_auth():
        try:
            connection = mysql.connector.connect(
                user='doadmin',
                password ='AVNS_WZEScW_Y5FNKr7m',
                host='db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com',
                port = 25060,
                database='defaultdb'
            )
            print('\n[+] Connected to db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com Successfully')

            cursor = connection.cursor()
            cursor.execute("Select * From User")
            result = cursor.fetchall()
            print("Output from query : Select * From User:")
            print(type(result))
            print(result, '\n')
            
        except BaseException as e:
            print(str(e))
    database_auth()

if __name__ == '__main__':
    MITMServerApp().run()
