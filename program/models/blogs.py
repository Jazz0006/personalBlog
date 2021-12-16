from main import db

class Blog(db.Model):
    __tablename__ = "blogs"
    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(80), nullable=False)
    blog_content = db.Column(db.Text())
    blog_created = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.user_id'), nullable=False)

    # Publicity of this blog article
    # 1 - Public
    # Everyone except those who are blocked can see this article
    # 2 - Private
    # Only those who follow the author can see this article
    blog_publicity = db.Column(db.Integer, default=1)