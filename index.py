from flask import Flask, request,session, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"]="aaryansr"

#CREATE TABLE posts (post_id int IDENTITY(1,1) PRIMARY KEY,post_headline varchar(255) NOT NULL,post_content TEXT;)

conn=sqlite3.connect("database.db")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS posts (post_id int IDENTITY(1,1) PRIMARY KEY,post_headline varchar(255) NOT NULL,post_content TEXT, password varchar(255))")
conn.commit()

conn=sqlite3.connect("database.db")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS passwords (password varchar(255))")
conn.commit()


@app.route('/')
def home():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    results=cur.execute("select post_headline, post_content, ROWID from posts")
    return render_template("home.html",results=list(results))


@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin-login", methods=['POST'])
def admin_login():
    password=request.form['password']
    if str(password)=="root":
        session['login'] = True
        login=session['login']
        return redirect(url_for("admin_dashboard", login=login))
    else:
        error=True
        return render_template("admin.html", error=error)

@app.route('/admin-dashboard/<login>', methods=['GET','POST'])
def admin_dashboard(login):
    if login:
         conn=sqlite3.connect("database.db")
         cur=conn.cursor()
         results=cur.execute("select post_headline, post_content, ROWID from posts")
         return render_template("admin-dashboard.html",results=results)
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    session.pop("login")
    return redirect(url_for("admin"))


@app.route("/newpost", methods=['POST'])
def newpost():
    login=session['login']
    ph=request.form["post_headline"]
    pc=request.form["post_content"]

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("insert into posts(post_headline,post_content) values(?,?)",(ph,pc))
    conn.commit()
    cur.close()
    flag=True
    return redirect(url_for("admin_dashboard",login=login))

@app.route("/deletepost/<int:id>")
def deletepost(id):
    login=session['login']
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("delete from posts where ROWID=?",(id,))
    conn.commit()
    cur.close()
    return redirect(url_for("admin_dashboard",login=login))


if __name__ == '__main__':
    app.run(debug=True)