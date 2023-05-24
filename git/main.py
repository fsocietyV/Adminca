from peewee import *

# Определяем модели таблиц
db = SqliteDatabase('example.db')

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

# Функция для вывода содержимого таблицы
def show_table(table_name):
    if table_name == 'clients':
        for client in Client.select():
            print(client.name, client.city, client.address, sep='\t')
    elif table_name == 'orders':
        for order in Order.select():
            print(order.client.name, order.date, order.amount, order.description, sep='\t')
    else:
        print('Unknown table name')

# Определяем логику программы
import sys

if len(sys.argv) == 1:
    print('Usage:')
    print('python program.py init - create database and tables')
    print('python program.py fill - fill tables with test data')
    print('python program.py show [tablename] - show contents of a table')
elif sys.argv[1] == 'init':
    create_tables()
elif sys.argv[1] == 'fill':
    fill_tables()
elif sys.argv[1] == 'show':
    if len(sys.argv) < 3:
        print('Table name is missing')
    else:
        show_table(sys.argv[2])
else:
    print('Unknown command')