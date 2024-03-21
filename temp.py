
from flask import Flask,render_template,request
import sqlite3 as sql
from flask_limiter import Limiter

app = Flask(__name__)
limiter=Limiter(app)

@app.route('/')
def homepage():
   return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/searchrec')
def searchrec():
   return render_template('searchrec.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        
        if username == request.form.get('username') and password == request.form.get('password'):
           return render_template('home.html')
        else:
            return render_template('login.html',message='Bad Credentials')



@app.route('/addrec',methods = ['POST', 'GET'])
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
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
  
      con = sql.connect("database.db")
      con.row_factory = sql.Row
   
      cur = con.cursor()
      cur.execute("select * from students")
   
      rows = cur.fetchall();
      con.close()
      return render_template("list.html",rows = rows)
 
      

@app.route('/search',methods = ['POST', 'GET'])
def search():
 
      pincode = request.form['pin']
      con = sql.connect("database.db")
      con.row_factory = sql.Row
   
      cur = con.cursor()
      cur.execute(f"select * from students where pin={pincode}")
   
      rows = cur.fetchall();
      if len(rows)>0:
         con.close()
         return render_template("search.html",rows = rows)
      else:
          msg = "No data found"
          con.close()
          return render_template("result.html",msg = msg)
         
       


@app.route('/logout')
def logout():
   return render_template('login.html')

