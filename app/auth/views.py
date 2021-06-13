from flask import render_template, url_for
from . import auth
from flask_login import login_user, login_required
from .forms import LoginForm, RegForm
from ..models import User
from .. import db

@auth.route('/login', methods = ['GET', 'POST'])
def