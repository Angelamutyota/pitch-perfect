from os import name
from flask import render_template, redirect, url_for, abort,request
from . import main
from flask_login import login_required, current_user
from ..models import User, Pitch, Comment, Upvote, Downvote
from .form import UpdateProfile, PitchForm, CommentForm
from .. import db, photos
from app.main import form

@main.route('/')
def index ():
    pitches = Pitch.query.filter_by().all()
    food = Pitch.query.filter_by(category = 'Food').all()
    it = Pitch.query.filter_by(category = 'IT').all() 
    entertainment = Pitch.query.filter_by(category = 'Entertainment').all() 
    sports = Pitch.query.filter_by(category = 'Sports').all() 



    title = "Home- This is the perfect spot to present your pitch to the world"
    return render_template('index.html', title= title, pitches= pitches, food=food, it=it, entertainment=entertainment,sports=sports)

@main.route('/pitch/<int:pitch_id>', methods = ['GET', 'POST'])
def pitch(pitch_id):
    pitches = Pitch.query.get(pitch_id)
    return render_template('pitch.html', pitches= pitches)

@main.route ('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    pitches = Pitch.query.filter_by(user_id=current_user.id).all()


    if user is None:
        abort(404)
    
    return render_template('profile/profile.html', user = user, pitches= pitches)

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

@main.route('/user/<name>/create_new', methods = ['POST','GET'])
@login_required
def new_pitch(name):
    user = User.query.filter_by(username = name).first()
    form = PitchForm()

    if user == None:
        abort(404)

    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_pitch_object = Pitch(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch_object.save_p()
        return redirect(url_for('.index', form = form))

    return render_template('new_pitch.html', form = form)

@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def comment_pitch (pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    user_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        new_comment.save_c()
        return redirect(url_for('.comment_pitch', pitch_id = pitch_id))
    return render_template('comments.html', form =form, pitch = pitch,all_comments=user_comments)

@main.route('/upvoted/<int:id>',methods = ['POST','GET'])
@login_required
def upvoted(id):
    like_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in like_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.id+=1
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/downvoted/<int:id>',methods = ['POST','GET'])
@login_required
def downvoted(id):
    pitch = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))

