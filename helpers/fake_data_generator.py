import csv
from random import choice
from random import sample
from random import randint
from random import random
from datetime import datetime
from faker import Faker

N_CITIES = 10
N_PRODUCTS = 10
N_CLIENTS = 100
N_DAYS = 30
TRANSACTIONS_PER_DAY = 50
PRODUCTS_PER_TRANSACTION = 5
NULL_DOB_PROBABILITY = 0.1

if __name__ == '__main__':
    faker = Faker()

    # Cities
    cities = [faker.city() for _ in range(N_CITIES)]

    # Products
    products = [
        {'name': 'Milk', 'unit_price': 1.5},
        {'name': 'Pasta', 'unit_price': 3},
        {'name': 'Orange Juice', 'unit_price': 3.5},
        {'name': 'Cheese', 'unit_price': 2.5},
        {'name': 'Lettuce', 'unit_price': 2},
        {'name': 'Tomatoes', 'unit_price': 5},
        {'name': 'Bread', 'unit_price': 2},
        {'name': 'Ice Cream', 'unit_price': 5},
        {'name': 'Ice Cubes', 'unit_price': 1},
        {'name': 'Carrots', 'unit_price': 2.7},
        {'name': 'Potatoes', 'unit_price': 2.3},
    ]

    # Clients
    client_columns = ['client_id', 'name', 'date_of_birth', 'city']
    with open('fake_clients.csv', 'w', newline='') as csvfile:
        client_writer = csv.DictWriter(csvfile, fieldnames=client_columns)
        client_writer.writeheader()
        for i in range(N_CLIENTS):
            if random() > NULL_DOB_PROBABILITY:
                dob = faker.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
            else:
                dob = ''
            client = {
                'client_id': i+1,
                'name': faker.name(),
                'date_of_birth': dob,
                'city': choice(cities)
            }
            client_writer.writerow(client)

    # Transactions
    transaction_columns = ['transaction_id', 'client_id', 'date', 'product', 'quantity', 'unit_price', 'total']
    transaction_id = 1
    with open('fake_transactions.csv', 'w') as csvfile:
        transaction_writer = csv.DictWriter(csvfile, fieldnames=transaction_columns)
        transaction_writer.writeheader()
        for day in range(N_DAYS):
            curr_date = datetime(2019, 1, day+1)
            for day_transaction in range(randint(1, TRANSACTIONS_PER_DAY)):
                client_id = randint(1, N_CLIENTS+1)
                items = sample(products, randint(1, PRODUCTS_PER_TRANSACTION))
                quantity = randint(1, 5)
                for item in items:
                    total = item['unit_price'] * quantity
                    transaction_data = {
                        'transaction_id': transaction_id,
                        'client_id': client_id,
                        'date': curr_date.strftime('%Y-%m-%d'),
                        'product': item['name'],
                        'quantity': quantity,
                        'unit_price': item['unit_price'],
                        'total': total
                    }
                    transaction_writer.writerow(transaction_data)
                transaction_id += 1
