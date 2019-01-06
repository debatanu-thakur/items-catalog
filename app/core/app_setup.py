from flask import Flask, g, render_template, request, redirect, url_for
from flask import flash
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import session as login_session
from main import app, DBSession
from api import api_data
from models.base import Base
from db_config import Category, Base, Item, User
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import or_
import datetime
auth = HTTPBasicAuth()

photos = UploadSet('photos', IMAGES)
full_filepath = 'static/img/'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.before_request
def before_request():
    if request.method == "POST":
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return redirect(url_for('logout'))


@app.route('/users/<string:user_type>/', methods=['GET'])
def add_user(user_type):
    session = DBSession()
    if user_type == 'google':
        user_info = login_session.get('google_user')
        username = user_info["given_name"] if "given_name" in user_info \
            else None
        email = user_info["email"] if "email" in user_info else abort(400)
        name = user_info["name"] if "name" in user_info else None
        image = user_info["picture"].replace("https:", "") \
            if "picture" in user_info else None
        user_detail = session.query(User).filter_by(email=email).first()
        if user_detail is None:
            user = User(username=username, email=email, image=image, name=name)
            session.add(user)
            session.commit()
            user_detail = session.query(User).filter_by(email=email).first()
        login_session["user"] = user_detail.serialize
    remove_session()
    return redirect(url_for("default"))


@auth.verify_password
def verify_password(username_or_token):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).first()
    else:
        user = session.query(User).filter_by(
                username=username_or_token).first()
        if not user:
            login_session["user"] = user.serialize
            login_session["token"] = username_or_token
            return False
    login_session["user"] = user.serialize
    return True


@app.route('/')
def DefaultLandingToPage():
    if "user" in login_session:
        return redirect(url_for('default'))
    output = render_template('home.html')
    return output


@auth.login_required
@app.route('/catalog/')
def default():
    if "user" not in login_session or login_session["user"] is None:
        return redirect(url_for('DefaultLandingToPage'))

    session = DBSession()
    user_json = login_session["user"]
    user_detail = session.query(User).filter_by(id=user_json["id"]).first()
    if user_detail.is_admin():
        categories = session.query(Category)
    else:
        categories = session.query(Category).filter_by(user_id=user_json["id"])
    output = render_template('catalog.html',
                             categories=categories,
                             user_data=login_session["user"],
                             app_route='catalog')
    remove_session()
    return output


@auth.login_required
@app.route('/catalog/add/', methods=['GET', 'POST'])
def add_catalog():
    if request.method == 'POST':
        name = request.form['name']
        image = ''
        if 'image' in request.files:
            image = str(login_session["user"]["id"]) + \
                str(int(datetime.datetime.now().timestamp())) + "."
            image = photos.save(request.files['image'], name=image)
            image = photos.url(image)
        user_info = login_session['user']
        session = DBSession()
        category = session.query(Category).filter_by(name=name).first()
        if category is None:
            category = Category(name=name,
                                image=image,
                                user_id=user_info["id"])
            session.add(category)
            session.commit()
            category = session.query(Category).filter_by(name=name).first()
        remove_session()
        return redirect(url_for('default'))
    else:
        output = render_template('add-catalog.html')
    return output


@auth.login_required
@app.route('/catalog/<string:category_name>/')
def catalog(category_name):
    session = DBSession()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id,
                                          is_deleted=False)
    output = render_template('category.html',
                             category=category,
                             items=items,
                             user_data=login_session["user"])
    remove_session()
    return output


@auth.login_required
@app.route('/catalog/<string:category_name>/add/', methods=['GET', 'POST'])
def addItem(category_name):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = ''
        if 'image' in request.files:
            image = str(login_session["user"]["id"]) + \
                str(int(datetime.datetime.now().timestamp())) + "."
            image = photos.save(request.files['image'], name=image)
            image = photos.url(image)
        session = DBSession()
        category = session.query(Category).filter_by(name=category_name).one()
        item = Item(title=title, description=description, image=image,
                    category_id=category.id)
        session.add(item)
        session.commit()
        remove_session()
        return redirect(url_for('catalog', category_name=category_name))
    else:
        session = DBSession()
        category = session.query(Category).filter_by(name=category_name).one()
        output = render_template('add.html', category=category)
        remove_session()
    return output


@auth.login_required
@app.route('/catalog/<string:category_name>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_name, item_id):
    if "user" not in login_session or login_session["user"] is None:
        return redirect(url_for('DefaultLandingToPage'))
    session = DBSession()
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(id=item_id,
                                         category_id=category.id).one()
    if request.method == 'POST':
        item.title = request.form['title']
        item.description = request.form['description']
        image = ''
        if 'image' in request.files:
            image = str(login_session["user"]["id"]) + \
                str(int(datetime.datetime.now().timestamp())) + "."
            item.image = photos.save(request.files['image'], name=image)
            item.image = photos.url(item.image)
        session.add(item)
        session.commit()
        remove_session()
        return redirect(url_for('catalog', category_name=category_name))
    else:
        output = render_template('edit.html', category=category, item=item)
        remove_session()
    return output


@auth.login_required
@app.route('/catalog/<string:category_name>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_id):
    session = DBSession()
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        item.is_deleted = True
        session.add(item)
        session.commit()
        remove_session()
        return redirect(url_for('catalog', category_name=category_name))
    else:
        output = render_template('delete.html', category=category, item=item)
        remove_session()
    return output


@auth.login_required
@app.route('/login/<string:login_type>', methods=['GET'])
def loginLanding(login_type):
    if "user" in login_session:
        return redirect(url_for('default'))
    if login_type is None or login_type == '':
        login_type = 'signin'
    output = render_template('login.html', login_type=login_type)
    return output


@auth.login_required
@app.route('/login/<string:login_type>/', methods=['POST'])
def login(login_type):
    if "user" in login_session:
        return redirect(url_for('default'))
    session = DBSession()
    if login_type == 'signin':
        username = request.form['username']
        password = request.form['password']
        if username is None or username == '':
            flash('Please enter a username')
        elif password is None or password == '':
            flash('Please enter a password')
        else:
            user_detail = session.query(User).filter(or_(
                                                     User.username == username,
                                                     User.email == username)
                                                     ).first()
            if user_detail is None or \
                    not user_detail.verify_password(password):
                flash('Please verify the combination of username and password')
            else:
                remove_session()
                login_session["user"] = user_detail.serialize
                return redirect(url_for('default'))
    elif login_type == 'signup':
        username = request.form['username']
        email = request.form['email-address']
        password = request.form['password']
        password_retype = request.form['password-retype']
        # Validate the fields
        if username is None or username == '':
            flash('Please enter a username')
        elif email is None or email == '':
            flash('Please enter a valid email')
        elif password is None or password == '':
            flash('Please enter a password')
        elif password != password_retype:
            flash('Passwords should match')
        elif session.query(User).filter_by(email=email).first() is not None:
            flash('User with email already exists, please signin')
        else:
            user = User(username=username, email=email)
            user.has_password(password)
            session.add(user)
            session.commit()
            user = session.query(User).filter_by(email=email).first()
            login_session['user'] = user.serialize
            remove_session()
            return redirect(url_for('default'))
    remove_session()
    output = render_template('login.html', login_type=login_type)
    return output


@auth.login_required
@app.route('/logout/')
def logout():
    if "user" in login_session:
        login_session.pop("user", None)
    return redirect(url_for('DefaultLandingToPage'))


def remove_session():
    DBSession.remove()
