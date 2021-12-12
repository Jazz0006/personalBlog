from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os

(
    db_user, 
    db_pass, 
    db_name, 
    db_domain
) = (os.environ.get(item) for item in [
    "DB_USER", 
    "DB_PASS", 
    "DB_NAME", 
    "DB_DOMAIN"
    ]
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Blog(db.Model):
    __tablename__ = "blogs"
    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(80), nullable=False)
    blog_content = db.Column(db.Text())
    blog_created = db.Column(db.Date, nullable=False)

db.create_all()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return f'Here is the blogs pointer {blogs}'

@app.route('/blog/<int:id>/', methods = ['GET'])
def get_blog(id):
    blog = Blog.query.get_or_404(id)
    return f"Here will be the template of the blog {id}: {blog}"

if __name__ == '__main__':
    app.run(debug=True)