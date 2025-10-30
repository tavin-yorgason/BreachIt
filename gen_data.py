from faker import Faker
import database
import random
from pathlib import Path

fake = Faker()

USER_COUNT = 100
ITEM_COUNT = 50
TRANSACTION_COUNT = 200
TRANSACTION_ITEM_COUNT = 300
CART_ITEM_COUNT = 20

print("Resetting database")
try:
    database.execute_query(
    "DROP TABLE users, items, transactions, transaction_items, cart_items")
except:
    print("Error dropping tables. This probably means one or more tables\n"
        " were already gone.")

database.execute_queries(Path("create_tables.sql").read_text())

# Users
print("Generating users")
usernames = []
for i in range(USER_COUNT):
    usernames.append(fake.user_name())
    email = fake.free_email()
    birthdate = fake.date_between(start_date = '-90y')

    database.execute_query(
        "INSERT IGNORE INTO users (username, email, birthdate)"
        f"VALUES ('{usernames[i]}', '{email}', '{birthdate}');")

# Items
print("Generating items")
for i in range(ITEM_COUNT):
    item_id = i
    price = random.randint(0, 100) + 0.99
    name = f"{fake.word()} {fake.word()}";
    description = fake.text(max_nb_chars = 200)
    
    database.execute_query(
        "INSERT IGNORE INTO items (id, price, name, description)"
        f"VALUES ({item_id}, {price}, '{name}', '{description}');")

# Transactions
print("Generating transactions")
for i in range(TRANSACTION_COUNT):
    transaction_id = i
    username = random.choice(usernames)
    time = fake.date_time()
    
    database.execute_query(
        "INSERT IGNORE INTO transactions (id, username, time)"
        f"VALUES ({transaction_id}, '{username}', '{str(time)}');")

# Transaction items
print("Generating transaction_items")
for i in range(TRANSACTION_ITEM_COUNT):
    transaction_id = random.randint(0, TRANSACTION_COUNT - 1)
    item_id = random.randint(0, ITEM_COUNT - 1)
    quantity = random.randint(1, 10)
    price = random.randint(0, 100) + 0.99
    
    database.execute_query(
        "INSERT IGNORE INTO transaction_items (transaction_id, item_id, quantity, price)"
        f"VALUES ({transaction_id}, {item_id}, {quantity}, {price});")

# Cart items
print("Generating cart_items")
for i in range(TRANSACTION_ITEM_COUNT):
    username = random.choice(usernames)
    item_id = random.randint(0, ITEM_COUNT - 1)
    quantity = random.randint(1, 10)
    
    database.execute_query(
        "INSERT IGNORE INTO cart_items (username, item_id, quantity)"
        f"VALUES ('{username}', {item_id}, {quantity});")
