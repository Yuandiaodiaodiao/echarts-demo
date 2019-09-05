from peewee import *
import json
with open('../web/src/config/config.json','r')as f:
    js=json.loads(f.read())
    dbpath=js['db_path']
    serverport=js['port']
    print(dbpath)
database = SqliteDatabase(dbpath)

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Category(BaseModel):
    category_description = CharField(column_name='categoryDescription', null=True)
    category_id = BigAutoField(column_name='categoryId', null=True)
    category_name = CharField(column_name='categoryName', null=True)

    class Meta:
        table_name = 'category'

class Food(BaseModel):
    category_id = BigIntegerField(column_name='categoryId', null=True)
    food_id = BigAutoField(column_name='foodId', null=True)
    food_name = CharField(column_name='foodName', null=True)
    id = BigIntegerField(null=True)
    min_purchase = IntegerField(column_name='minPurchase', null=True)
    month_sales = IntegerField(column_name='monthSales', null=True)
    price = FloatField(null=True)
    rating = FloatField(null=True)
    rating_count = IntegerField(column_name='ratingCount', null=True)
    statisfy_count = IntegerField(column_name='statisfyCount', null=True)
    statisfy_rate = FloatField(column_name='statisfyRate', null=True)

    class Meta:
        table_name = 'food'

class Shop(BaseModel):
    address = CharField(null=True)
    description = CharField(null=True)
    id = BigAutoField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    name = CharField(null=True)
    phone = CharField(null=True)
    promotion_info = TextField(null=True)

    class Meta:
        table_name = 'shop'

