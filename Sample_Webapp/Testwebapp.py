from collections import UserDict, UserList
from operator import methodcaller
from flask import Flask, render_template, request, redirect, \
url_for, flash, make_response, session, jsonify
from flask import render_template
import psycopg2

app = Flask(__name__)
app.secret_key = "any random string"

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      session['email'] = request.form['email']
      session['password'] = request.form['password']
      if authenticate(session['email'], session['password']):
        return redirect(url_for('tickets'))
   return """dex
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
    return "Ticket List\n" + "<b><a href = '/logout'>click here to log out</a></b>"

@app.route('/logout')
def logout():
   # remove the email and password from the session if it is there
   session.pop('email', None)
   session.pop('password', None)
   return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug = True)