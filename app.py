from flask import Flask, render_template, request, url_for, redirect, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import uuid
import os
import sqlite3 as sql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from schema import MyForm, create_db

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "100 per hour"],
)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager(app)
login_manager.login_view = 'index'

#create db if it is not exist
if not os.path.exists('database.db'):
    create_db()


class User(UserMixin):
    def __init__(self, name, password):
        self.id = str(uuid.uuid4())
        self.name = name
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    if 'User' in session and session['User']['id'] == user_id:
        print("User found")
        user_info = session['User']
        return User(user_info['name'], user_info['password'])
    return None
 
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
   return render_template('home.html')

@app.route('/enternew')
@login_required
def new_student():
   return render_template('student.html')

@app.route('/searchrecord')
@login_required
def searchrecord():
   return render_template('searchRecord.html')

@app.route('/addrec',methods = ['POST', 'GET'])
@login_required
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
          
            cur.execute("INSERT INTO students (name,addr,city,pin)VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         con.close()
         return render_template("result.html",msg = msg)

@app.route('/list')
@login_required
def list():
      con = sql.connect("database.db")
      con.row_factory = sql.Row
   
      cur = con.cursor()
      cur.execute("select * from students")
   
      rows = cur.fetchall()
      con.close()
      return render_template("list.html",rows = rows)
 
      

@app.route('/search',methods = ['POST', 'GET'])
@login_required
def search():
    if request.method == 'POST':
        pincode = request.form['pin']
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from students where pin= ? " ,(pincode,))

        rows = cur.fetchall()
        con.close()
        
        if len(rows)>0:
            return render_template("search.html",rows = rows)
        else:
            msg = "No data found"
            return render_template("result.html",msg = msg)
        
@app.route('/logout')
@login_required
def logout():
   logout_user()
   session.pop('User', None)
   return redirect('/')

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("1/second")
def index():
    form = MyForm()

    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        user = User(name, password)

        if user:
            login_user(user)
            session['User'] = {'id': user.id, 'name': user.name, 'password': user.password}
            return redirect('/home')
        
    # print("Form errors:", form.errors)
    return render_template('index.html', form = form)
 
if __name__ == '__main__':
    app.run(debug=True)
 