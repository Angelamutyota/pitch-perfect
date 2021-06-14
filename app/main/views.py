from flask import render_template, redirect, url_for, abort,request
from . import main
from flask_login import login_required, current_user
from ..models import User, Pitch, Comment, Upvote, Downvote
from .form import UpdateProfile, PitchForm, CommentForm
from .. import db, photos
from app.main import form

@main.route('/')
def index ():
    title = "Home- This is the perfect spot to present your pitch to the world"
    return render_template('index.html', title= title)

@main.route('/pitch/<int:pitch_id>', methods = ['GET', 'POST'])
def pitch(pitch_id):
    pitches = Pitch.query.get(pitch_id)

    return render_template('pitch.html', pitches= pitches)

@main.route ('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()

    if user is None:
        abort(404)
    
    return render_template('profile/profile.html', user = user)

@main.route('/user/<name>/profileupdate', methods = ['GET', 'POST'])
def profileupdate(name):
    user = User.query.filter_by(username = name).first()
    form = UpdateProfile()
    if user == None:
        abort(404)

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', name=user.username))

    return render_template ('profile/update.html', form= form, user=user)

@main.route ('/user/<name>/update pic', methods = ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', name=name))