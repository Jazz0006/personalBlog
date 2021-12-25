# from sqlalchemy.sql.expression import table
from main import db
from flask import Blueprint
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
import json
from datetime import date


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
    from schemas.item_schema import item_schema
    from schemas.car_schema import car_schema
    from faker import Faker
    from random import randrange
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

        # Register a car to some users
        if i % 3 == 0:
            car_json = {
                "bought_at" : faker.date(),
                "next_service" : "2022-01-01",
                "service_period" : i % 2 + 1
            }
            car = car_schema.load(car_json)
            car.owner_id = i + 1
            db.session.add(car)

        # Adding fake blogs
        blog_json = {
            "blog_title" : faker.sentence(),
            "blog_content" : faker.text(),
            "blog_created" : faker.date(),
            
            # Half of the fake blogs are public, and half are private
            "blog_publicity" : i % 2 + 1
        }
        blog = blog_schema.load(blog_json)
        
        # Assign the author for the fake blog
        blog.author_id = i+1
        db.session.add(blog)

        # Adding items to this user
        for _ in range(randrange(1, 5)):
            item_json = {
                "item_name" : faker.bs().split()[0],
                "bought_at" : faker.date(),
                "item_price" : float(faker.pricetag()[1:].replace(",",""))
            }
            item = item_schema.load(item_json)
            item.owner_id = i + 1
            db.session.add(item)

    db.session.commit()
    print("Blogs table seeded")

@db_commands.cli.command("dump")
def dump_db():
    ''' Dump the database into backdb.txt file'''

    from config import app_config
    
    # Create the database engine
    engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)

    # Use the MetaData to reflect the whole database
    meta = MetaData()
    meta.reflect(bind=engine)

    # dump all tables into a dictionary
    result = {}
    for table in meta.sorted_tables:
        result[table.name] = [dict(row) for row in engine.execute(table.select())]

    # dump to json string
    json_obj = json.dumps(result, indent=4, default=str)

    # write to a txt file
    with open("backupdb.txt", 'w') as backup_file:
        backup_file.write(json_obj)

    print("Database has been dumped into backupcb.txt file")
    return None