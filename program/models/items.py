from main import db

class Bought_Item(db.Model):
    __tablename__ = "bought_items"
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(40), nullable=False)
    item_description = db.Column(db.Text())
    bought_at = db.Column(db.Date)
    warrenty_expire = db.Column(db.Date)
    item_price = db.Column(db.Float)
    owner_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.user_id'), nullable=False)