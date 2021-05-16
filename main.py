from flask import Flask,render_template,request,redirect,session
from flask_bcrypt import Bcrypt #encrypt passwords 
from flaskext.mysql import MySQL #allows flask and mysql connection
from dotenv import load_dotenv #to get env variables for db connection
import os
load_dotenv()


app=Flask(__name__) #this initializes the flask app (required)
bcrypt=Bcrypt(app) ##to encrypt passwd https://flask-bcrypt.readthedocs.io/en/latest/
mysql=MySQL() #to connect flask to mysql


app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=os.getenv('password')
app.config['MYSQL_DATABASE_DB']='testdatabase'
mysql.init_app(app)

conn=mysql.connect()
mycursor=conn.cursor()
##Table-Flask_Login
##good example of REST request https://towardsdatascience.com/launch-your-own-rest-api-using-flask-python-in-7-minutes-c4373eb34239


app.config['SECRET_KEY'] = 'hello' #use session to save personal data to so user doesnt have to log in over and over
login_state=False


@app.route('/',methods=["GET","POST"])
def home():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']


        if username and password != "":
            mycursor.execute(f"SELECT * FROM Flask_Login WHERE name = '{username}'")
            result=mycursor.fetchall()

            for i in result:
                # print(i[1])
                passwd_check=bcrypt.check_password_hash(i[1], password)
                print(passwd_check)

            if passwd_check == True:
                session["username"]=username
                return redirect(f'/profile')     
            
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
        
        print("\nUser db:")
        mycursor.execute(f"SELECT * FROM Flask_Login")
        for i in mycursor:
            print(i)

        print("\nUser attr db:")
        mycursor.execute('SELECT * FROM Flask_Profile_Info')
        for i in mycursor:
            print(i)

        print(f"Current session: {session}")
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
            return redirect(f'/profile')
        
        else:
            # print(password,compare_password)
            return redirect('/register')
        # login_state=True
        # return redirect(f'/profile/{username}')


@app.route('/profile' ,methods=["GET","POST","PUT","DELETE"])
def profile():
    user_attr=[]
    if request.method=="GET":
            if "username" in session:
                username=session['username']
                mycursor.execute('SELECT * FROM Flask_Profile_Info')
                try:
                    for num,x in enumerate(mycursor):
                        for i in x:
                            # print(i)
                            user_attr.append(i)
                    
                    user_attr.pop(0)
                    print(f"filtered list: {user_attr}")

                except:
                    print("fuck this time to go to sleep... not connected to the 2nd db do that later....")
                
                return render_template('profile.html',username=username,user_attr=user_attr)

            else:
                return redirect("/")

    elif request.method=="POST":
        return redirect(f'/profile')


@app.route('/logout')
def logout():
    session.pop("username")
    return redirect("/")


@app.route("/delete")
def delete():
    username=session["username"]
    mycursor.execute(f"DELETE FROM Flask_Login WHERE name=%s",(username))
    mycursor.execute(f"DELETE FROM Flask_Profile_Info WHERE author=%s",(username))
    conn.commit()
    session.pop("username")
    return redirect("/")


@app.route("/profile/settings",methods=["GET","POST","PUT","DELETE"])
def setting():
    if request.method=="GET":
        if "username" in session:
            return render_template("settings.html")
        
        elif "username" not in session:
            return redirect("/")

    elif request.method=="POST":
        # print(request.values)
        username=session['username']
        gender=request.form['gender']
        age=request.form['age']
        job_role=request.form['job-role']
        location=request.form['location']

        mycursor.execute(f"UPDATE Flask_Profile_Info SET gender = %s, age = %s,  job = %s,  location = %s WHERE author = %s", (gender,age,job_role,location,username))
        conn.commit()

        return redirect("/profile")


if __name__ == '__main__':
    app.run(debug=True)