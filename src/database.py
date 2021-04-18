from peewee import (
    BooleanField,
    DateTimeField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

db = SqliteDatabase('packages.db')


class BaseModel(Model):
    class Meta:
        database = db


class Package(BaseModel):
    name = TextField()
    license = TextField()
    url = TextField()
    version = TextField()
    total_cost = IntegerField()
    total_lines = IntegerField()
    package_url = TextField()
    package_name = TextField()
    downloaded = BooleanField()
    date = DateTimeField()
    label = TextField()
    packge_type = TextField()


class LastPackage(BaseModel):
    name = TextField()
    version = TextField()
    total_cost = IntegerField()
    total_lines = IntegerField()
    group = TextField()


db.create_tables([LastPackage])

db.create_tables([Package])
