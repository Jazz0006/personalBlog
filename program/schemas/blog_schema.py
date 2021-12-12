from marshmallow_sqlalchemy.schema import auto_field
from main import ma
from models.blogs import Blog
from marshmallow_sqlalchemy import auto_field

class BlogSchema(ma.SQLAlchemySchema):
    blog_id = auto_field(dump_only=True)
    blog_title = auto_field(Required = True)
    blog_content = auto_field()
    blog_created = auto_field()

    class Meta:
        model = Blog
        load_instance = True

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)