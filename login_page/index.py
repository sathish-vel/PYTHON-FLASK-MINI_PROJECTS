from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_mysqldb import MySQL

app=Flask(__name__,template_folder="template")

app.secret_key = 'your secret key'

app.config["MYSQL_HOST"]='localhost'
app.config["MYSQL_USER"]='root'
app.config["MYSQL_PASSWORD"]=''
app.config["MYSQL_DB"]='crud'
app.config["MYSQL_CURSORCLASS"]='DictCursor'
mysql=MySQL(app)



@app.route("/login",methods=['POST','GET'])
def login():
    return render_template("loginpage.html")
@app.route("/home")
@app.route("/",methods=['POST','GET'])    
def home():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form: 
        username=request.form["username"]
        password=request.form["password"]
        email=request.form["email"]
        con=mysql.connection.cursor()
        con.execute("select * from login where username =%s and password =%s",(username,password))
        details=con.fetchone()
        if details:
            session['loggedin']=True
            session['id']=details['id']
            session['username']=details['username']
            return render_template("logout.html")
        else:
            msg="incorrect Username or Password"   
            return render_template("loginpage.html",msg=msg)

    return render_template("navbar.html")


@app.route("/loggedout",methods=['POST','GET'])
def loggedout():
   session.pop('loggedin', None)   
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('home'))



@app.route('/signup',methods=['POST','GET'])
def signup():
    msg=''
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        email=request.form["email"]
        con=mysql.connection.cursor()
        con.execute("INSERT INTO LOGIN (username,password,email) value(%s,%s,%s)",(username,password,email))
        con.connection.commit()
        con.close()
        msg="successfully signed up..."
        return render_template("signup.html",msg=msg)    
    return render_template("signup.html")    
if __name__=="__main__":
    app.run(debug=True)
