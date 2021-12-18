from flask.json import jsonify
from main import db
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.cars import Car
from schemas.car_schema import car_schema
from schemas.user_schema import user_schema

my_car = Blueprint('cars', __name__)

@my_car.route('/car/', methods=['GET', 'POST'])
@login_required
def register_car():
    my_car = None
    if current_user.car:
        my_car = car_schema.dump(current_user.car[0])
    
    if request.method=="POST":
        if not current_user.car:
            web_form = request.form
            my_car = car_schema.load(web_form)
            my_car.owner = current_user
            db.session.add(my_car)
            db.session.commit()

    data = {
        "page_title" : "My Car",
        "my_car" : my_car
    }
    return render_template("car.html", page_data=data)   

@my_car.route("/car/delete/", methods=["POST"])
@login_required
def delete_car():
    #current_car = db.session.query(Car).filter(Car.owner_id==current_user.user_id).first()
    current_car = current_user.car[0]
    print(jsonify(car_schema.dump(current_car)))
    db.session.delete(current_car)
    db.session.commit()

    return redirect(url_for("cars.register_car"))
