from main import db


class Car(db.Model):
    __tablename__ = "cars"
    car_id = db.Column(db.Integer, primary_key=True)
    bought_at = db.Column(db.Date, nullable=False)

    # 1 - one year
    # 2 - half year
    service_period = db.Column(db.Integer, default=1)
    next_service = db.Column(db.Date)

    # One on one relationship with the User
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('flasklogin-users.user_id'),
        nullable=False,
        unique=True)
