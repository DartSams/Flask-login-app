from flask import Flask,render_template,request,redirect

app=Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello World!</h1> <a href='/login'>Login</a> <br> <a href='/profile'>Profile</a>"


@app.route('/login' ,methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        # print(username,password)
        print(request.form)
        # return redirect(f'/profile/{username}')

        if username and password == "":
            print('wrong bitch')

        elif username and password != "":
            return redirect(f'/profile/{username}')

    if request.method=="GET":
        username=""
        password=""
        return render_template('login.html')
        # return redirect('/profile')

@app.route('/profile/<name>')
def profile(name):
    return render_template('profile.html',name=name)

if __name__ == '__main__':
    app.run(debug=True)