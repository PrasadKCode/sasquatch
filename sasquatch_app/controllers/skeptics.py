from sasquatch_app import app
from flask import render_template,redirect,request,session,flash
from sasquatch_app.models.skeptic import Skeptic



@app.route('/skeptics/insert/<int:user_id>/<int:sasquatch_id>')
def create_skeptic(user_id,sasquatch_id):
    data = {
        'user_id':user_id,
        'sasquatch_id':sasquatch_id
    }
    new_skeptic_id = Skeptic.create_skeptic(data)
    return redirect(f'/show/{sasquatch_id}')


@app.route('/skeptics/delete/<int:user_id>/<int:sasquatch_id>')
def delete_skeptic(user_id,sasquatch_id):
    data = {
        'user_id':user_id,
        'sasquatch_id':sasquatch_id
    }
    new_skeptic_id = Skeptic.delete_skeptic(data)
    return redirect(f'/show/{sasquatch_id}')

