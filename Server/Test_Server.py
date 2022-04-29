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


class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    #label = None

    def build(self):
        root = self.setup_gui()
        reactor.listenTCP(8000, EchoServerFactory(self))
        return root

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    # Print message to console on server
    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)

     # Taking input from console line and processing it locally on server
    def send_message(self, *args):
        msg = self.textbox.text
        if msg:
            self.print_message(f"{msg}")
            self.textbox.text = ""
            return (msg.encode('utf-8'))

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.label.text = "received:  {}\n".format(msg)

        response = self.send_message()

        self.label.text += "responded: {}\n".format(response)
        return response


if __name__ == '__main__':
    TwistedServerApp().run()
