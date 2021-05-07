from flask import Flask,render_template,request,redirect
from flask_bcrypt import Bcrypt


##docs to encrypt passwd https://flask-bcrypt.readthedocs.io/en/latest/
app=Flask(__name__)
bcrypt=Bcrypt(app)


@app.route('/')
def home():
    return "<h1>Hello World!</h1> <a href='/login'>Login</a> <br> <a href='/profile'>Profile</a>"


@app.route('/login' ,methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        hash_passwd = bcrypt.generate_password_hash(password).decode('utf-8')

        # print(username,password)
        print(f"\ndictionary of username + password: {request.form}")
        print(f"hashed password: {hash_passwd}\n")


        ##check if database passwd and entered password are the same
        candidate = 'secret'
        passwd_check=bcrypt.check_password_hash(hash_passwd, candidate)
        print(passwd_check)


        if username and password != "":
                if passwd_check==True:
                    return redirect(f'/profile/{username}')


    if request.method=="GET":
        username=""
        password=""
        return render_template('login.html')

@app.route('/profile/<name>')
def profile(name):
    return render_template('profile.html',name=name)

if __name__ == '__main__':
    app.run(debug=True)