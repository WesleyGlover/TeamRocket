from kivy.lang import Builder;
from kivy.uix.scrollview import ScrollView;
from kivy.uix.label import Label;
from kivy.uix.boxlayout import BoxLayout;
from kivy.properties import NumericProperty, ReferenceListProperty;
from kivy.uix.popup import Popup;
from kivy.garden.mapview import MapView;
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

#These are defaults for the MeetingLayout classes
<MeetingLayout>:
    do_scroll_x: False #needs to be false to scoll only in 'y' direction
    do_scroll_y: True
    app: app
<MeetingBandContainer>
    oriention: "vertical"
    size_hint_y: None #needs to be none to scrollview properly
<MeetingBand>:
    size_hint_y: None #needs to be none to scrollview properly
    height: 40 #we have to manually set the height of the bands
    md_bg_color: utils.get_color_from_hex(peach_pink)
    ripple_behavior: True #cool ripple effect so that the user knows which band they touched
    on_touch_down: self.on_touch_down(args[1]) #we call that sweet meeting popup
<MeetingName>:
    id: meeting_name
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)
<MeetingPartner>:
    id: meeting_partner
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)
<MeetingDate>:
    id: meeting_date
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)
<MeetingLocation>:
    id: meeting_location
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(off_white)
    multiline: True
<MeetingInfoPopup>
    size_hint: (.8, .8)
    pos_hint: {'center_x': .5, 'center_y': .5}
""")

#The MeetingInfoPopup will display on band touch
class MeetingInfoPopup(Popup):
    def __init__(self, meeting_id, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.meeting_id = meeting_id;
        self.title = "Request Information";

        self.meeting_info_container = BoxLayout();
        #query for the meeting info from the server
        #populate that here to widgets
        #meeting map
        self.meeting_info_container.meeting_loc_map = MapView();
        self.meeting_info_container.meeting_loc_map.lat = meeting_id['mp_lat'];
        self.meeting_info_container.meeting_loc_map.lon = meeting_id['mp_lon'];
        self.meeting_info_container.meeting_loc_map.zoom = 17;
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_loc_map);

        #meeting instigator
        self.meeting_info_container.meeting_participants = Label();
        self.meeting_info_container.meeting_participants.text = f"Meeting Participants: {meeting_id['meeting_instigator']}";
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_participants);

        #meeting datetime
        self.meeting_info_container.meeting_date = Label();
        self.meeting_info_container.meeting_date.text = "Meeting Date: temp date";
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_date);
        self.meeting_info_container.meeting_time = Label(size_hint_y = None, text_size= (self.width, None), height = self.texture_size[1]);
        self.meeting_info_container.meeting_time.text = f"Meeting Time: {meeting_id['meeting_time']}";
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_time);

        #meeting instigator
        self.meeting_info_container.meeting_location = Label();
        self.meeting_info_container.meeting_location.text = f"Meeting Address: {meeting_id['location_ID']}";
        self.meeting_info_container.add_widget(self.meeting_info_container.meeting_location);

        self.content = self.meeting_info_container;

class MeetingLayout(ScrollView):
    def __init__(self, *args, **kwargs):
        super(MeetingLayout, self).__init__(*args, **kwargs);
        self.init_ui({})

    def init_ui(self, data):
        self.main_view = MeetingBandContainer(); #create the boxlayout that goes in the scrollview
        self.main_view.bind(minimum_height=self.main_view.setter('height'))
        self.add_widget(self.main_view);

        self.main_view.band_list = []; #i made the bands into a list so we can access them later if need be

        count = 0;
        for d in data:
            self.create_meeting_band(d, count);
            count += 1;

    def create_meeting_band(self, data_instance, position):
        user_to_show = data_instance['meeting_partner'] if self.app.user_info['username'] == data_instance['meeting_instigator'] else data_instance['meeting_instigator']

        self.main_view.band_list.append(MeetingBand(orientation = "horizontal"));
        self.main_view.band_list[position].meeting_id = data_instance;
        self.main_view.band_list[position].add_widget(MeetingPartner(text = user_to_show));
        self.main_view.band_list[position].add_widget(MeetingDate(text = data_instance['meeting_date']));
        #self.main_view.band_list[position].add_widget(MeetingLocation(text = data_instance['location_ID']));

        self.main_view.add_widget(self.main_view.band_list[position]);

    def update_meetings(self, meetings_list):
        self.main_view.band_list.clear()
        self.main_view.clear_widgets()

        for meeting in meetings_list:
            if meeting['meeting_status'] == "ACCEPTED":
                self.create_meeting_band(meeting, len(self. main_view.band_list))



class MeetingBandContainer(BoxLayout):
    pass;

class MeetingBand(MDCard):
    meeting_id = None; #keep track of the meeting_id so that we can kill it later, maybe

    def on_touch_down(self, touch):
        meeting_popup = MeetingInfoPopup(self.meeting_id); #might pass that to the MeetingInfoPopup so that we can display all the info
        meeting_popup.open();

class MeetingName(Label):
    pass;
class MeetingPartner(Label):
    pass;
class MeetingDate(Label):
    pass;
class MeetingLocation(Label):
    pass;
