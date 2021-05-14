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
app.config['MYSQL_DATABASE_PASSWORD']='Dartagnan18@'
app.config['MYSQL_DATABASE_DB']='testdatabase'
mysql.init_app(app)

conn=mysql.connect()
mycursor=conn.cursor()
##Table-Flask_Login
##good example of REST request https://towardsdatascience.com/launch-your-own-rest-api-using-flask-python-in-7-minutes-c4373eb34239

login_state=False

@app.route('/',methods=["GET","POST"])
def home():
    global login_state,username,password
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']


        if username and password != "":
            mycursor.execute(f"SELECT * FROM Flask_Login WHERE name = '{username}'")
            result=mycursor.fetchall()

            for i in result:
                print(i[1])
                passwd_check=bcrypt.check_password_hash(i[1], password)
                print(passwd_check)

            if passwd_check == True:
                login_state=True
                return redirect(f'/profile/{username}')     
            
            elif passwd_check == False:
                return redirect('/')

        elif username and password == "" or password == "":
            print('You must fill in the username and password fields')
            return redirect('/')


        # print(username,password)
        # print(f"\ndictionary of username + password: {request.form}")
        # print(f"hashed password: {hash_passwd}\n")


        # ##check if database passwd and entered password are the same
        # example = 'secret'
        # passwd_check=bcrypt.check_password_hash(hash_passwd, example)
        # print(passwd_check)


    elif request.method=="GET":
        username=""
        password=""
        mycursor.execute(f"SELECT * FROM Flask_Login")
        for i in mycursor:
            print(i)
        return render_template('login.html')



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
        # terms=request.form['terms-of-service']
        # print(request.form)
        # print(f'account info:')
        # print(username,email,password,co+mpare_password)
            
        hash_passwd = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(hash_passwd)

        if password==compare_password and 'terms-of-service' in request.form:
            login_state=True
            mycursor.execute("INSERT INTO Flask_Login (name,password,email,privilege) VALUES (%s,%s,%s,%s)", (username,hash_passwd,email,'user'))
            conn.commit()
            return redirect(f'/profile/{username}')
        
        else:
            # print(password,compare_password)
            return redirect('/register')
        # login_state=True
        # return redirect(f'/profile/{username}')


@app.route("/login",methods=["GET", "POST"])
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
                print(i[2])
                passwd_check=bcrypt.check_password_hash(i[2], password)
                print(passwd_check)

            if passwd_check == True:
                login_state=True
                return redirect(f'/profile/{username}')     
            
            elif passwd_check == False:
                return redirect('/')

        elif username and password == "" or password == "":
            print('You must fill in the username and password fields')
            return redirect('/')


        # print(username,password)
        # print(f"\ndictionary of username + password: {request.form}")
        # print(f"hashed password: {hash_passwd}\n")


        # ##check if database passwd and entered password are the same
        # example = 'secret'
        # passwd_check=bcrypt.check_password_hash(hash_passwd, example)
        # print(passwd_check)


    elif request.method=="GET":
        username=""
        password=""
        mycursor.execute(f"SELECT * FROM Flask_Login")
        for i in mycursor:
            print(i)
        return render_template('login.html')



@app.route('/profile/<name>')
def profile(name):
    global login_state

    # print(login_state)
    if login_state==False:
        return redirect('/')

    else:
        login_state=False
        # print(password)
        return render_template('profile.html',name=name)

if __name__ == '__main__':
    app.run(debug=True)