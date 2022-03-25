import kivy.utils as utils;
from kivymd.app import MDApp;
from kivy.lang import Builder;
from kivy.uix.screenmanager import ScreenManager, Screen;
from kivy.properties import ObjectProperty;
from kivy.core.window import Window;
from kivy.animation import Animation;
from kivy.uix.popup import Popup

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

#define our screens (we have quite a few)
class TitleScreen(Screen):
    pass;
class LoginScreen(Screen):
    pass;
class RegisterScreen(Screen):
    pass;
class HomeScreen(Screen):
    pass;
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
kv = Builder.load_file('applayout.kv');

class Meet_in_the_MiddleApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs);

        # self.theme_cls.theme_style = "Light"
        Window.clearcolor = utils.get_color_from_hex(egg_back);

    def build(self):
        return kv;

if __name__ == '__main__':
    Meet_in_the_MiddleApp().run();

#settings_file.write();
#settings_file.close();
