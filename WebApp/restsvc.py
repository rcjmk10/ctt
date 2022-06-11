from flask import Flask, render_template, request, redirect, \
url_for, flash, make_response, session, jsonify
from flask import render_template
import json
import psycopg2

app = Flask(__name__)
app.secret_key = "any random string"

@app.route("/")
def index():
    if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"

@app.route('/product/<name>')
def get_product(name):
  return "The product is " + str(name)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/json')
def jsonIndex():
    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})

@app.route('/sql')
def postgresql():
    conn = None
    local_content=""
    try:
        conn = psycopg2.connect( host="localhost",database="ctt",   user="postgres",   password="cynthus2003")
        cur = conn.cursor()
            
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT * from ctt_users')

        # display the PostgreSQL database server version
        local_users = cur.fetchall()
        for localuser in local_users:
            local_content=local_content+", "+str(localuser[0])+", "+str(localuser[1])+", "+str(localuser[2])
            print("Id = ", localuser[0], )
            print("Model = ", localuser[1])
            print("Price  = ", localuser[2], "\n")
            
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return  "The product is " + str(local_content)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      return 'file uploaded successfully'

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('index'))
   return '''
	
   <form action = "/login" method = "post">
      <p><input type = "text" name = "username"/></p>
      <p><input type = submit value = "Login"/></p>
   </form>	
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug = True)