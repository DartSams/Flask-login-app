from flask import Flask,render_template,request,redirect
from flask_bcrypt import Bcrypt #encrypt passwords 
from flaskext.mysql import MySQL #allows flask and mysql connection
from dotenv import load_dotenv #to get env variables for db connection
import os
load_dotenv()


##to encrypt passwd https://flask-bcrypt.readthedocs.io/en/latest/
app=Flask(__name__)
bcrypt=Bcrypt(app)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=os.getenv('password')
app.config['MYSQL_DATABASE_DB']='testdatabase'
mysql.init_app(app)

conn=mysql.connect()
mycursor=conn.cursor()
##Table-Flask_Login

login_state=False

@app.route('/')
def home():
    mycursor.execute(f"SELECT * FROM Flask_Login")
    for i in mycursor:
        print(i)
    return "<h1>Hello World!</h1> <a href='/login'>Login</a> <br> <a href='/register'>Create Account</a>"


@app.route('/login' ,methods=["GET","POST"])
def login():
    global login_state,username,password
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']


        if username and password != "":
            hash_passwd = bcrypt.generate_password_hash(password).decode('utf-8')
            mycursor.execute(f"SELECT * FROM Flask_Login WHERE name = '{username}'")
            result=mycursor.fetchall()

            for i in result:
                passwd_check=bcrypt.check_password_hash(i[2], password)

            if passwd_check == True:
                login_state=True
                return redirect(f'/profile/{username}')     
            
            elif passwd_check == False:
                return redirect('/login')

        elif username and password == "" or password == "":
            #add in html alerts later
            print('You must fill in the username and password fields')
            return redirect('/login')

    elif request.method=="GET":
        username=""
        password=""
        return render_template('login.html')



@app.route('/profile/<name>')
def profile(name):
    global login_state

    if login_state==False:
        return redirect('/login')

    else:
        login_state=False
        return render_template('profile.html',name=name)

@app.route('/register',methods=["GET","POST"])
def register():
    global login_state
    if request.method=='GET':
        return render_template('register.html')

    elif request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        compare_password=request.form['compare-password']

        if password==compare_password:
            login_state=True
            hash_passwd = bcrypt.generate_password_hash(password).decode('utf-8')
            mycursor.execute("INSERT INTO Flask_Login (name,email,password,privilege) VALUES (%s,%s,%s,%s)", (username,email,hash_passwd,'user'))
            conn.commit()
            return redirect(f'/profile/{username}')
        
        else:
            return redirect('/register')


if __name__ == '__main__':
    app.run(debug=False)