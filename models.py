from peewee import *

db = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Company(BaseModel):
    id = AutoField()
    name = TextField()
    password = TextField()

class Product(BaseModel):
    name = TextField()
    price = FloatField()
    category = TextField()
    company = ForeignKeyField(Company, backref='products')

def init_db():
    db.connect()
    db.drop_tables([Product, Company])
    db.create_tables([Product, Company])