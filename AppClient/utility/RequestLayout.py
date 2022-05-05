#going to be a similar mechanism as the MeetingLayout class
#this will be used to populate the requests popup with meeting requests dynamically
from kivy.lang import Builder;
from kivy.uix.scrollview import ScrollView;
from kivy.uix.label import Label;
from kivy.uix.button import Button;
from kivy.uix.boxlayout import BoxLayout;
from kivy.properties import NumericProperty, ReferenceListProperty;
from kivy.uix.popup import Popup;
from kivy.uix.textinput import TextInput;

from kivymd.uix.card import MDCard;

from kivy.garden.mapview import MapView;

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

#These are defaults for the MeetingLayout classes
<RequestLayout>:
    do_scroll_x: False #needs to be false to scoll only in 'y' direction
    do_scroll_y: True
<RequestBandContainer>
    oriention: "vertical"
    size_hint_y: None #needs to be none to scrollview properly
<RequestBand>:
    size_hint_y: None #needs to be none to scrollview properly
    height: 40 #we have to manually set the height of the bands
    md_bg_color: utils.get_color_from_hex(peach_pink)
    ripple_behavior: True #cool ripple effect so that the user knows which band they touched
    on_touch_down: self.on_touch_down(args[1]) #we call that sweet meeting popup
<RequestInstigator>:
    id: request_instigator
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)
<RequestDate>:
    id: request_date
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)

<ConfirmRequestPopup>
    size_hint: (.8, .8)
    pos_hint: {'center_x': .5, 'center_y': .5}
""")

class ConfirmRequestPopup(Popup):
    def __init__(self, meeting_info, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.meeting_info = meeting_info;
        self.title = "Request Information";

        #query for the meeting info from the server
        #populate that here to widgets
        self.meeting_info_container = BoxLayout();

        # #meeting map
        # self.meeting_info_container.meeting_loc_map = MapView();
        # self.meeting_info_container.meeting_loc_map.lat = 30.273300;
        # self.meeting_info_container.meeting_loc_map.lon = -98.789063;
        # self.meeting_info_container.meeting_loc_map.zoom = 17;
        # self.meeting_info_container.add_widget(self.meeting_info_container.meeting_loc_map);

        #meeting instigator
        self.meeting_info_container.meeting_instigator = Label();
        self.meeting_info_container.meeting_instigator.text = f"Meeting Instigater: {meeting_info['meeting_instigator']}";
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_instigator);

        #meeting datetime
        self.meeting_info_container.meeting_date = Label();
        self.meeting_info_container.meeting_date.text = "Meeting Date: temp date";
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_date);
        self.meeting_info_container.meeting_time = Label();
        self.meeting_info_container.meeting_time.text = f"Meeting Time: {meeting_info['meeting_time']}";
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_time);

        self.meeting_info_container.accept_button = Button(text = "Accept");
        self.meeting_info_container.add_widget(self.meeting_info_container.accept_button);
        self.meeting_info_container.reject_button = Button(text = "Reject");
        self.meeting_info_container.add_widget(self.meeting_info_container.reject_button);

        #meeting instigator
        self.meeting_info_container.second_addr_label = Label();
        self.meeting_info_container.second_addr_label.text = "Starting Address:";
        self.meeting_info_container.add_widget(self.meeting_info_container.second_addr_label);

        self.meeting_info_container.second_addr = TextInput();
        self.meeting_info_container.add_widget(self.meeting_info_container.second_addr);

        #then assign the container to self.content
        self.content = self.meeting_info_container;

class RequestLayout(ScrollView):
    def __init__(self, *args, **kwargs):
        super(RequestLayout, self).__init__(*args, **kwargs);

        self.init_ui([]);

    def init_ui(self, data):
        self.main_view = RequestBandContainer();
        self.main_view.bind(minimum_height=self.main_view.setter('height'));
        self.add_widget(self.main_view);

        self.main_view.band_list = [];

        count = 0;
        for d in data:
            self.create_request_band(d, count);
            count += 1;

    def create_request_band(self, data_instance, position):

        self.main_view.band_list.append(RequestBand(orientation = "horizontal"));
        self.main_view.band_list[position].meeting_info = data_instance;
        self.main_view.band_list[position].add_widget(RequestInstigator(text = data_instance['meeting_instigator']));
        self.main_view.band_list[position].add_widget(RequestDate(text = "date"));

        self.main_view.add_widget(self.main_view.band_list[position]);

    def update_requests(self, meetings_list):
        self.main_view.band_list.clear()
        self.main_view.clear_widgets()

        for meeting in meetings_list:
            if meeting['meeting_status'] == "PENDING":
                self.create_meeting_band(meeting, len(self. ain_view.band_list))


class RequestBandContainer(BoxLayout):
    pass;

class RequestBand(MDCard):
    meeting_info = {}

    def on_touch_down(self, touch):
        meeting_popup = ConfirmRequestPopup(self.meeting_info);
        meeting_popup.open();

class RequestInstigator(Label):
    pass;
class RequestDate(Label):
    pass;
