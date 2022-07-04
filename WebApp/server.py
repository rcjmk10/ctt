from collections import UserDict, UserList
import json
from operator import methodcaller
from flask import Flask, render_template, request, redirect, \
url_for, flash, make_response, session, jsonify
from flask import render_template
import psycopg2

app = Flask(__name__)
app.secret_key = "any random string"

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
        local_users = cur.fetchall()
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
    if len(local_users) == 1:
        print(UserList)
        return True
    else:
        print(UserList)
        return False

@app.route('/')
def home():
    return "Not Logged in,\n" + "<b><a href = '/login'>click here to log in</a></b>"

@app.route('/tickets')
def tickets():
    if session['authenticationtoken']:
        return "Ticket List\n" + "<b><a href = '/logout'>click here to log out</a></b>"
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
        template = 'INSERT INTO public.ctt_tickets(\nticket_id, \"TowerID\",\
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

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
            return "completed"
    else:
        return 'Content-Type not supported!'



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug = True)