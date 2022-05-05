# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
import os
import json
import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import mysql.connector
from scipy.spatial import cKDTree
from geographiclib.geodesic import Geodesic
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from scipy import inf

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


# Class to handle the data sent from connection. Each instance is connection
class MITMServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


# Factory class to initialize new connections as MITMServer classes
class MITMServerFactory(protocol.Factory):
    protocol = MITMServer

    def __init__(self, app):
        self.app = app


# App that runs it all
class MITMServerApp(App):
    label = None
    textbox = None

    #Connecting to db. Cursor is used to query the db. connection is for commiting a edit to the db
    def database_auth():
            try:
                connection = mysql.connector.connect(
                    user='doadmin',
                    password ='AVNS_WZEScW_Y5FNKr7m',
                    host='db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com',
                    port = 25060,
                    database='defaultdb'
                )
                print('\n[+] Connected to db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com Successfully')

                cursor = connection.cursor()

                return cursor, connection
            except BaseException as e:
                print(str(e))
    # Databse Connection vars. connectionarray holds variables to query and modify db

    connectorarr = database_auth()
    cursor = connectorarr[0]
    connection = connectorarr[1]

    # Initializing the server
    def build(self):
        root = self.setup_gui()
        self.listen_for_client()
        return root

    # Setting up the gui
    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    # Waiting for client connection
    def listen_for_client(self):
        #reactor.listenTCP(25565, MITMServerFactory(self))
        reactor.listenTCP(8000, MITMServerFactory(self))

    # Taking input from console line and processing it locally on server
    def send_message(self, *args):
        msg = self.textbox.text
        if msg:
            self.print_message(f"{msg}")
            self.textbox.text = ""
            return (msg.encode('utf-8'))

    # Handling the messages sent by the client
    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.print_message("\nreceived:  {}\n".format(msg))
        msg = json.loads(msg)
        response = "failure"

        # Checking for keywords from input
        if msg['command'] == "login":
            self.print_message("Starting Login Process")
            response = self.auth_login(msg)
            self.print_message(f"Response: {response['result']}")

        # Checking for registration
        if msg['command'] == "register":
            self.print_message("Starting Registration Process")
            response = self.auth_regi(msg)

        # Checking for Creation of new meeting
        if msg['command'] == 'create_meeting':
            self.print_message("Starting New Meeting")
            self.new_meeting(msg)

        # Checking for update pings
        if msg['command'] == 'ping_meetings':
            self.print_message("Ping Update")
            response = self.ping_update(msg)


        self.label.text += "responded: {}\n".format(response)
        return (json.dumps(response).encode('utf-8'))

    # Print message to console on server
    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)

    # Defining the authentication function
    def auth_login(self, msg):
        # Setting up json message to send back
        response = {'command': 'auth_login'}

        self.cursor.execute("Select * From User where Username = '{}' and Password = '{}' ".format(msg['username'],msg['password']))
        result = self.cursor.fetchall()
        if(result == []):
            response['result'] = "fail"
        else:
            response['result'] = "success"
            response['username'] = msg['username']
        return response

    # Defining the registration function
    def auth_regi(self, msg):
        response = {'command': 'auth_register'}
        #TODO change * to username
        self.cursor.execute(f"Select * From User where Username = \'{msg['username']}\'")
        result = self.cursor.fetchall()
        self.print_message(result)
        if(result != []):
            response['result'] = "username_exists"
            self.print_message(response)
            return response

        self.cursor.execute(f"Select * From User where Email = \'{msg['email']}\' ")
        result = self.cursor.fetchall()
        if(result != []):
            response['result'] = "email_exists"
            self.print_message(response)
            return response


        sql = 'INSERT INTO User (Name, Email, Password, Username) VALUES (%s,%s,%s,%s)'
        val = (msg['name'], msg['email'], msg['password'], msg['username'])
        self.cursor.execute(sql,val)
        self.connection.commit()

        response['result'] = "success"
        response['username'] = msg['username']
        return response

    # Defining the new meeting creation function
    meetingIDList = []
    def new_meeting(self, msg):
        newMeetingID = random.randint(10000,99999)
        while(self.meetingIDList.__contains__(newMeetingID) == True):
            newMeetingID = random.randint(10000,99999)
        self.meetingIDList.append(newMeetingID)
        #{"command": "create_meeting", "meeting_instigator": "kalvin", "meeting_partner": Wesley, "instigator_location": "123, Sesame Street", "date": "1/5/2019", "time": "17:15"}//
        sql = "INSERT INTO defaultdb.Meeting (MeetingID, User1, User2, MeetingTime, LocationID, mp_lon, mp_lat, user1_Addr, user2_Addr, meeting_Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (newMeetingID, msg['meeting_instigator'], msg['meeting_partner'], msg['time'], '0', '1.1', '1.1', msg['instigator_location'], 'PENDING', 'PENDING')
        self.cursor.execute(sql,val)
        self.connection.commit()

        #if user2 accepts
        #insert the user2 addr, meeting_status into the db
        #call midpoint with the two user locations {We should just make that function convert the locs to lat and long}
        #assign the users one of the locations between them
        #insert the locationID of the assigned place to db


        # Make new table entry in database
        # add user information from given login
        # Find other user and send invite by adding it to table in database
            # This may require on login/ random refresh for users to check for any invites.
        # Here is what we want passed to server
            # datetime
            # Locations filters
            # User invited
            # user ID (for location finding in DB)
        self.print_message("Inside new_meeting Function")
        # self.print_message(f"Meeting Instigater: {msg["meeting_instigator"]}")
        # self.print_message(f"Meeting Partner: {msg["meeting_partner"]}")
        # self.print_message(f"Instigater Location: {msg["instigator_location"]}")
        # self.print_message(f"Date: {msg["date"]}")
        # self.print_message(f"Time: {msg["time"]}")

        # SQL Command to create a new meeting with these Item printed above
            #

    # This function gets the mid point between two locations
    def findMidPoint(self, loc1X, loc1Y, loc2X, loc2Y):
        # taking two users location and finding the mid point and returning it
        l = Geodesic.WGS84.InverseLine(loc1X, loc1Y, loc2X, loc2Y)
        m = l.Position(0.5 * l.s13)

        # Creating json to return
        midpoint = {'command': 'midpoint'}
        midpoint['lat'] = m['lat2']
        midpoint['lon'] = m['lon2']

        return midpoint

    # This function works for updating client by set pinging intervals
    def ping_update(self, msg):
        # breaking down the message passed
        username = msg['user']

        # quering the DB for list of meeting information based on username
        # Tbales: User, Meeting, Locations.
        # Meeting contains username(s). Search through meeting table and
        # Return all meetings with user involved
        sql = 'SELECT * FROM Meeting WHERE User1 = (%s) OR User2 = (%s)'
        val = (username, username)
        self.cursor.execute(sql, val)
        meetings = self.cursor.fetchall()

        # Stored as an array:
        # 0: MeetingID
        # 1: User1
        # 2: User2
        # 3: MeetingTime
        # 4: LocationID
        # 5: mp_lon
        # 6: mp_lat
        # 7: user1_Addr
        # 8: User2_Addr
        # 9: meeting_status
        keys = ['meeting_id', 
                'meeting_instigator', 
                'meeting_partner', 
                'meeting_time',
                'location_ID',
                'mp_lon', 
                'mp_lat',
                'meeting_instigator_addr',
                'meeting_partner_addr',
                'meeting_status']

        keys_for_user = ['meeting_id', 
                'meeting_instigator', 
                'meeting_partner', 
                'meeting_time',
                'location_ID',
                'mp_lon', 
                'mp_lat',
                'meeting_status']

        response_meetings = []

        for meeting in meetings:
            meetings_as_dict = dict(zip(keys, meeting))
            response_meetings.append({k:v for k,v in meetings_as_dict.items() if k in keys_for_user})

        self.print_message(f"Size of Meeting: {len(meetings)}")

        # Creating a json to send back to client
        response = {'command' : 'user_meetings'}
        response['#_of_meetings'] = len(meetings)
        response['meetings'] = response_meetings

        # Returning the meetings to the client
        return response

    # Function to update the meeting in the SQL database
    def update_meeting(self, msg):
        user1Coords = []
        user2Coords = []
        # This is used for accepting/rejecting a meeting.
        self.print_message(f"Updating Meeting: {msg['meeting']['meeting_id']} to {msg['meeting']['meeting_status']} Location2: {msg['meeting']['user2_Addr']}")
        id = msg['meeting']['meeting_id']
        self.cursor.execute(f'SELECT * FROM Meeting WHERE MeetingID = {id}')
        tempmeeting = self.cursor.fetchall()
        user1CoordsTemp = tempmeeting[0][7]
        user1Coords = user1CoordsTemp.split(",")
        user2CoordsTemp = msg['meeting']['user2_Addr']
        user2Coords = user2CoordsTemp.split(",")
        midCoords = self.findMidPoint(float(user1Coords[0]), float(user1Coords[1]), float(user2Coords[0]), float(user2Coords[1]))
        midLat = midCoords['lat']
        midLon = midCoords['lon']
        sql = 'UPDATE Meeting SET meeting_Status = (%s), user2_Addr = (%s), mp_lon = (%s), mp_lat = (%s) WHERE MeetingID = (%s)'
        val = (msg['meeting']['meeting_status'], msg['meeting']['user2_Addr'], midLon, midLat, msg['meeting']['meeting_id'])
        self.cursor.execute(sql, val)
        self.connection.commit()

        return "Sucessful"




if __name__ == '__main__':
    MITMServerApp().run()
