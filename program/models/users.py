from sqlalchemy.orm import backref
from main import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from models.blogs import Blog
from models.items import Bought_Item
from models.cars import Car

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('flasklogin-users.user_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('flasklogin-users.user_id')),
)

class User(UserMixin, db.Model):

    __tablename__ = 'flasklogin-users'

    user_id = db.Column(
        db.Integer,
        primary_key = True
    )
    user_name = db.Column(
        db.String(100),
        nullable = False
    )
    email = db.Column(
        db.String(40),
        unique = True,
        nullable = False
    )
    password = db.Column(
        db.String(200),
        nullable = False
    )

    blogs = db.relationship(
        'Blog',
        backref="author"
    )

    followed = db.relationship(
        'User', 
        secondary=followers,
        primaryjoin=(followers.c.follower_id == user_id),
        secondaryjoin=(followers.c.followed_id == user_id),
        backref=db.backref('followers', lazy='dynamic'), 
        lazy='dynamic'
    )

    bought_items = db.relationship(
        'Bought_Item',
        backref="owner"
    )

    car = db.relationship(
        'Car',
        backref="owner"
    )

    # def __init__(self, name, email):
    #     self.user_name = name
    #     self.email = email


    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Overwirte get_id method to return the user_id
    def get_id(self):
        return (self.user_id)

    def is_following(self, user):
        ''' Check if I am following a given user'''
        return self.followed.filter(followers.c.followed_id == user.user_id).count() > 0

    def follow(self, user):
        ''' Follows the specified user '''
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        ''' Unfollow the speficied user '''
        if self.is_following(user):
            self.followed.remove(user)

    def followed_blogs(self):
        ''' Get the blogs that are posted by users that I follow '''
        return Blog.query.join(
            followers, (followers.c.followed_id == Blog.author_id)).filter(
                followers.c.follower_id == self.user_id).order_by(
                    Blog.blog_created.desc()
                )
            

