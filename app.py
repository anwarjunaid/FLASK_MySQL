from flask import Flask, render_template, request, redirect, jsonify, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

# MySQL configurations
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://junaidali:Rockstar%4023@localhost/pydb"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

db = SQLAlchemy(app)                   

class Task(db.Model):
    __tablename__ = 'tasks'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
class Users(db.Model):
    __tablename__ = 'usertable'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f"(name='{self.name}', email='{self.email}', password='{self.password}')"


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            todo = Task(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Task.query.all()
    # return jsonify({
    #     "sno": allTodo.sno,
    #     "title": allTodo.title,
    #     "desc": allTodo.desc
    # })
    return render_template("index.html", allTodo = allTodo)




# Deletion
@app.route('/delete/<int:sno>', methods=['DELETE'])
def delete(sno):
    todo = Task.query.get(sno)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    print("data deleted")
    return jsonify({"message": "Todo deleted successfully"})




# Updation
@app.route('/update/<int:sno>', methods=['GET', 'PUT'])
def update(sno):
    if request.method == 'PUT':
        todo = Task.query.get(sno)
        print(todo)
        data = request.get_json()   # Parse JSON data from the request
        print(data)
        if 'title' in data:
            todo.title = data['title']
        if 'desc' in data:
            todo.desc = data['desc']
        db.session.commit()
        return jsonify({"success": True})
    
    todo = Task.query.get(sno)
    return render_template('update.html', todo = todo)


# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name and email and password:
            data = Users(name=name, email=email, password=password)
            print(data)
            db.session.add(data)
            db.session.commit()
            return redirect('/regsuccess')
    return render_template("signup.html")


# registration successfull
@app.route('/regsuccess')
def regsuccess():
    return render_template("regsuccess.html")

# singin route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = Users.query.all()
        for users in data:
            if users.email == email and users.password == password:
                session['email'] = email
                return render_template("profile.html", users = users )
            
        return render_template('signin.html', error='Invalid user')
    return render_template('signin.html')


# profile of a particular user
@app.route('/profile')
def profile():
    data = Users.query.all()
    email = session['email']
    for users in data:
        if users.email == email:
            return render_template("profile.html", users=users)
        

# logout route
@app.route('/logout')
def logout():
    print(session['email'])
    # Removed the email from the session if it exists
    session.pop('email', None)
    flash('You were successfully logged out')
    return redirect('/')
    

# change password route
@app.route('/changepwd/<int:sno>', methods=['GET', 'POST', 'PUT'])
def changePassword(sno):
    if request.method == 'PUT':
        data = request.get_json()
        print(data)
        person = Users.query.get(sno)
        person.password = data['newpwd']
        db.session.commit()
        return jsonify({"success": True})
    
    return render_template("profile.html")
    
if __name__ == '__main__':
    app.run(debug=True, port=3000)
