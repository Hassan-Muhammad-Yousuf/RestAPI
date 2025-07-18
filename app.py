
from flask import Flask, request

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return 'Hello!'

@app.route('/drinks')
def get_drinks():
    drinks =  Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'id' : drink.id, 'name' : drink.name, 'description': drink.description}

        output.append(drink_data)
    return {"drinks": output}

@app.route('/drinks/<int:id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name" : drink.name, 'description' : drink.description}


@app.route('/drinks', methods=['POST'])
def add_drink():
    data = request.json
    new_drink = Drink(name=data['name'], description=data['description'])
    db.session.add(new_drink)
    db.session.commit()
    return {'id': new_drink.id}

@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"Error": "Not Found"}
    db.session.delete(drink)
    db.session.commit()
    return {"Message": "Delete Sucessfully"}