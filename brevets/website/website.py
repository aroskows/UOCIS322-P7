from flask import Flask, render_template, request, redirect, url_for, abort, session
from urllib.parse import urlparse, urljoin
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user, UserMixin,
                         confirm_login, fresh_login_required)
from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, StringField, validators, PasswordField
from passlib.hash import sha256_crypt as pwd_context
import requests
import flask
import json
import jsonpickle
import base64


app = Flask(__name__)
app.secret_key = "secret words that no one knows"

class LoginForm(Form):
    username = StringField('Username', [
        validators.Length(min=2, max=25,
                          message=u"Huh, little too short for a username."),
        validators.InputRequired(u"Forget something?")])
    password = PasswordField('Password', [
        validators.Length(min=2, max=25,
                          message=u"Huh, little too short for a password."),
        validators.InputRequired(u"Forget something?")])
    remember = BooleanField('Remember me')

class RegistrationForm(Form):
    username = StringField('Username', [
        validators.Length(min=2, max=25,
                          message=u"Huh, little too short for a username."),
        validators.InputRequired(u"Forget something?")])
    password = PasswordField('Password', [
        validators.Length(min=2, max=25,
                          message=u"Huh, little too short for a password."),
        validators.InputRequired(u"Forget something?")])
    remember = BooleanField('Remember me')


def is_safe_url(target):
    """
    :source: https://github.com/fengsp/flask-snippets/blob/master/security/redirect_back.py
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def myhash(password):
    return pwd_context.using(salt="codeword").encrypt(password)
        

class User(UserMixin):
    def __init__(self, usrname, token, id_):
        self.token = token
        self.username = usrname
        self.id = id_

    def __str__(self):
        return str(self.username)
app.config.from_object(__name__)


login_manager = LoginManager() #this is from flask_login
login_manager.session_protection = "strong"

login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."

login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    ''' # Should retirn NONE if ID is not valid 
    app.logger.debug("LOAD USER")
    #return User.get(user_id)
    app.logger.debug(user_id)
    app.logger.debug(session['user'][user_id])'''
    ''' return the user with the id of user_id '''
    pass

login_manager.init_app(app)

'''
the stuff above may be wrong --> I stole it from DockerLogin/flaskLogin.py
'''

@app.route('/')
@app.route('/index')
@login_required
def home():
    return render_template('index.html')

@app.route("/register", methods =("POST", "GET"))
def register():
    '''
    frind the usernamer make sure its not in DB
    if not add it the database w/ the hashed password and increment to get
    the id
    ''' 
    form = RegistrationForm(request.form)
    app.logger.debug("REGISTER")
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        token = myhash(password)
        encode_token = base64.urlsafe_b64encode(token.encode("ascii"))
        app.logger.debug(username)
        
        app.logger.debug(token)
        app.logger.debug(encode_token)
        user = load_user(username)
        # see if  user is in database
        r = requests.get("http://restapi:5000/register/" + username + "/" +  str(encode_token))
        app.logger.debug(r)
        if r == False:
            abort(400)
        else:
            return r


    return render_template('register.html', form=form)

@app.route('/login', methods=("POST", "GET"))
def login():
    '''
    not gonna lie i have no idea
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        token = myhash(password)
      
        app.logger.debug(username)
        app.logger.debug(password)
        app.logger.debug(token)
        encode_token = base64.urlsafe_b64encode(token.encode("ascii"))
        #newuser = User(username, token, id_)
        #app.logger.debug(session)
        '''try:
            app.logger.debug("EXISTS")
            session['user'][str(newuser.id)] = jsonpickle.encode(newuser)
            app.logger.debug(session['user'])
        except:
            app.logger.debug("EXECPT")
            session['user'] = {str(newuser.id):  jsonpickle.encode(newuser)}
            app.logger.debug(session['user']) '''
        
        usr = login_user(newuser)
        app.logger.debug(usr)
        flask.flash("Logged in!")
        next = flask.request.args.get('next')
        app.logger.debug(next)
        if not is_safe_url(next):
            app.logger.debug("NOT SAFE")
            return flask.abort(400) # might be a diff error
        app.logger.debug("SAFE")
        return flask.redirect(next or flask.url_for('index'))
    
    return render_template('login.html', form=form)


@app.route('/listeverything')
def listeverything():
    ''' these ports might be wrong ?'''
    dtype = request.args.get("dtype") 
    topk = request.args.get("topk").strip()
    if topk == "":
        topk = "-1"

    r = requests.get('http://restapi:5000/listAll/' + dtype + "/" + topk)
    return flask.jsonify({"result": r.text})

@app.route('/listopentimes')
def listopentimes():
    dtype = request.args.get("dtype") 
    topk = request.args.get("topk").strip()
    if topk == "":
        topk = "-1"

    r = requests.get('http://restapi:5000/listOpen/' + dtype + "/" + topk)
    return flask.jsonify({"result": r.text})

@app.route('/listclosetimes')
def listclosetimes():
    dtype = request.args.get("dtype")
    topk = request.args.get("topk").strip()
    if topk == "":
        topk = "-1"
    app.logger.debug(type(topk))
    app.logger.debug(topk)
    r = requests.get('http://restapi:5000/listClose/' + dtype + "/" + topk) 
    app.logger.debug(r)
    
    return flask.jsonify({"result": r.text})

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
