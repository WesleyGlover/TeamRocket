import kivy.utils as utils;
#from kivy.app import App;
from kivy.lang import Builder;
from kivy.uix.screenmanager import ScreenManager, Screen;
from kivy.properties import ObjectProperty;
from kivy.core.window import Window;
from kivy.animation import Animation;
from kivy.uix.popup import Popup

from kivymd.app import MDApp;
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior;
from kivymd.uix.card import MDCard;

class Card(MDCard, RoundedRectangularElevationBehavior):
    pass;
#location services
import datetime
from geopy.geocoders import Nominatim
import geocoder

#Server connectivity
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol

#clear files from cache
import os

#constants
#colors for app elements
#text font colors
soft_black = '#333333' #for sky_blue, aqua_blue, mint_green, peach_pink, egg_back
harsh_black = '#0F0F0F' #for apple_red
not_white = '#EBEBEB' #for forest_green, night_blue, apple_red, thick_ice, black_back
off_white = '#FCFCFC' #for dark_peach

#colors for visual elements for app
apple_red = '#F5345C' #can be used in both themes

mint_green = '#B2EB9C' #not for light mode
peach_pink = '#E0AF9D' #not for light mode
aqua_blue = '#4ED2DB' #not for light mode
sky_blue = '#51A6F5' #not for light mode

dark_peach = '#D1797B' #not for dark mode (but can be used)
night_blue = '#366EA3' #not for dark mode
forest_green = '#1D7850' #not for dark mode
thick_ice = '#0C6399' #not for dark mode

#app beckground colors
black_back = '#0D0D0D' #for dark mode background
egg_back = '#F2F2F2' #for light mode background

#settings_file = open('brownie.set', 'rw');
#option = settings_file.readline();


#Classes for connecting to server complimentary of wesley
class EchoClient(protocol.Protocol):
    #we don't know if thing thing or not. Wesley look at this 
    #self connection = connection
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    #Return response from server
    def dataReceived(self, data):
        self.factory.app.print_message(data.decode('utf-8'))


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        pass
        #self.app.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        pass
        #self.app.print_message('Lost connection.')

    def clientConnectionFailed(self, connector, reason):
        pass
        #self.app.print_message('Connection failed.')
##End server classes

#define our screens (we have quite a few)
class TitleScreen(Screen):
    pass;
class LoginScreen(Screen):
    pass;
class RegisterScreen(Screen):
    pass;
class HomeScreen(Screen):
    def get_user_lat(self):
        app = Nominatim(user_agent="MITM")

        #Get location based on user
        location = geocoder.ip('me')

        lat = location.geojson['features'][0]['properties']['lat']
        return lat

    def get_user_lon(self):
        app = Nominatim(user_agent="MITM")

        location = geocoder.ip('me')

        lon = location.geojson['features'][0]['properties']['lng']

        return lon

class MeetingInfoScreen(Screen):
    pass;
class CreateMeetingScreen(Screen):
    pass;
class SettingsScreen(Screen):
    pass;
class CalenderScreen(Screen):
    pass;
class ConfirmRequestScreen(Screen):
    pass;
class ExploreScreen(Screen):
    pass;


#creating the screen manager
class Manager(ScreenManager):
    pass;

#set the app size
Window.size = (900/2, 1600/2);

#grab the design document

    

class Meet_in_the_MiddleApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs);

        # self.theme_cls.theme_style = "Light"
        Window.clearcolor = utils.get_color_from_hex(egg_back);
        # Window.borderless = True;

        #Clear all files in the cache
        dir = './cache'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    def build(self):
        self.connect_to_server() #For server
        kv = Builder.load_file('applayout.kv');
        return kv;

    #Server connectivity funtionality
    def connect_to_server(self):
        #Values will need to change when connecting to actual server
        reactor.connectTCP('localhost', 8000, EchoClientFactory(self))

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(msg.encode('utf-8'))
            self.textbox.text = ""

if __name__ == '__main__':
    Meet_in_the_MiddleApp().run();

#settings_file.write();
#settings_file.close();
