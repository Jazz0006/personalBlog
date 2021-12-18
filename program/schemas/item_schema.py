from marshmallow.fields import Nested
from marshmallow_sqlalchemy import auto_field
from main import ma
from models.items import Bought_Item

class ItemSchema(ma.SQLAlchemySchema):
    item_id = auto_field(dump_only=True)
    item_name = auto_field()
    item_description = auto_field()
    bought_at = auto_field()
    warrenty_expire = auto_field()
    # Todo: add validation, warrenty should be later than bought date
    
    item_price = auto_field()
    owner = ma.Nested(
        "UserSchema",
        only = ("user_id", "user_name", "email")
    )

    class Meta:
        model = Bought_Item
        load_instance = True

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)