import kivy;
from kivy.app import App;
from kivy.uix.widget import Widget;
from kivy.properties import ObjectProperty;
from kivy.lang import Builder;
from kivy.uix.screenmanager import ScreenManager, Screen;
from kivy.core.window import Window;

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
Window.size = (600, 900);

#grab the design document
kv = Builder.load_file('applayout.kv');

def on_touch_down(self, touch):
    pass;

class Meet_in_the_MiddleApp(App):
    def build(self):
        return kv;

if __name__ == '__main__':
    Meet_in_the_MiddleApp().run();
