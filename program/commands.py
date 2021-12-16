from main import db
from flask import Blueprint

from controllers.user_controller import load_user

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_cersion;")
    print("Tables deleted")
    
@db_commands.cli.command("seed")
def seed_db():
    #from models.blogs import Blog
    from schemas.blog_schema import blog_schema
    from schemas.user_schema import user_schema
    from faker import Faker
    faker = Faker()

    for i in range(20):
        # Adding fake users
        user_json = {
            "user_name" : faker.name(),
            "email" : faker.email(),
            "password" : "1234567"
        }
        user = user_schema.load(user_json)
        db.session.add(user)

        # Adding fake blogs
        blog_json = {
            "blog_title" : faker.sentence(),
            "blog_content" : faker.text(),
            "blog_created" : faker.date()
        }
        blog = blog_schema.load(blog_json)
        
        # Assign the author for the fake blog
        blog.author_id = i+1

        db.session.add(blog)

    db.session.commit()
    print("Blogs table seeded")