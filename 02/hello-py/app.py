import os

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


migrate = Migrate(app, db)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Data


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user', methods=['POST', 'GET'])
def user():
    result: dict
    if request.method == 'POST':  # create
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']

        try:
            data = Data(name, email, phone)
            db.session.add(data)
            db.session.commit()
            result = user_schema.dump(data)
        except:
            result = {"response": "Error: Unable to add item to database"}
    elif request.method == 'GET':  # read
        try:
            data = Data.query.all()
            result = users_schema.dump(data)
        except:
            result = {"response": "Error: Unable to select item from database"}

    return jsonify(result)


@app.route('/user/<id>', methods=['GET', 'DELETE', 'PUT'])
def user_id(id):
    result: dict

    if request.method == 'PUT':  # update
        try:
            data = Data.query.get(id)
            data.name = request.json['name']
            data.email = request.json['email']
            data.phone = request.json['phone']

            db.session.commit()
            result = user_schema.dump(data)
        except:
            result = {"response": "Error: Unable to update item to database"}
    elif request.method == 'DELETE':  # delete
        try:
            data = Data.query.get(id)
            db.session.delete(data)
            db.session.commit()
            result = user_schema.dump(data)
        except:
            result = {"response": "Error: Unable to delete item from database"}
    elif request.method == 'GET':  # read
        try:
            data = Data.query.get(id)
            result = user_schema.dump(data)
        except:
            result = {"response": "Error: Unable to select item from database"}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=9090)
