from peewee import (
    BooleanField,
    DateTimeField,
    ForeignKeyField,
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
    name = TextField(unique=True)
    license = TextField()
    url = TextField()


class PackageDependency(BaseModel):
    package = ForeignKeyField(Package, backref='package')
    dependency = ForeignKeyField(Package, backref='dependency')


class PackageHistory(BaseModel):
    name = ForeignKeyField(Package, backref='package')
    version = TextField()
    total_cost = IntegerField(default=0)
    total_lines = IntegerField(default=0)
    package_url = TextField()
    package_name = TextField()
    downloaded = BooleanField(default=False)
    date = DateTimeField()
    package_type = TextField(default='')


class LastPackage(BaseModel):
    name = ForeignKeyField(Package, backref='package')
    version = TextField()
    total_cost = IntegerField()
    total_lines = IntegerField()
    group = TextField()


db.create_tables([Package, LastPackage, PackageHistory, PackageDependency])
