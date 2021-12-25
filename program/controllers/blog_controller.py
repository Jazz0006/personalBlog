from flask import Blueprint, jsonify, request, render_template, url_for, redirect
from main import db
from models.blogs import Blog
from schemas.blog_schema import blog_schema, blogs_schema
from flask_login import login_required, current_user
from datetime import datetime


blogs = Blueprint('blogs', __name__)


@blogs.route('/')
@blogs.route('/blogs/', methods=['GET'])
def get_blogs():
    # First get all public blogs
    public_blogs = db.session.query(Blog).filter(Blog.blog_publicity == 1)

    followed_private_blogs = None
    my_blogs = None
    if current_user.is_authenticated:
        # Adding private blogs from the authors that I follow.
        # And sort the blogs by date
        followed_private_blogs = current_user.followed_blogs()
        public_blogs = public_blogs.filter(
            Blog.author_id != current_user.user_id).union(
                followed_private_blogs).order_by(Blog.blog_created.desc())
        my_blogs = current_user.blogs
    else:
        public_blogs = public_blogs.order_by(Blog.blog_created.desc())
    data = {
        "page_title": "View Blogs",
        "other_blogs": blogs_schema.dump(public_blogs),
        "my_blogs": blogs_schema.dump(my_blogs)
    }
    return render_template("blog_index.html", page_data=data)


@blogs.route('/blogs/', methods=['POST'])
@login_required
def create_blog():
    # Get the form from the front end, and add the current time as blog_created
    web_form = dict(request.form)
    # print(web_form)

    # Set the create time as the current time
    #web_form["blog_created"] = datetime.today().strftime("%Y-%m-%d")

    # Create the new blog
    new_blog = blog_schema.load(web_form)
    new_blog.author = current_user

    db.session.add(new_blog)
    db.session.commit()
    return jsonify(blog_schema.dump(new_blog))


@blogs.route('/blogs/<int:id>/', methods=['GET'])
def get_blog(id):
    blog = Blog.query.get_or_404(id)
    blog_dict = blog_schema.dump(blog)
    data = {
        "page_title": blog_dict["blog_title"],
        "blog": blog_dict
    }
    return render_template("blog_detail.html", page_data=data)


@blogs.route('/blogs/<int:id>/delete/', methods=['POST'])
@login_required
def delete_blog(id):
    this_blog = Blog.query.get_or_404(id)
    db.session.delete(this_blog)
    db.session.commit()
    return redirect(url_for("blogs.get_blogs"))
