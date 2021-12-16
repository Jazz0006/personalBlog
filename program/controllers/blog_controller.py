from flask import Blueprint, jsonify, request, render_template, url_for
from werkzeug.utils import redirect
from main import db
from models.blogs import Blog
from schemas.blog_schema import blog_schema, blogs_schema
from flask_login import login_required, current_user
from datetime import datetime


blogs = Blueprint('blogs', __name__)

@blogs.route('/')
def hello_world():
    return 'Hello, World!'

@blogs.route('/blogs/', methods=['GET'])
def get_blogs():
    other_blogs = db.session.query(Blog).filter(Blog.blog_publicity==1)
    my_blogs = None
    if current_user.is_authenticated:
        other_blogs = other_blogs.filter(Blog.author_id!=current_user.user_id)
        my_blogs = db.session.query(Blog).filter(Blog.author_id==current_user.user_id)
    data = {
        "page_title" : "My Blogs",
        "other_blogs" : blogs_schema.dump(other_blogs),
        "my_blogs" : blogs_schema.dump(my_blogs)
    }
    return render_template("blog_index.html", page_data = data)

@blogs.route('/blogs/', methods=['POST'])
@login_required
def create_blog():
    # Get the form from the front end, and add the current time as blog_created
    web_form = dict(request.form)
    print(web_form)

    # Set the create time as the current time
    web_form["blog_created"] = datetime.today().strftime("%Y-%m-%d")

    # Create the new blog
    new_blog = blog_schema.load(web_form)
    new_blog.author = current_user
    
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(blog_schema.dump(new_blog))

@blogs.route('/blogs/<int:id>/', methods = ['GET'])
def get_blog(id):
    blog = Blog.query.get_or_404(id)
    blog_dict = blog_schema.dump(blog)
    data = {
        "page_title" : blog_dict["blog_title"],
        "blog" : blog_dict
    }   
    return render_template("blog_detail.html", page_data=data)

@blogs.route('/blogs/<int:id>/delete/', methods = ['POST'])
@login_required
def delete_blog(id):
    this_blog = Blog.query.get_or_404(id)
    db.session.delete(this_blog)
    db.session.commit()
    return redirect(url_for("blogs.get_blogs"))
