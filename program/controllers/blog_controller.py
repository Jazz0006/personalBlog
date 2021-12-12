from flask import Blueprint
from main import db
from models.blogs import Blog

blogs = Blueprint('blogs', __name__)

@blogs.route('/')
def hello_world():
    return 'Hello, World!'

@blogs.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return f'Here is the blogs pointer {blogs}'

@blogs.route('/blog/<int:id>/', methods = ['GET'])
def get_blog(id):
    blog = Blog.query.get_or_404(id)
    return f"Here will be the template of the blog {id}: {blog}"