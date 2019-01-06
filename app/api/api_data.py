from api.endpoints import user
from db_config import Category, Base, Item, User
from flask import session as login_session
from main import app, DBSession
from flask import jsonify, request, abort


@app.route('/json/users', methods=['POST'])
def new_user():
    remove_session()
    session = DBSession()
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if session.query(User).filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username, email=email)
    user.has_password(password)
    session.add(user)
    session.commit()
    remove_session()
    return jsonify({'username': user.username}), 201


@app.route('/json/catalog/',
           methods=['GET'])
def JSONDefault():
    session = DBSession()
    categories = session.query(Category)
    remove_session()
    output = jsonify(Categories=[cat.serialize for cat in categories])
    return output


@app.route('/json/catalog/<int:category_id>/',
           methods=['GET'])
def JSONCatalog(category_id):
    session = DBSession()
    items = session.query(Item).filter_by(category_id=category_id)
    remove_session()
    output = jsonify(Items=[item.serialize for item in items])
    return output


@app.route('/json/catalog/<int:category_id>/<int:item_id>/',
           methods=['GET'])
def JSONItem(category_id, item_id):
    session = DBSession()
    item = session.query(Item).filter_by(id=item_id).one()
    remove_session()
    output = jsonify(Item=item.serialize)
    return output


def remove_session():
    DBSession.remove()