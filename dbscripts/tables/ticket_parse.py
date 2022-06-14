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

def ticket_parse(filename_in):
    '''
    Reads in and parses csv file filename_in from cell tower with 6 columns: Message,
    Equipment, Tower, RegDate, TowerLatitude, and TowerLongitude. Writes to file ticket.sql
    which is a script that will add the tickets from filename_in into the database. If
    no longitude or latitude is provided, their values will be listed as "No Value" and
    the corresponding geometry will be "POINT (0 0)".

    Effects:
        Reads file named filename_in
        Writes to file named "ticket.sql"

    ticket_parse_temp: Str => None
    '''
    prefix = ""
    outputtext = ""
    with open(filename_in, "r") as ct_ticket:
        csv_reader = csv.reader(ct_ticket, delimiter = ",")
        line_count = 0

        for row in csv_reader:
            if line_count>1:
                prefix = "\n\n"

            if (row[4]=="" or row[5]=="") and line_count>1:
                outputtext = outputtext + prefix + 'INSERT INTO public.ctt_tickets(\nticket_id, \"TowerID\",\
\"TowerStreet\", \"ModuleID\", \"ErrorCode\", \"ErrorDetails\", \"ErrorDateTime\",\
\"AssignedUser_ID\", \"AssignedDateTime\", \"Ticket_Status\", \"CompletedDateTime\",\
\"Longitude\", \"Latitude\", geom)\nVALUES (gen_random_uuid(),\
\''+ space_delimiter(row[2], "Front")+'\', \''+ space_delimiter(row[2], "Back")+'\',\
\''+row[1]+'\', \'\', \''+row[0]+'\',\
\''+row[3]+'\', \'\', \''+row[3]+'\', \'0\',\
\''+row[3]+'\', \'No Value\', \'No Value\',\
\'POINT'+"(0 0)"+'\' );'
                line_count = line_count+1

            elif line_count>1:
                outputtext = outputtext + prefix + 'INSERT INTO public.ctt_tickets(\nticket_id, \"TowerID\",\
\"TowerStreet\", \"ModuleID\", \"ErrorCode\", \"ErrorDetails\", \"ErrorDateTime\",\
\"AssignedUser_ID\", \"AssignedDateTime\", \"Ticket_Status\", \"CompletedDateTime\",\
\"Longitude\", \"Latitude\", geom)\nVALUES (gen_random_uuid(),\
\''+ space_delimiter(row[2], "Front")+'\', \''+ space_delimiter(row[2], "Back")+'\',\
\''+row[1]+'\', \'\', \''+row[0]+'\',\
\''+row[3]+'\', \'\', \''+row[3]+'\', \'0\',\
\''+row[3]+'\', \''+row[4]+'\', \''+row[5]+'\',\
\'POINT'+"("+row[4]+" "+row[5]+")"+'\' );'
                line_count = line_count+1

            else:
                line_count = line_count+1

    ct_ticket.close
    ticketoutput = open("D:\Actual program files lol\\repo\ctt\dbscripts\\tables\TestOutput\\ticket.sql", "w")
    ticketoutput.write(outputtext)
    ticketoutput.close
    pass

'''
#Test using messages.csv

ticket_parse("D:\\Actual program files lol\\repo\ctt\dbscripts\\tables\\messages.csv")
'''

'''
#Class for ticket, currently not used
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

'''