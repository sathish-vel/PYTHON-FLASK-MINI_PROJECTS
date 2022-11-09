from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_mysqldb import MySQL
app=Flask(__name__,template_folder="template")

app.secret_key = 'your secret key'


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='crud'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)


@app.route('/',methods=['POST','GET'])
def home():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form :
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']

        con=mysql.connection.cursor()
        con.execute('select * from login where username = %s and email = %s ',(username,email))
        result=con.fetchone()

       

        if result:
            session['id']=result['id']
            session['username']=result['username']
            return redirect(url_for("table"))
        else:
            msg="invalid username or password.. plz Register now "
            return render_template('login.html',msg=msg)  
    return render_template("login.html")
@app.route('/table',methods=['POST','GET'])
def table():
    cursor=mysql.connection.cursor()
    cursor.execute('select * from login')
    value=cursor.fetchall()
    return render_template("table.html",value=value)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST' and 'uname' in request.form and 'e' in request.form and 'pword' in request.form :
        username=request.form['uname']
        password=request.form['pword']
        email=request.form['e']

        # con=mysql.connection.cursor()
        # con.execute('INSERT INTO LOGIN (username,password,email) values(%s,%s,%s)',(username,password,email))
        # con.connection.commit()
        # con.close()
        # return redirect(url_for('home'))
        return redirect(url_for("home"))

    return render_template("register.html")

if __name__=='__main__':
    app.run(debug=True)