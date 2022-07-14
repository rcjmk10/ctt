from collections import UserDict, UserList
import json
from operator import methodcaller
from threading import local
from turtle import update
from flask import Flask, render_template, request, redirect, \
url_for, flash, make_response, session, jsonify
from flask import render_template
import psycopg2

app = Flask(__name__)
app.secret_key = "any random string"

Userlat = 0
Userlong = 0
logout_link = "<b><a href = '/logout'>click here to log out</a></b>"

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
            <td>
                {0}
            </td>
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



@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      session['email'] = request.form['email']
      session['password'] = request.form['password']
      session['authenticationtoken'] = False
      if authenticate(session['email'], session['password']):
        session['authenticationtoken'] = True
        return redirect(url_for('tickets'))
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
        return True
    else:
        print("Invalid Login, Authentication Failed")
        return False

@app.route('/')
def home():
    return "Not Logged in,\n" + "<b><a href = '/login'>click here to log in</a></b>"

@app.route('/tickets', methods = ['POST', 'GET'])
def tickets():
    logout_link = "<b><a href = '/logout'>click here to log out</a></b>" + "\n"
    worklist_link = "<b><a href = '/tickets/worklist'>Your Tickets</a></b>"
    if session['authenticationtoken']:
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
                print(local_content[0])
            ticketlisthtml = ""
            for row in local_content:
                ticketlisthtml = ticketlisthtml + ticketlisttemplate.format(row[0], row[1], row[2], row[3], \
                row[4], row[5], row[6], row[7], row[8], row[9], row[-4], row[-3], row[-2])
            return "Ticket List\n" + worklist_link + "\n" + '''
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
                        <td>
                            TicketID
                        </td>
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
                            CompletedDateTime
                        </td>
                        <td>
                            Longitude
                        </td>
                        <td>
                            Latitude
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

@app.route('/tickets/addnewticket', methods = ['POST'])
def process_json():

    conn = None

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        template = 'INSERT INTO ctt_tickets(\nticket_id, \"TowerID\",\
\"TowerStreet\", \"ModuleID\", \"ErrorCode\", \"ErrorDetails\", \"ErrorDateTime\",\
\"AssignedUser_ID\", \"AssignedDateTime\", \"Ticket_Status\", \"CompletedDateTime\",\
\"Longitude\", \"Latitude\", geom)\nVALUES (gen_random_uuid(),\
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
    
    if session['authenticationtoken']:
        conn = None
        local_content=""
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
                ticketlisthtml = ticketlisthtml + ticketlisttemplate.format(row[0], row[1], row[2], row[3], \
                row[4], row[5], row[6], row[7], row[8], row[9], row[-4], row[-3], row[-2])
            return "Assigned Tickets\n" + logout_link + "\n" + "<b><a href = '/tickets'>Ticket List</a></b>" + "\n"\
            + '''
            <html>
                <table border="1" align="center">
                    <tr>
                        <td>
                            TicketID
                        </td>
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
                            CompletedDateTime
                        </td>
                        <td>
                            Longitude
                        </td>
                        <td>
                            Latitude
                        </td>
                    </tr>
            ''' + ticketlisthtml
    return redirect(url_for("login"))


@app.route('/tickets/addtoworklist', methods = ['POST', 'GET'])
def add_to_worklist():
    update_query = "UPDATE public.ctt_tickets\nSET \"AssignedUser_ID\" = \'{0}\'\nWHERE \"ticket_id\" = \'{1}\';".format(session["uuid"], request.args.get("ticketid"))
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

@app.route('/getnewticket')
def getnewticket():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    selectquery = '''
    SELECT *, ST_Distance('POINT({0} {1})', concat('POINT(', "Longitude", ' ', "Latitude", ')')) AS l_distance FROM ctt_tickets\
    ORDER BY ST_Distance('POINT({0} {1})', concat('POINT(', "Longitude", ' ', "Latitude", ')')) ASC\
    limit 10
    '''.format(latitude, longitude)
    print(selectquery)
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
            for row in local_content:
                ticketlisthtml = ticketlisthtml + ticketlisttemplate.format(row[0], row[1], row[2], row[3], \
                row[4], row[5], row[6], row[7], row[8], row[9], row[-5], row[-4], row[-3])
            return "Assigned Tickets\n" + logout_link + '''
            <html>
                <table border="1" align="center">
                    <tr>
                        <td>
                            TicketID
                        </td>
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
                            CompletedDateTime
                        </td>
                        <td>
                            Longitude
                        </td>
                        <td>
                            Latitude
                        </td>
                    </tr>
            ''' + ticketlisthtml
    return redirect(url_for("tickets"))

    return request.args.get("latitude") + "\n" + request.args.get("longitude")
        


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug = True)