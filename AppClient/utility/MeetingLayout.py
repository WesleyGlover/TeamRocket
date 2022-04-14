from kivy.lang import Builder;
from kivy.uix.scrollview import ScrollView;
from kivy.uix.label import Label;
from kivy.uix.boxlayout import BoxLayout;
from kivy.properties import NumericProperty, ReferenceListProperty;

from kivymd.uix.card import MDCard;

Builder.load_string("""
#:import utils kivy.utils

#colors for app elements
#text font colors
#:set soft_black '#333333' #for sky_blue, aqua_blue, mint_green, peach_pink, egg_back
#:set harsh_black: '#0F0F0F' #for apple_red
#:set not_white '#EBEBEB' #for forest_green, night_blue, apple_red, thick_ice, black_back
#:set off_white '#FCFCFC' #for dark_peach

#colors for visual elements for app
#:set apple_red '#F5345C' #can be used in both themes

#:set mint_green '#B2EB9C' #not for light mode
#:set peach_pink '#E0AF9D' #not for light mode
#:set aqua_blue '#4ED2DB' #not for light mode
#:set sky_blue '#51A6F5' #not for light mode

#:set dark_peach '#D1797B' #not for dark mode (but can be used)
#:set night_blue '#366EA3' #not for dark mode
#:set forest_green '#1D7850' #not for dark mode
#:set thick_ice '#0C6399' #not for dark mode

#app beckground colors
#:set black_back '#0D0D0D' #for dark mode background
#:set egg_back '#F2F2F2' #for light mode background

<MeetingBand>:
    orientation: "horizontal"
    md_bg_color: utils.get_color_from_hex(peach_pink)
<MeetingName>:
    id: meeting_name
    color: utils.get_color_from_hex(soft_black)
<MeetingInstigator>:
    id: meeting_instigator
    color: utils.get_color_from_hex(soft_black)
<MeetingDate>:
    id: meeting_date
    color: utils.get_color_from_hex(soft_black)
""")

class Data:
    name = "";
    inst = "";
    date = "";

class MeetingBand(MDCard):
    pass;

class MeetingName(Label):
    pass;
class MeetingInstigator(Label):
    pass;
class MeetingDate(Label):
    pass;

class MeetingLayout(ScrollView):
    def __init__(self, *args, **kwargs):
        super(MeetingLayout, self).__init__(*args, **kwargs);

        ins_data = Data();
        ins_data.name = "Book Club";
        ins_data.inst = "Kalvin";
        ins_data.date = "May 20, 2020";

        proc_data_set = [ins_data, ins_data] #self.prepare_data();
        self.init_ui(proc_data_set);

    def init_ui(self, data):
        self.main_view = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_view);

        for d in data:
            self.main_view.new_insert = MeetingBand();
            self.main_view.new_insert.add_widget(MeetingName(text = d.name));
            self.main_view.new_insert.add_widget(MeetingInstigator(text = d.inst));
            self.main_view.new_insert.add_widget(MeetingDate(text = d.date));

            self.main_view.add_widget(self.main_view.new_insert);

    def create_meeting_band(self):
        pass;
    def prepare_data(self, data_set):
        pass;
    def on_touch_move(self, touch):
        pass;
