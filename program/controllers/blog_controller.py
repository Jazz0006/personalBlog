from flask import Blueprint, jsonify, request, render_template
from main import db
from models.blogs import Blog
from schemas.blog_schema import blog_schema, blogs_schema
from datetime import datetime


blogs = Blueprint('blogs', __name__)

@blogs.route('/')
def hello_world():
    return 'Hello, World!'

@blogs.route('/blogs/', methods=['GET'])
def get_blogs():
    data = {
        "page_title" : "My Blogs",
        "blogs" : blogs_schema.dump(Blog.query.all())
    }
    return render_template("blog_index.html", page_data = data)

@blogs.route('/blogs/', methods=['POST'])
def create_blog():
    # Get the form from the front end, and add the current time as blog_created
    web_form = dict(request.form)    
    web_form["blog_created"] = datetime.today().strftime("%Y-%m-%d")

    # Create the new blog
    new_blog = blog_schema.load(web_form)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(blog_schema.dump(new_blog))

@blogs.route('/blog/<int:id>/', methods = ['GET'])
def get_blog(id):
    blog = blog_schema.dump(Blog.query.get_or_404(id))
    data = {
        "page_title" : blog["blog_title"],
        "blog" : blog
    }
    return render_template("blog_detail.html", page_data=data)