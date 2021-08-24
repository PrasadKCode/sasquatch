from sasquatch_app.models.sasquatch import Sasquatch
from sasquatch_app import app
from flask import render_template,request,redirect,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from sasquatch_app.models.user import User



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/create',methods = ['post'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.save(data)
    
    session['logged_user'] = user_id
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']

    return redirect('/dashboard')


@app.route('/user/login',methods = ['post'])
def login_user():
    data = {
        'email' : request.form['email']
    }

    retrieved_user = User.get_by_email(data)

    if not retrieved_user:
        flash("Invalid email/password","login_error")
        return redirect('/')
    
    if not bcrypt.check_password_hash(retrieved_user.password,request.form['password']):
        flash("Invalid email/password","login_error")
        return redirect('/')
    
    session['logged_user'] = retrieved_user.id
    session['first_name'] = retrieved_user.first_name
    session['last_name'] = retrieved_user.last_name

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():

    if 'logged_user' not in session:
        return redirect('/')
        
    sightings = Sasquatch.get_all()
    return render_template('dashboard.html',first_name=session['first_name'],last_name = session['last_name'],sightings = sightings,user_id = session['logged_user'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')