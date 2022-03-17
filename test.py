import kivy;
from kivy.app import App;
from kivy.uix.label import Label;
# from kivy.uix.gridlayout import GridLayout;
# from kivy.uix.textinput import TextInput;
# from kivy.uix.button import Button;
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('whatever.kv');

class MyLayout(Widget):
    # #initialize infinite keyords
    # def __init__(self, **kwargs):
    #     #call grid layout constructor
    #     super(MyGridLayout, self).__init__(**kwargs);
    #
    #     #set columns
    #     self.cols = 1;
    #
    #     #create new grid GridLayout
    #     self.top_grid = GridLayout(
    #         row_force_default = True,
    #         row_default_height = 100
    #         );
    #     self.top_grid.cols = 2;
    #
    #     #add widgets
    #     self.top_grid.add_widget(Label(text = "Name: "));
    #     #add input box
    #     self.name = TextInput(multiline = False);
    #     self.top_grid.add_widget(self.name);
    #     #add widgets
    #     self.top_grid.add_widget(Label(text = "Favorite Cat Breed: "));
    #     #add input box
    #     self.cat_breed = TextInput(multiline = False);
    #     self.top_grid.add_widget(self.cat_breed);
    #
    #     #add new top_grid
    #     self.add_widget(self.top_grid);
    #
    #     #create submit
    #     self.submit = Button(text = "Submit",
    #         font_size = 30,
    #         size_hint_y = None,
    #         height = 50
    #         );
    #     #bind Button
    #     self.submit.bind(on_press = self.press);
    #     self.add_widget(self.submit);

    # name = ObjectProperty(None);
    # cat_breed = ObjectProperty(None);
    #
    # #button press stuff
    # def press(self):
    #     name = self.name.text;
    #     cat_breed = self.cat_breed.text;
    #
    #     #print(f'Hello {name}, your favorite cat breed is {cat_breed}');
    #     #print to screen
    #     self.add_widget(Label(text = f'Hello {name}, your favorite cat breed is {cat_breed}'));
    #     #clear input boxes
    #     self.name.text = "";
    #     self.cat_breed.text = "";

    def press(self):
        #variables for our widgets
        self.ids.image_label.text = "Shinobu is Not Impressed";
        self.ids.image_on_screen.source = 'shinobu_unimpressed.png';

    def release(self):
        #variables for our widgets
        self.ids.image_label.text = "Crying Until I'm Laughing Cow Emoji";
        self.ids.image_on_screen.source = 'crying_until_im_laughing_cow_emoji.png';

class MeetInMiddleApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1);
        return MyLayout();

if __name__ == '__main__':
    MeetInMiddleApp().run();
