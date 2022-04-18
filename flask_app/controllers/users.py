from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if "first_name" in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/reg_login', methods=["POST"])
def reg_login():
    #if user is registering
    if (request.form["which_form"] == "register"):
        #validate data
        if not User.validate_registration(request.form):
            return redirect('/')

        #hash password:
        pw_hash = bcrypt.generate_password_hash(request.form["password"])

        #gather data for User.save
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
        }

        #send data to User.save:
        id = User.save(data)
        session["id"] = id
        session["first_name"] = request.form["first_name"]

        return redirect('/dashboard')

    #if user is logging in
    if (request.form["which_form"] == "login"):

        data = {
            "email":request.form['email']
        }

        if not User.get_user_by_email(data):
            flash("Invalid email/password.", "login_error")
            return redirect('/')
        
        user = User.get_user_by_email(data)

        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash("Invalid email/password.", "login_error")
            return redirect('/')

        session["id"] = user.id
        session["first_name"] = user.first_name

        return redirect('/dashboard')


    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if "id" not in session:
        return redirect('/')

    data = {"id":session["id"]}
    user = User.get_user_by_id(data)
    recipes = Recipe.get_all()
    print(recipes[0])
    return render_template('dashboard.html', user = user, recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
