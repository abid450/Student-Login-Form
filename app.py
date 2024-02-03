from flask import Flask,render_template,request,session,redirect
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.studymart

app = Flask(__name__)
app.secret_key = "dwhdiu2h2903e"

# Register form ----------------------------------------------

@app.route("/register", methods=['POST','GET'])
def register():
    msg = None
    if request.method=='GET':
        if 'username' in session.keys():
            return redirect('/user')
        return render_template('register.html',**locals())
    elif request.method=='POST':
        record = request.form
        found = db.users.find_one({'username': record['username']})
        if found is not None:
            msg = "Duplicate Username Exists"
            return render_template('register.html',**locals())
        db.users.insert_one(dict(record))
        for item in db.users.find():
            print(item)
        return redirect('/login')

# Login form ----------------------------------------------
@app.route("/login", methods=['POST','GET'])
def login():
    msg = None
    if request.method=='GET':
        if 'username' in session.keys():
            return redirect('/user')
        return render_template('login.html',**locals())
    else:
        record = request.form
        found = db.users.find_one({'username': record['username']})
        if found is None:
            msg = "Username does not exist"
            return render_template('login.html',**locals())
        if found['password']!= record['password']:
            msg = "Password did not match"
            return render_template('login.html',**locals())
        session['username'] = record['username']
        return redirect('/user')


@app.route("/user")
def user():
    if 'username' not in session.keys():
        return redirect('/login')
    return render_template('user.html',**locals())


@app.route("/logout")
def logout():
    if 'username' in session.keys():
        session.pop('username')
    return redirect('/login')





if __name__ == "__main__":
    app.run(debug=True)