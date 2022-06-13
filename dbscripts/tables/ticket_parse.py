import csv

def space_delimiter(Str, Select):
    '''
    returns either the portion of the string before the first " " in the string or everything after
    depending on Selector

    space_delimiter: Str, Str => Str
    '''
    str1 = ""
    str2 = ""
    bool = False
    for letter in Str:
        if bool == True:
            str2 = str2+letter
        elif letter == " ":
            bool = True
        else:
            str1 = str1+letter
    if Select == "Back":
        return str2
    elif Select == "Front":
        return str1
    else:
        return "Invalid Select in space_delimiter in ticket_parse.py"

class ticket:
    def __init__(self, Msg, ModuleID, TowerID_Street, Timestamp, Lat, Long):
        self.message = Msg
        self.moduleid = ModuleID
        self.towerid = space_delimiter(TowerID_Street, "Front")
        self.street = space_delimiter(TowerID_Street, "Back")
        self.timestamp = Timestamp
        self.lat = Lat
        self.long = Long

    def __repr__(self):
        s = "Error: {0.message}, ModuleID: {0.moduleid}, TowerID: {0.towerid}, Street: {0.street},\
             Time and Date: {0.timestamp}, Latitude: {0.lat}, Longitude: {0.long}"
        return s.format(self)

    def __eq__(self, other):
        return isinstance(other, ticket) and\
            self.message == other.message and\
            self.moduleid == other.moduleid and\
            self.towerid == other.towerid and\
            self.street == other.street and\
            self.timestamp == other.timestamp and\
            self.lat == other.lat and\
            self.long == other.long
    
    