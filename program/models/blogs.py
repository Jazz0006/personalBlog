from main import db

class Blog(db.Model):
    __tablename__ = "blogs"
    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(80), nullable=False)
    blog_content = db.Column(db.Text())
    blog_created = db.Column(db.Date, nullable=False)