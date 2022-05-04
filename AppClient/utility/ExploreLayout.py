#going to be a similar mechanism as the MeetingLayout class
#this will be used to populate the explore page with locations dynamically
from kivy.lang import Builder;
from kivy.uix.scrollview import ScrollView;
from kivy.uix.label import Label;
from kivy.uix.boxlayout import BoxLayout;
from kivy.properties import NumericProperty, ReferenceListProperty;
from kivy.uix.popup import Popup;
from kivy.uix.textinput import TextInput;

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

#These are defaults for the ExploreLayout classes
<ExploreLayout>:
    do_scroll_x: False #needs to be false to scoll only in 'y' direction
    do_scroll_y: True
<ExploreBandContainer>
    oriention: "vertical"
    size_hint_y: None #needs to be none to scrollview properly
<ExploreBand>:
    size_hint_y: None #needs to be none to scrollview properly
    height: 40 #we have to manually set the height of the bands
    md_bg_color: utils.get_color_from_hex(peach_pink)
    ripple_behavior: True #cool ripple effect so that the user knows which band they touched
    on_touch_down: self.on_touch_down(args[1]) #we call that sweet meeting popup
<LocationName>:
    id: location_name
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)
<LocationRating>:
    id: location_rating
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)
<LocationType>:
    id: location_type
    pos_hint: {"center_y": .5}
    color: utils.get_color_from_hex(soft_black)

<LocationInfoPopup>
    size_hint: (.8, .8)
    pos_hint: {'center_x': .5, 'center_y': .5}
""")

#The MeetingInfoPopup will display on band touch
class LocationInfoPopup(Popup):
    def __init__(self, location_id, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.location_id = location_id;
        self.title = "Location Information";

        #query for the location info from the server
        #populate that here to widgets

        #add each widget to a container widget
        #then assign the container to self.content

class ExploreLayout(ScrollView):
    #the data for this layout should be based on the location entered in the search bar
    def __init__(self, *args, **kwargs):
        super(ExploreLayout, self).__init__(*args, **kwargs);

        ins_data = ExploreLayoutData();
        ins_data.location_id = 12345;
        ins_data.location_name = "West Coast Library";
        ins_data.location_rating = "3/5";
        ins_data.location_type = "Library";

        proc_data_set = [ins_data] #self.prepare_data();
        self.init_ui(proc_data_set);

    def init_ui(self, data):
        self.main_view = BoxLayout();
        self.add_widget(self.main_view);

        self.main_view.search_bar_label = Label(text = "Seach");
        self.main_view.add_widget(self.main_view.search_bar_label);
        self.main_view.explore_search_bar = TextInput();
        self.main_view.add_widget(self.main_view.explore_search_bar);

        self.main_view.explore_band_container = ExploreBandContainer(); #create the boxlayout that goes in the scrollview
        self.main_view.explore_band_container.bind(minimum_height=self.main_view.setter('height'))
        self.main_view.add_widget(self.main_view.explore_band_container);

        self.main_view.explore_band_container.band_list = []; #i made the bands into a list so we can access them later if need be

        count = 0;
        for d in data:
            self.create_explore_band(d, count);
            count += 1;

    def create_explore_band(self, data_instance, position):
        self.main_view.explore_band_container.band_list.append(ExploreBand(orientation = "horizontal"));
        self.main_view.explore_band_container.band_list[position].location_id = data_instance.location_id;
        self.main_view.explore_band_container.band_list[position].add_widget(LocationName(text = data_instance.location_name));
        self.main_view.explore_band_container.band_list[position].add_widget(LocationRating(text = data_instance.location_rating));
        self.main_view.explore_band_container.band_list[position].add_widget(LocationType(text = data_instance.location_type));

        self.main_view.explore_band_container.add_widget(self.main_view.explore_band_container.band_list[position]);

    #Data_set is the dictionary with meeting information
    #Turn it into a meeting band
    def prepare_data(self, data_set):
        data = ExploreLayoutData()
        data.location_id = data_set['meeting_id']
        data.location_name = data_set['meeting_name']
        data.location_rating = data_set['meeting_partner']
        data.location_type = data_set['meeting_date']

        return data
        #self.app.get_data(); #we ask the server nicely for the current user's meetings

    def update_locations(self, location_list):
        self.main_view.band_list.clear()
        self.main_view.clear_widgets()

        for location in location_list:
            print(meeting)
            datum = self.prepare_data(location)
            self.create_location_band(datum, len(self.main_view.explore_band_container.band_list))



class ExploreBandContainer(BoxLayout):
    pass;

class ExploreBand(MDCard):
    location_id = None; #keep track of the meeting_id so that we can kill it later, maybe

    def on_touch_down(self, touch):
        location_info_popup = LocationInfoPopup(self.location_id); #might pass that to the MeetingInfoPopup so that we can display all the info
        location_info_popup.open();

class LocationName(Label):
    pass;
class LocationRating(Label):
    pass;
class LocationType(Label):
    pass;

class ExploreLayoutData: #this is the data class the meetinglayout will be using
    location_id = None;
    location_name = None;
    location_rating = None;
    location_type = None;
