import flask_login
from models import User
from __init__ import *
app = create_app()

app.secret_key = 'super secret string'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user



@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

# delete this later
