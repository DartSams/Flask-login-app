from flask import Flask,render_template,request,redirect
# from flask.ext.bcrypt import Bcrypt
from flask_bcrypt import Bcrypt


##to encrypt passwd https://flask-bcrypt.readthedocs.io/en/latest/
app=Flask(__name__)
bcrypt=Bcrypt(app)
login_state=False

@app.route('/')
def home():
    return "<h1>Hello World!</h1> <a href='/login'>Login</a> <br> <a href='/profile'>Profile</a>"


@app.route('/login' ,methods=["GET","POST"])
def login():
    global login_state
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']

        if username and password != "":
            hash_passwd = bcrypt.generate_password_hash(password).decode('utf-8')
            example = 'a'
            passwd_check=bcrypt.check_password_hash(hash_passwd, example)
            print(passwd_check)
            if passwd_check == True:
                login_state=True
                return redirect(f'/profile/{username}')
            
            elif passwd_check == False:
                return redirect('/login')

        elif username and password == "" or password == "":
            print('You must fill in the username and password fields')
            return redirect('/login')


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
        return render_template('login.html')

@app.route('/profile/<name>')
def profile(name):
    global login_state

    if login_state==False:
        return redirect('/login')

    else:
        login_state=False
        return render_template('profile.html',name=name)


if __name__ == '__main__':
    app.run(debug=True)