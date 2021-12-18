from models.cars import Car
from marshmallow_sqlalchemy.schema import auto_field
from main import ma
from marshmallow.validate import OneOf

class CarSchema(ma.SQLAlchemySchema):
    car_id = auto_field(dump_only=True)
    bought_at = auto_field()
    service_period = auto_field(validate=OneOf([1,2]))
    next_service = auto_field()
    owner_id = ma.Nested(
        "UserSchema",
        only = ("user_id", "user_name", "email")
    )

    class Meta:
        model = Car
        load_instance = True

car_schema = CarSchema()
cars_schema = CarSchema(many=True)