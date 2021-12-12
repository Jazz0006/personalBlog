from flask import Blueprint, jsonify, request
from main import db
from models.blogs import Blog
from schemas.blog_schema import blog_schema, blogs_schema


blogs = Blueprint('blogs', __name__)

@blogs.route('/')
def hello_world():
    return 'Hello, World!'

@blogs.route('/blogs/', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify(blogs_schema.dump(blogs))

@blogs.route('/blogs/', methods=['POST'])
def create_blog():
    #print(request.get_data())
    new_blog = blog_schema.load(request.get_json())
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(blog_schema.dump(new_blog))

@blogs.route('/blog/<int:id>/', methods = ['GET'])
def get_blog(id):
    blog = Blog.query.get_or_404(id)
    return jsonify(blog_schema.dump(blog))