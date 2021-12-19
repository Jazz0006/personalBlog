from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from main import db
from models.items import Bought_Item
from schemas.item_schema import item_schema, items_schema
from sqlalchemy.sql import func

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
    # Get all items owned by current user
    my_items = current_user.bought_items    
    num_item = len(my_items)

    # Query for the total price
    select_total = db.session.query(
        func.sum(Bought_Item.item_price).label("total")
    ).filter(Bought_Item.owner_id==current_user.user_id)
    total_price = select_total.first()["total"]
    data = {
        "page_title" : "My items",
        "list_items" : items_schema.dump(my_items),
        "num_item" : num_item,
        "total_price" : total_price
    }
    return render_template("item_index.html", page_data=data)
    
@bought_items.route('/item/delete/<int:id>/')
@login_required
def delete_item(id):
    item = Bought_Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()