import os
import pytest
from peewee import *

# Определяем модели таблиц
db = SqliteDatabase(':memory:')

class Client(Model):
    name = CharField()
    city = CharField()
    address = CharField()

    class Meta:
        database = db

class Order(Model):
    client = ForeignKeyField(Client, backref='orders')
    date = DateField()
    amount = FloatField()
    description = TextField()

    class Meta:
        database = db

# Функция для создания таблиц в базе данных
def create_tables():
    with db:
        db.create_tables([Client, Order])

# Функция для заполнения таблиц данными
def fill_tables():
    import random
    import string

    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    clients = []
    for i in range(10):
        name = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
        city = random.choice(cities)
        address = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        client = Client.create(name=name, city=city, address=address)
        clients.append(client)

    for i in range(10):
        client = random.choice(clients)
        date = '2022-{:02d}-{:02d}'.format(random.randint(1,12), random.randint(1,28))
        amount = round(random.uniform(100, 1000), 2)
        description = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        Order.create(client=client, date=date, amount=amount, description=description)

# Функция для проверки наличия базы данных
def test_database_created():
    assert os.path.isfile('example.db') == True

# Функция для проверки наличия необходимых колонок
def test_database_columns():
    columns = [column.name for column in Client._meta.sorted_fields]
    assert 'name' in columns
    assert 'city' in columns
    assert 'address' in columns

    columns = [column.name for column in Order._meta.sorted_fields]
    assert 'client_id' in columns
    assert 'date' in columns
    assert 'amount' in columns
    assert 'description' in columns

# Функция для проверки наличия строк в базе данных
def test_database_rows():
    assert Client.select().count() >= 10
    assert Order.select().count() >= 10