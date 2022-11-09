from flask import Flask,render_template,redirect,request,url_for
from flask_mysqldb import MySQL

app=Flask(__name__,template_folder="template")
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="crud"
app.config['MYSQL_CURSORCLASS']="DictCursor"
mysql=MySQL(app)

@app.route("/",methods=['POST','GET'])
def home():
    if request.method=="POST":
        list=request.form["list"]
        con=mysql.connection.cursor()
        sql="insert into todo (list) value(%s)"
        con.execute(sql,[list])
        con.connection.commit()
        con.close()
        return redirect(url_for("home"))
    con=mysql.connection.cursor()
    sql="select * from todo"
    con.execute(sql)
    res=con.fetchall()
    return render_template("homepage.html",value=res)    
    # return render_template("homepage.html")

@app.route("/delete/<string:id>")
def delete(id):
    con=mysql.connection.cursor()
    sql="delete from todo where id=%s"
    con.execute(sql,[id])
    con.connection.commit()
    con.close()
    return redirect(url_for("home"))
@app.route("/update/<string:id>")
def update(id):
    if request.method=='POST':
        list=request.form["list"]
        con=mysql.connection.cursor()
        sql="update todo set list=%s"
        con.execute(sql,[list])
        con.connection.commit()
        con.close()
        return redirect(url_for("home"))
    con=mysql.connection.cursor()
    sql="select * from todo where id=%s"
    con.execute(sql,[id])
    result=con.fetchone()

    con=mysql.connection.cursor()
    sql="select * from todo"
    con.execute(sql)
    res=con.fetchall()
    return render_template("update.html",val1=result,value=res)   


if __name__=="__main__":
    app.run(debug=True)