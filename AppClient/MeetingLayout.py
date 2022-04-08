from kivy.lang import Builder;
import kivy.uix.scrollview from ScrollView;
from kivy.uix.label import Label;
from kivy.properties import NumericProperty, ReferenceListProperty;

from kivymd.uix.card import MDCard;

Builder.load_string("""
<MeetingName>:
<MeetingInsigator>:
<MeetingDate>
<MeetingBand>
    orientation: horizontal

    MeetingName:
        id: meeting_name
    MeetingInsigator:
        id: meeting_instigator
    MeetingDate:
        id: meeting_date
""")

class MeetingLayout(ScrollView):
    def __init__(self, *args, **kwargs):
        super(MeetingLayout, self).__init__(*args, **kwargs);

        self.prepare_data();
        self.init_ui();

    def init_ui(self):
        pass;
    def create_meeting_band(self):
        pass;
    def prepare_data(self):
        pass;
    def on_touch_move(self, touch):
        pass;

class MeetingBand(Card):
    pass;

class MeetingName(Label):
    pass;
class MeetingInsigator(Label):
    pass;
class MeetingDate(Label):
    pass;
