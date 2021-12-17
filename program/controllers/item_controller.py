from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from main import db
from models.items import Bought_Item
from schemas.item_schema import item_schema, items_schema

bought_items = Blueprint('bought_items', __name__)

@bought_items.route('/items/', methods=["POST"])
@login_required
def add_item():
    web_form = request.form
    new_item = item_schema.load(web_form)
    new_item.owner = current_user
    db.session.add(new_item)
    db.session.commit()
    return "I registered an item"

@bought_items.route('/items/', methods=['GET'])
@login_required
def get_items():
    my_items = db.session.query(Bought_Item).filter(
        Bought_Item.owner_id==current_user.user_id
    )
    data = {
        "page_title" : "My items",
        "list_items" : items_schema.dump(my_items)
    }
    return render_template("item_index.html", page_data=data)
    