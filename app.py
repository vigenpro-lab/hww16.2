from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import utils
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf-8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User")
    order = db.relationship("Order")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


with app.app_context():
    #
    db.create_all()
    #
    users = utils.add_users_data(User, utils.read_json_file('users_data.json'))

    db.session.add_all(users)
    db.session.commit()

    orders = utils.add_orders_data(Order, utils.read_json_file('orders_data.json'))

    db.session.add_all(orders)
    db.session.commit()

    offers = utils.add_offers_data(Offer, utils.read_json_file('offers_data.json'))
    db.session.add_all(offers)
    db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        result = []
        users_to_show = User.query.all()
        for user in users_to_show:
            result.append(user.to_dict())
        return jsonify(result)

    elif request.method == 'POST':
        user_data = json.loads(request.data)
        modified_user = utils.add_new_user(User, user_data)
        db.session.add(modified_user)
        db.session.commit()
        return 201


@app.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_user_by_id(uid):
    if request.method == 'GET':
        user = User.query.get(uid)
        return jsonify(user.to_dict())

    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        user = User.query.get(uid)
        user.id = data_to_update['id']
        user.first_name = data_to_update["first_name"]
        user.last_name = data_to_update["last_name"]
        user.age = data_to_update['age']
        user.email = data_to_update['email']
        user.role = data_to_update['role']
        user.phone = data_to_update['phone']

        db.session.add(user)
        db.session.commit()

        return 201

    elif request.method == 'DELETE':
        user_to_delete = User.query.get(uid)
        db.session.delete(user_to_delete)
        db.session.commit()
        return 201


@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        result = []
        orders_to_show = Order.query.all()
        for order in orders_to_show:
            result.append(order.to_dict())
        return jsonify(result)

    elif request.method == 'POST':
        orders_data = json.loads(request.data)
        modified_order = utils.add_new_order(Order, orders_data)
        db.session.add(modified_order)
        db.session.commit()
        return 201


@app.route('/orders/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_order_by_id(uid):
    if request.method == 'GET':
        order = Order.query.get(uid)
        return jsonify(order.to_dict())

    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        order = Order.query.get(uid)
        order.id = data_to_update['id']
        order.name = data_to_update["name"]
        order.description = data_to_update["description"]
        order.start_date = data_to_update['start_date']
        order.end_date = data_to_update['end_date']
        order.address = data_to_update['address']
        order.price = data_to_update['price']
        order.customer_id = data_to_update['customer_id']
        order.executor_id = data_to_update['executor_id']

        db.session.add(order)
        db.session.commit()

        return 201

    elif request.method == 'DELETE':
        order_to_delete = Order.query.get(uid)
        db.session.delete(order_to_delete)
        db.session.commit()
        return 201


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        result = []
        offers_to_show = Offer.query.all()
        for offer in offers_to_show:
            result.append(offer.to_dict())
        return jsonify(result)

    elif request.method == 'POST':
        offers_data = json.loads(request.data)
        modified_offer = utils.add_new_offer(Offer, offers_data)
        db.session.add(modified_offer)
        db.session.commit()
        return 201


@app.route('/offers/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_offer_by_id(uid):
    if request.method == 'GET':
        offer = Offer.query.get(uid)
        return jsonify(offer.to_dict())

    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        offer = Offer.query.get(uid)
        offer.id = data_to_update['id']
        offer.order_id = data_to_update["order_id"]
        offer.executor_id = data_to_update["executor_id"]

        db.session.add(offer)
        db.session.commit()

        return 201

    elif request.method == 'DELETE':
        offer_to_delete = Offer.query.get(uid)
        db.session.delete(offer_to_delete)
        db.session.commit()
        return 201


app.run()
# f
