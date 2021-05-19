# Flask-login-app

> A clean & beautiful CRUD REST Login & Registration App!


### Website Preview
<p> 
    <img src="assets/preview.PNG">
</p>


## Features 
> Valid HTML5, CSS3 & Python code\
> Easy to modify\
> Uses Flask Server


## Sections 
✔️ Home \
✔️ Shop \
✔️ About Us \
✔️ Contact \
✔️ login \
✔️ Register \
✔️ Profile 


## Tools Used 
* [<b>Flask Bcrypt</b>](https://flask-bcrypt.readthedocs.io/en/latest/) - To encrypt passwords.
* [<b>Flask</b>](https://flask-doc.readthedocs.io/en/latest/) - To host the server.
* [<b>Flask-mysql-connector</b>](https://pypi.org/project/flask-mysql-connector/) - To save user data to a database.
* [<b>Flask-session</b>](https://pythonbasics.org/flask-sessions/) - To get the current user logged in.


## Learned subjects
-  How to join mysql tables
-  Encrypt/Hash passwords
-  Flask session


## Installation & Deployment 
-	Clone the repository
-	To connect your own  MYSQL database first create two tables called Flask_Login and Flask_Profile_Info.The Flask_Login table if for storing user login data such as name,password,email & privilege.The Flask_Profile_Info table stores user personal data such as author,gender,age,job & location both tables need these columnes.
-   Now create a `.env` file in the same directory as the main.py file this is to hold the enviroment variable for your MYSQL password inside it write `password=<your-mysql-password>` after this 
-	 
