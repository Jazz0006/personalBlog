from main import db
from flask import Blueprint

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted")
    
@db_commands.cli.command("seed")
def seed_db():
    #from models.blogs import Blog
    from schemas.blog_schema import blog_schema
    from faker import Faker
    faker = Faker()

    for i in range(20):
        blog_json = {
            "blog_title" : faker.sentence(),
            "blog_content" : faker.text(),
            "blog_created" : faker.date()
        }
        blog = blog_schema.load(blog_json)
        db.session.add(blog)

    db.session.commit()
    print("Blogs table seeded")