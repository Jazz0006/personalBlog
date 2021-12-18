from main import ma
from marshmallow_sqlalchemy import auto_field
from marshmallow import validate, fields, exceptions
from werkzeug.security import generate_password_hash

from models.users import User

class UserSchema(ma.SQLAlchemySchema):
    user_id = auto_field(dump_only=True)
    user_name = auto_field(required=True, validate=validate.Length(min=1))
    email = auto_field(required=True, validate=validate.Email())
    car = auto_field()
    password = fields.Method(
        required = True,
        load_only = True,
        deserialize="load_password"
    )

    def load_password(self, password):
        if len(password)>6:
            return generate_password_hash(password, method='sha256')
        raise exceptions.ValidationError("Password must be at least 6 harachers.")

    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserSchema(partial=True)