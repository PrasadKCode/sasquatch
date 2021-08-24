from sasquatch_app.models.skeptic import Skeptic
from sasquatch_app import app
from flask import render_template,redirect,request,session,flash
from sasquatch_app.models.sasquatch import Sasquatch
app.jinja_env.add_extension('jinja2.ext.do')

@app.route('/new/sighting')
def add_sighting():
    
    return render_template('add_sasquatch.html',first_name = session['first_name'],last_name=session['last_name'])

@app.route('/sasquatch/create',methods = ['post'])
def create_sasquatch():

    if 'logged_user' not in session:
        return redirect('/')

    if not Sasquatch.validate_sasquatch(request.form):
        return redirect('/new/sighting')
    
    data ={
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_of_sighting':request.form['date_of_sighting'],
        'num_of_sasquatches':request.form['num_of_sasquatches'],
        'user_id':session['logged_user']
    }
    new_appointment = Sasquatch.save(data)
    return redirect('/dashboard')


@app.route('/edit/<int:id>')
def edit_sasquatch(id):

    if 'logged_user' not in session:
        return redirect('/')

    data = {
        'id':id
    }
    sasquatch = Sasquatch.get_one(data)
    return render_template('edit_sasquatch.html',sasquatch = sasquatch,first_name = session['first_name'],last_name = session['last_name'])


@app.route('/dashboard/<int:id>/update',methods = ['post'])
def update_sasquatch(id):
    if 'logged_user' not in session:
        return redirect('/')

    if not Sasquatch.validate_sasquatch(request.form):
        return redirect(f'/edit/{id}')
    data ={
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_of_sighting':request.form['date_of_sighting'],
        'num_of_sasquatches':request.form['num_of_sasquatches'],
        'id':id
    }
    Sasquatch.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_sasquatch(id):

    if 'logged_user' not in session:
        return redirect('/')
        
    data = {
        'id':id
    }
    Skeptic.delete_skeptic_all(data)
    Sasquatch.delete(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_sasquatch(id):

    if 'logged_user' not in session:
        return redirect('/')
        
    data = {
        'id':id
    }

    sasquatch = Sasquatch.get_one(data)
    return render_template('show_sasquatch.html',sasquatch = sasquatch,first_name=session['first_name'],last_name = session['last_name'],user_id = session['logged_user'])

