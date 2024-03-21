from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp
import sqlite3

class MyForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=3 , max=10, message="Password must be between 3-10 characters long"),]
            ,render_kw={"placeholder": "Username"} )

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8,max=20, message="Password must be between 8-20 characters long"),
        Regexp(
    '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:"<>?`~,-./;\'[\]\\=]).+$',
    message="Password must include at least one lowercase letter, one uppercase letter, one digit, and one      special character."
),
    ], render_kw={"placeholder": "Password"})  
    submit = SubmitField('Submit')

def create_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    cur = conn.cursor()
    conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
    print("Table created successfully")
    students_data = [
        ("Akash", "Varanasi", "Varansi", "231304"),
        ("JashRaj", "Nanded", "Nanded", "440021"),
        ("Abhay", "Kanpur", "Kanpur", "440027"),
    ]
    
    conn.executemany('INSERT INTO students (name, addr, city, pin) VALUES (?, ?, ?, ?)', students_data)
    conn.commit()
    # cur.execute('SELECT * from students')
    # rows = cur.fetchall()
    # for r in rows:
    #     print(r)
    conn.close()

    