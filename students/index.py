from flask import Flask,render_template,redirect,request,url_for
from flask_mysqldb import MySQL

app=Flask(__name__,template_folder="template1")
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/",methods=['POST','GET'])
def home():
    if request.method=='POST':
        name=request.form["name"]
        rollno=request.form["rollno"]
        schoolname=request.form["schoolname"]
        departmentname=request.form["departmentname"]
        phoneno=request.form["phoneno"]
        con=mysql.connection.cursor()
        sql="insert into students(name,rollno,schoolname,departmentname,phoneno) value   (%s,%s,%s,%s,%s)"
        con.execute(sql,[name,rollno,schoolname,departmentname,phoneno])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template("homepage.html")
@app.route("/showtable",methods=['POST','GET'])
def showtable():
    con=mysql.connection.cursor()
    sql="select * from students"
    con.execute(sql)
    res=con.fetchall()
    return render_template("table.html",value=res)

@app.route("/delete/<string:id>")
def delete(id):
    con=mysql.connection.cursor()
    sql="delete from students where id=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for('showtable'))
@app.route("/edit/<string:id>",methods=['POST','GET'])
def edit(id):
    if request.method=='POST':
        name=request.form["name"]
        rollno=request.form["rollno"]
        schoolname=request.form["schoolname"]
        departmentname=request.form["departmentname"]
        phoneno=request.form["phoneno"]
        con=mysql.connection.cursor()
        sql="update students set name=%s,rollno=%s,schoolname=%s,departmentname=%s,phoneno=%s where id=%s "
        con.execute(sql,[name,rollno,schoolname,departmentname,phoneno,id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for('showtable'))
    con=mysql.connection.cursor()
    sql="select * from students where id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template('edit.html',value=res)
       



if __name__=="__main__":
    app.run(debug=True)