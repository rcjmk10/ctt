from collections import UserDict, UserList
import json
from operator import methodcaller
from threading import local
from turtle import update
from urllib.request import urlretrieve
from flask import Flask, render_template, request, redirect, \
url_for, flash, make_response, session, jsonify
from flask import render_template
import psycopg2

'''
all functions have redirect to login page if no authentication token or if authentication token is false.
all functions as of 7/25/2022 have a redirect
future functions will use following copy paste if/else statements cause its easier than one if statement and appending a return at the end of the function if the if statement returns false.:

if not("authenticationtoken" in session) and not(session["authenticationtoken"]):
    return redirect(url_for("login"))
else:
    #code here
'''

app = Flask(__name__)
app.secret_key = "any random string"

Userlat = 0
Userlong = 0
logout_link = "<b><a href = '/logout'>click here to log out</a></b>"
navbar = '''
<ul>
    <li><a href="/tickets">All Tickets</a></li>
    <li><a href="/tickets/worklist">My Worklist</a></li>

    <style>
        li {
            display: inline;
        }
    </style>
</ul>
'''

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



ticketlisttemplate = '''
        <tr>
            <!--<td>
                {0}
            </td>-->
            <td>
                {1}
            </td>
            <td>
                {2}
            </td>
            <td>
                {3}
            </td>
            <td>
                {4}
            </td>
            <td>
                {5}
            </td>
            <td>
                {6}
            </td>
            <td>
                {7}
            </td>
            <td>
                {8}
            </td>
            <td>
                {9}
            </td>
            <td>
                {10}
            </td>
            <td>
                {11}
            </td>
            <td>
                {12}
            </td>
            <td>
                <input type=button value="assign to myself" onclick="window.open('/tickets/addtoworklist?ticketid={0}')">
            </td>
        </tr>
'''

ticketlisttemplateassigned = '''
        <tr>
            <!--<td>
                {0}
            </td>-->
            <td>
                {1}
            </td>
            <td>
                {2}
            </td>
            <td>
                {3}
            </td>
            <td>
                {4}
            </td>
            <td>
                {5}
            </td>
            <td>
                {6}
            </td>
            <td>
                {7}
            </td>
            <td>
                {8}
            </td>
            <td>
                {9}
            </td>
            <td>
                {10}
            </td>
            <td>
                {11}
            </td>
            <td>
                {12}
            </td>
            <td>
                Already Assigned
            </td>
        </tr>
'''

ticketlisttemplategetnewticket = '''
        <tr>
            <!--<td>
                {0}
            </td>-->
            <td>
                {1}
            </td>
            <td>
                {2}
            </td>
            <td>
                {3}
            </td>
            <td>
                {4}
            </td>
            <td>
                {5}
            </td>
            <!--<td>
                {6}
            </td>-->
            <!--<td>
                {7}
            </td>-->
            <!--<td>
                {8}
            </td>-->
            <td>
                {9}
            </td>
            <td>
                {10}
            </td>
            <td>
                {11}
            </td>
            <td>
                {12}
            </td>
            <td>
                {13}
            </td>    
            <td>
                <input type=button value="assign to myself" onclick="window.open('/tickets/addtoworklist?ticketid={0}')">
            </td>
        </tr>
'''

ticketlisttemplateworklist = '''
        <tr>
            <!--<td>
                {0}
            </td>-->
            <td>
                {1}
            </td>
            <td>
                {2}
            </td>
            <td>
                {3}
            </td>
            <td>
                {4}
            </td>
            <td>
                {5}
            </td>
            <td>
                {6}
            </td>
            <!--<td>
                {7}
            </td>-->
            <td>
                {8}
            </td>
            <td>
                {9}
            </td>
            <td>
                {10}
            </td>
            <td>
                {11}
            </td>
            <td>
                {12}
            </td>
            <td>
                <input type=button value="Update Status" onclick="window.open('/tickets/modifyticket?ticketid={0}&date='+Date())\">
                <script>
                document.getElementById("current_date".innerHTML = Date());
                </script>
            </td>

        </tr>
'''



@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      session['email'] = request.form['email']
      session['password'] = request.form['password']
      session['authenticationtoken'] = False
      if authenticate(session['email'], session['password']):
        session['authenticationtoken'] = True
        return redirect(url_for('worklist'))
   return """
   <form action = "/login" method = "post">
      <label for="email">Email:</label>
      <p><input type = "text" name = "email"/></p>
      <label for="password">Password:</label>
      <p><input type = "password" name = "password"/></p>
      <p><input type = submit value = "Login"/></p>
   </form>	
""" 

def authenticate(id, passw):
    conn = None
    local_content=""
    try:
        conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
        cur = conn.cursor()

        #Statement Execution
        print('PostgreSQL vers:')
        cur.execute('SELECT * from public.ctt_users WHERE \"EmailAddr\" = \'' + id + '\'')

        #Consolidate info from query
        local_content = cur.fetchall()
        '''
        for localuser in local_users:
            local_content=local_content+", "+str(localuser[0])+", "+str(localuser[1])+", "+str(localuser[2])
            '''

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    if len(local_content) == 1:
        print(local_content)
        print("uuid = " + (local_content[0])[0])
        session['uuid'] = (local_content[0])[0]
        session['name'] = (local_content[0])[3] + " " + (local_content[0])[4]
        return True
    else:
        print("Invalid Login, Authentication Failed")
        return False

@app.route('/')
def home():
    return navbar + "<br" + "Not Logged in,\n" + "<b><a href = '/login'>click here to log in</a></b>"

@app.route('/tickets', methods = ['POST', 'GET'])
def tickets():
    sort = request.args.get("sort")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    logout_link = "<b><a href = '/logout'>click here to log out</a></b>" + "\n"
    worklist_link = "<b><a href = '/tickets/worklist'>Your Tickets</a></b>"
    dropdown_sort = '''
        <select id="sort">
        <option value="0">Newest</option>
        <option value="10">Distance</option>
        </select>

        <br><br>

        <button onclick = "
        var sort=document.getElementById('sort').value;
        window.location.replace('/tickets?sort='+sort);">Sort</button>  
        '''
    if ("authenticationtoken" in session) and session['authenticationtoken']:
        
        if sort=="0":
            conn = None
            local_content=""
            try:
                conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
                cur = conn.cursor()

                #Statement Execution
                print('PostgreSQL vers:')
                cur.execute('SELECT * from ctt_tickets\nORDER BY "ErrorDateTime" DESC')

                #Consolidate info from query
                local_content = cur.fetchall()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
                    #print(local_content[0])
                ticketlisthtml = ""

                for row in local_content:
                    status = ""
                    if row[9] == "0":
                        status = "Just Assigned"
                    elif row[9] == "10":
                        status = "Work in Progress"
                    elif row[9] == "20":
                        status = "Pending Info"
                    elif row[9] == "100":
                        status = "Completed"
                    else:
                        status = "err: invalid status value"
                    if row[7] == '':
                        ticketlisthtml = ticketlisthtml + ticketlisttemplate.format(row[0], row[1], row[2], row[3], \
                        row[4], row[5], row[6], row[7], row[8], status, row[-4], row[-3], row[-2])
                    else:
                        ticketlisthtml = ticketlisthtml + ticketlisttemplateassigned.format(row[0], row[1], row[2], row[3], \
                        row[4], row[5], row[6], row[7], row[8], status, row[-4], row[-3], row[-2])
                return navbar+ "<br>" + "Ticket List\n" + worklist_link + dropdown_sort + "\n" + '''
                <button onclick="getLocation()">Click to get closest tickets</button>

                <p id="locate"></p>

                <script>
                var x = document.getElementById("locate");

                function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition);
                } else { 
                    x.innerHTML = "Geolocation is not supported by this browser.";
                }
                }

                function showPosition(position) {
                var localurl = "/getnewticket?latitude="+position.coords.latitude+"&longitude="+position.coords.longitude;
                window.open(localurl);
                x.innerHTML = "Latitude: " + position.coords.latitude + 
                "<br>Longitude: " + position.coords.longitude;
                }
                </script>
                ''' +\
                logout_link + '''
                <html>
                    <table border="1" align="center">
                        <tr>
                            <!--<td>
                                TicketID
                            </td>-->
                            <td>
                                TowerID
                            </td>
                            <td>
                                TowerStreet
                            </td>
                            <td>
                                ModuleID
                            </td>
                            <td>
                                ErrorCode
                            </td>
                            <td>
                                ErrorDetails
                            </td>
                            <td>
                                ErrorDateTime
                            </td>
                            <td>
                                AssignedUser_ID
                            </td>
                            <td>
                                AssignedDateTime
                            </td>
                            <td>
                                Ticket_Status
                            </td>
                            <td>
                                UpdatedDateTime
                            </td>
                            <td>
                                Latitude
                            </td>
                            <td>
                                Longitude
                            </td>
                        </tr>
                ''' + ticketlisthtml
        elif sort == "10":
            print("wat")
            return redirect(url_for("getlocation"))
        elif sort == "11":
            latitude = request.args.get("latitude")
            longitude = request.args.get("longitude")
            
            selectquery = '''
            SELECT *, ST_Distance('POINT({0} {1})', concat('POINT(', "Latitude", ' ', "Longitude", ')')) AS l_distance FROM ctt_tickets\
            ORDER BY ST_Distance('POINT({0} {1})', concat('POINT(', "Latitude", ' ', "Longitude", ')')) ASC
            '''.format(latitude, longitude)
            #print(selectquery)
            local_content = ""
            conn = None
            try:
                conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
                cur = conn.cursor()

                #Statement Execution
                print('PostgreSQL vers:')
                cur.execute(selectquery)
                local_content = cur.fetchall()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
                    ticketlisthtml = ""
                    print(local_content)
                    for row in local_content:
                        status = ""
                        if row[9] == "0":
                            status = "Just Assigned"
                        elif row[9] == "10":
                            status = "Work in Progress"
                        elif row[9] == "20":
                            status = "Pending Info"
                        elif row[9] == "100":
                            status = "Completed"
                        if row[7] == '':
                            ticketlisthtml = ticketlisthtml + ticketlisttemplate.format(row[0], row[1], row[2], row[3], \
                            row[4], row[5], row[6], row[7], row[8], status, row[-4], row[-3], row[-2])
                        else:
                            ticketlisthtml = ticketlisthtml + ticketlisttemplateassigned.format(row[0], row[1], row[2], row[3], \
                            row[4], row[5], row[6], row[7], row[8], status, row[-4], row[-3], row[-2])
                return navbar+ "<br>" + "Ticket List\n" + worklist_link + dropdown_sort + "\n" + '''
                <button onclick="getLocation()">Click to get closest tickets</button>

                <p id="demo"></p>

                <script>
                var x = document.getElementById("demo");

                function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition);
                } else { 
                    x.innerHTML = "Geolocation is not supported by this browser.";
                }
                }

                function showPosition(position) {
                var localurl = "/getnewticket?latitude="+position.coords.latitude+"&longitude="+position.coords.longitude;
                window.open(localurl);
                x.innerHTML = "Latitude: " + position.coords.latitude + 
                "<br>Longitude: " + position.coords.longitude;
                }
                </script>
                ''' +\
                logout_link + '''
                <html>
                    <table border="1" align="center">
                        <tr>
                            <!--<td>
                                TicketID
                            </td>-->
                            <td>
                                TowerID
                            </td>
                            <td>
                                TowerStreet
                            </td>
                            <td>
                                ModuleID
                            </td>
                            <td>
                                ErrorCode
                            </td>
                            <td>
                                ErrorDetails
                            </td>
                            <td>
                                ErrorDateTime
                            </td>
                            <td>
                                AssignedUser_ID
                            </td>
                            <td>
                                AssignedDateTime
                            </td>
                            <td>
                                Ticket_Status
                            </td>
                            <td>
                                UpdatedDateTime
                            </td>
                            <td>
                                Latitude
                            </td>
                            <td>
                                Longitude
                            </td>
                        </tr>
                ''' + ticketlisthtml
        conn = None
        user_location=""
        local_content=""
        try:
            conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
            cur = conn.cursor()

            #Statement Execution
            print('PostgreSQL vers:')
            cur.execute('SELECT * from ctt_tickets')

            #Consolidate info from query
            local_content = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                #print(local_content[0])
            ticketlisthtml = ""

            for row in local_content:
                status = ""
                if row[9] == "0":
                    status = "Just Assigned"
                elif row[9] == "10":
                    status = "Work in Progress"
                elif row[9] == "20":
                    status = "Pending Info"
                elif row[9] == "100":
                    status = "Completed"
                else:
                    status = "err: invalid status value"
                if row[7] == '':
                    ticketlisthtml = ticketlisthtml + ticketlisttemplate.format(row[0], row[1], row[2], row[3], \
                    row[4], row[5], row[6], row[7], row[8], status, row[-4], row[-3], row[-2])
                else:
                    ticketlisthtml = ticketlisthtml + ticketlisttemplateassigned.format(row[0], row[1], row[2], row[3], \
                    row[4], row[5], row[6], row[7], row[8], status, row[-4], row[-3], row[-2])
            return navbar+ "<br>" + "Ticket List\n" + worklist_link + dropdown_sort + "\n" + '''
            <button onclick="getLocation()">Click to get closest tickets</button>

            <p id="demo"></p>

            <script>
            var x = document.getElementById("demo");

            function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            } else { 
                x.innerHTML = "Geolocation is not supported by this browser.";
            }
            }

            function showPosition(position) {
            var localurl = "/getnewticket?latitude="+position.coords.latitude+"&longitude="+position.coords.longitude;
            window.open(localurl);
            x.innerHTML = "Latitude: " + position.coords.latitude + 
            "<br>Longitude: " + position.coords.longitude;
            }
            </script>
            ''' +\
             logout_link + '''
            <html>
                <table border="1" align="center">
                    <tr>
                        <!--<td>
                            TicketID
                        </td>-->
                        <td>
                            TowerID
                        </td>
                        <td>
                            TowerStreet
                        </td>
                        <td>
                            ModuleID
                        </td>
                        <td>
                            ErrorCode
                        </td>
                        <td>
                            ErrorDetails
                        </td>
                        <td>
                            ErrorDateTime
                        </td>
                        <td>
                            AssignedUser_ID
                        </td>
                        <td>
                            AssignedDateTime
                        </td>
                        <td>
                            Ticket_Status
                        </td>
                        <td>
                            UpdatedDateTime
                        </td>
                        <td>
                            Latitude
                        </td>
                        <td>
                            Longitude
                        </td>
                    </tr>
            ''' + ticketlisthtml
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
   # remove the email and password from the session if it is there
   session.pop('email', None)
   session.pop('password', None)
   session.pop('authenticationtoken', False)
   return redirect(url_for('home'))

@app.route('/getlocation')
def getlocation():
    return '''
                <body onload="getLocation()">...Getting Location...</body>

                <p id="locate"></p>

                <script>
                var x = document.getElementById("locate");

                function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition);
                } else { 
                    x.innerHTML = "Geolocation is not supported by this browser.";
                }
                }

                function showPosition(position) {
                var localurl = "/tickets?sort=11&latitude="+position.coords.latitude+"&longitude="+position.coords.longitude;
                window.location.replace(localurl);
                x.innerHTML = "Latitude: " + position.coords.latitude + 
                "<br>Longitude: " + position.coords.longitude;
                }
                </script>
                ''' 


@app.route('/tickets/addnewticket', methods = ['POST'])
def process_json():
    #Not sure if authentication is necessary for this function

    conn = None

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        template = 'INSERT INTO ctt_tickets(\nticket_id, \"TowerID\",\
\"TowerStreet\", \"ModuleID\", \"ErrorCode\", \"ErrorDetails\", \"ErrorDateTime\",\
\"AssignedUser_ID\", \"AssignedDateTime\", \"Ticket_Status\", \"CompletedDateTime\",\
\"Latitude\", \"Longitude\", geom)\nVALUES (gen_random_uuid(),\
\'{0}\', \'{1}\',\
\'{2}\', \'\', \'{3}\',\
\'{4}\', \'\', \'{4}\', \'0\',\
\'{4}\', \'{5}\', \'{6}\',\
\'POINT'+"({5} {6})"+'\' );'

        ticket = request.json
        insertcommand = ""
        towerid = space_delimiter(ticket["Tower"], "Front")
        towerstreet = space_delimiter(ticket["Tower"], "Back")
        moduleid = ticket["Equipment"]
        #errorcode = ""
        errordetails = ticket["Message"]
        errordatetime = ticket["RegDate"]
        #assigneduserid = ""
        #assigneddatetime = ticket["RegDate"]
        #ticketstatus = "0"
        #completeddatetime = ticket["RegDate"]
        long = ticket["TowerLongitude"]
        lat = ticket["TowerLatitude"]

        insertcommand = template.format(towerid, towerstreet, moduleid, errordetails, errordatetime, long, lat)
        print(insertcommand)

        try:
            conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
            cur = conn.cursor()

            #Statement Execution
            cur.execute(insertcommand)
            conn.commit()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
            return insertcommand
    else:
        return 'Content-Type not supported!'

@app.route('/tickets/worklist', methods = ['POST', 'GET'])
def worklist():
    
    if ("authenticationtoken" in session) and session['authenticationtoken']:
        conn = None
        local_content=""
        

        locationlist = ""
        try:
            conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
            cur = conn.cursor()

            #Statement Execution
            print('PostgreSQL vers:')
            cur.execute('SELECT * from ctt_tickets WHERE \"AssignedUser_ID\" = \''+session['uuid']+'\'')

            #Consolidate info from query
            local_content = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                print(local_content)
            ticketlisthtml = ""
            for row in local_content:
                locationlist = locationlist + "[{0}, {1}, '{2}'], ".format(row[-3], row[-2], (row[2] + ", " + row[3] + ", " + row[5]))
                status = ""
                if row[9] == "0":
                    status = "Just Assigned"
                elif row[9] == "10":
                    status = "Work in Progress"
                elif row[9] == "20":
                    status = "Pending Info"
                elif row[9] == "100":
                    status = "Completed"
                
                ticketlisthtml = ticketlisthtml + ticketlisttemplateworklist.format(row[0], row[1], row[2], row[3], \
                row[4], row[5], row[6], row[7], row[8], status, row[-4], row[-3], row[-2])
            print(locationlist)
            mapview = "\
    <script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>\
    <script type=\"text/javascript\">\n\
      google.charts.load(\"current\", {\n\
        \"packages\":[\"map\"],\n\
        // Note: you will need to get a mapsApiKey for your project.\n\
        // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings\n\
        \"mapsApiKey\": \"AIzaSyCkae3VLDmnW7jFEIjJQ3e3rG-3NBq3ZQQ\"\n\
      });\
      google.charts.setOnLoadCallback(drawChart);\n\
      function drawChart() {\n\
        var data = google.visualization.arrayToDataTable([\
          [\'Lat\', \'Long\', \'Name\'], " + locationlist + "\n\
        ]);\n\
\n\
        var options = {\n\
          icons: {\n\
            default: {\n\
              normal: \'https://icons.iconarchive.com/icons/icons-land/vista-map-markers/48/Map-Marker-Ball-Azure-icon.png\',\n\
              selected: \'https://icons.iconarchive.com/icons/icons-land/vista-map-markers/48/Map-Marker-Ball-Right-Azure-icon.png\'\n\
            }\n\
          },\n\
          showTooltip: true,\n\
          showInfoWindow: true\n\
\n\
        };\n\
\n\
        var map = new google.visualization.Map(document.getElementById(\'map_markers_div\'));\n\
        map.draw(data, options);\n\
      }\n\
\n\
    </script>\n\
\n\
    <div id=\"map_markers_div\" style=\"width: 400px; height: 300px\"></div>"
        return navbar + "<br>" + "Assigned Tickets\n" + logout_link + "<br>" + "<b><a href = '/tickets'>Ticket List</a></b>" + "<br>"\
            + '''
            <html>
                <table border="1" align="center">
                    <tr>
                        <!--<td>
                            TicketID
                        </td>-->
                        <td>
                            TowerID
                        </td>
                        <td>
                            TowerStreet
                        </td>
                        <td>
                            ModuleID
                        </td>
                        <td>
                            ErrorCode
                        </td>
                        <td>
                            ErrorDetails
                        </td>
                        <td>
                            ErrorDateTime
                        </td>
                        <!--<td>
                            AssignedUser_ID
                        </td>-->
                        <td>
                            AssignedDateTime
                        </td>
                        <td>
                            Ticket_Status
                        </td>
                        <td>
                            UpdatedDateTime
                        </td>
                        <td>
                            Latitude
                        </td>
                        <td>
                            Longitude
                        </td>
                    </tr>
            ''' + ticketlisthtml + "<br>" + mapview
    return redirect(url_for("login"))


@app.route('/tickets/addtoworklist', methods = ['POST', 'GET'])
def add_to_worklist():
    if ("authenticationtoken" in session) and session["authenticationtoken"]:
        update_query = "UPDATE public.ctt_tickets\nSET \"AssignedUser_ID\" = \'{0}\'\nWHERE \"ticket_id\" = \'{1}\';".format(session["name"], request.args.get("ticketid"))
        print(update_query)
        conn = None
        try:
            conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
            cur = conn.cursor()

            #Statement Execution
            print('PostgreSQL vers:')
            cur.execute(update_query)
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        return redirect(url_for("tickets"))
    return redirect(url_for("login"))

@app.route('/getnewticket')
def getnewticket():
    if ("authenticationtoken" in session) and session["authenticationtoken"]:
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
        
        selectquery = '''
        SELECT *, ST_Distance('POINT({0} {1})', concat('POINT(', "Latitude", ' ', "Longitude", ')')) AS l_distance FROM ctt_tickets\
        WHERE \"AssignedUser_ID\" = \'\'
        ORDER BY ST_Distance('POINT({0} {1})', concat('POINT(', "Latitude", ' ', "Longitude", ')')) ASC\
        limit 10
        '''.format(latitude, longitude)
        #print(selectquery)
        local_content = ""
        conn = None
        try:
            conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
            cur = conn.cursor()

            #Statement Execution
            print('PostgreSQL vers:')
            cur.execute(selectquery)
            local_content = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                ticketlisthtml = ""
                print(local_content)
                for row in local_content:
                    status = ""
                    if row[9] == "0":
                        status = "Just Assigned"
                    elif row[9] == "10":
                        status = "Work in Progress"
                    elif row[9] == "20":
                        status = "Pending Info"
                    elif row[9] == "100":
                        status = "Completed"
                    ticketlisthtml = ticketlisthtml + ticketlisttemplategetnewticket.format(row[0], row[1], row[2], row[3], \
                    row[4], row[5], row[6], row[7], row[8], row[-5], status, row[-4], row[-3], row[-1])
                return navbar + "<br>" + "Closest 10 Tickets:\n" + logout_link + '''
                <html>
                    <table border="1" align="center">
                        <tr>
                            <!--<td>
                                TicketID
                            </td>-->
                            <td>
                                TowerID
                            </td>
                            <td>
                                TowerStreet
                            </td>
                            <td>
                                ModuleID
                            </td>
                            <td>
                                ErrorCode
                            </td>
                            <td>
                                ErrorDetails
                            </td>
                            <td>
                                ErrorDateTime
                            </td>
                            <!--<td>
                                AssignedUser_ID
                            </td>-->
                            <!--<td>
                                AssignedDateTime
                            </td>-->
                            <td>
                                Ticket_Status
                            </td>
                            <!--<td>
                                CompletedDateTime
                            </td>-->
                            <td>
                                Latitude
                            </td>
                            <td>
                                Longitude
                            </td>
                            <td>
                                Distance
                            </td>
                        </tr>
                ''' + ticketlisthtml
        return redirect(url_for("tickets"))
    return redirect(url_for("login"))
        
@app.route('/tickets/modifyticket')
def modifyticket():
    if ("authenticationtoken" in session) and session["authenticationtoken"]:   
        ticketid = request.args.get("ticketid")
        date = request.args.get("date")
        dropdown_status = '''
        <select id="status_{0}">
        <option value="0">Just Assigned</option>
        <option value="10" selected>Work In Progress</option>
        <option value="20">Pending Information</option>
        <option value="100">Completed</option>
        </select>

        <input type="text" id="comment" name="comment"><br><br>

        <button onclick = "
        var new_status_val=document.getElementById('status_{0}').value;
        var comment = document.getElementById('comment').value;
        window.open('/tickets/modifyticket/addcomment/alterdata?ticketid={0}&ticket_status='+new_status_val+'&comment='+comment+'&date={1}');">Submit</button>  
        '''.format(ticketid, date)
        logout_link = "<b><a href = '/logout'>click here to log out</a></b>"
        worklist_link = "<b><a href = '/tickets/worklist'>Your Tickets</a></b>"
        ticketlist_link = "<b><a href = '/tickets'>All Tickets</a></b>"
        
        table = '''
        Ticket ID = {0}
        <table border="1" align="center">
            <tr>
                <td>
                Ticket Comments
                </td>
                <td>
                Date
                </td>
                <td>
                Status
                </td>
            </tr>
        '''.format(ticketid)
        conn = None
        Local_Content = ""
        try:
            conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
            cur = conn.cursor()

            #Statement Execution
            print('PostgreSQL vers:')
            cur.execute("SELECT * FROM ctt_ticket_details WHERE \"ticket_id\" = \'"+ticketid+"\'")

            Local_Content = cur.fetchall()
            for row in Local_Content:
                table = table + '''
                <tr>
                    <td>
                    {0}
                    </td>
                    <td>
                    {1}
                    </td>
                    <td>
                    {2}
                    </td>
                </tr>
                '''.format(row[1], row[2], row[3])

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        #TODO add comment button with date autofill
        return "navbar" + "<br" + worklist_link + "\n" + ticketlist_link + "\n" + logout_link + "<br>" + table + "<br>" + dropdown_status
    return redirect(url_for("login"))

@app.route("/tickets/modifyticket/addcomment/alterdata")
def alterdata():
    if ("authenticationtoken" in session) and session["authenticationtoken"]:
        ticketid = request.args.get("ticketid")
        date = request.args.get("date")
        ticket_status = request.args.get("ticket_status")
        comment = request.args.get("comment")

        conn = None
        insert_query = '''
        INSERT INTO public.ctt_ticket_details(
        "ticket_id", "comments", "date", "ticket_status")
        VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\');
        '''.format(ticketid, comment, date, ticket_status)
        update_query = '''
        UPDATE public.ctt_tickets
        SET \"Ticket_Status\" = \'{1}\'
        WHERE \"ticket_id\"=\'{0}\';
        '''.format(ticketid, ticket_status)
        try:
            conn = psycopg2.connect( host="localhost", database="ctt", user="postgres", password="cynthus2003")
            cur = conn.cursor()

            #Statement Execution
            print('PostgreSQL vers:')
            print(insert_query)
            print(update_query)
            cur.execute(insert_query)
            cur.execute(update_query)
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        return redirect(url_for("worklist"))
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug = True)