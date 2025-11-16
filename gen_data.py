from faker import Faker
import database
import random
from pathlib import Path

fake = Faker()

USER_COUNT = 9
ITEM_COUNT = 50
TRANSACTION_COUNT = 200
TRANSACTION_ITEM_COUNT = 300
CART_ITEM_COUNT = 20

def main():
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
    columns = ["username", "email", "birthdate"]
    values = Empty2dArray(USER_COUNT + 1, len(columns))

    for i in range(USER_COUNT):
        usernames.append(fake.user_name())
        email = fake.free_email()
        birthdate = fake.date_between(start_date = '-90y')

        values[i] = [Quote(usernames[i]), Quote(email), Quote(birthdate)]
    # Add default user for testing purposes
    usernames.append("default")
    values[USER_COUNT] = [Quote(usernames[USER_COUNT]), Quote("default@gmail.com"), Quote("1967-06-09")]

    ExecuteInsertQuery("users", columns, values)

    # Items
    print("Generating items")
    columns = ["item_id", "price", "name", "description"]
    values = Empty2dArray(ITEM_COUNT, len(columns))
    for i in range(ITEM_COUNT):
        item_id = i
        price = random.randint(0, 100) + 0.99
        name = f"{fake.word()} {fake.word()}";
        description = fake.text(max_nb_chars = 200)

        values[i] = [str(item_id), str(price), Quote(name), Quote(description)]
    ExecuteInsertQuery("items", columns, values)

    # Transactions
    print("Generating transactions")
    columns = ["transaction_id", "username", "time"]
    values = Empty2dArray(TRANSACTION_COUNT, len(columns))
    for i in range(TRANSACTION_COUNT):
        transaction_id = i
        username = random.choice(usernames)
        time = fake.date_time()

        values[i] = [str(transaction_id), Quote(username), Quote(time)]
    ExecuteInsertQuery("transactions", columns, values)

    # Transaction items
    print("Generating transaction_items")
    columns = ["transaction_id", "item_id", "quantity", "price"]
    values = Empty2dArray(TRANSACTION_ITEM_COUNT, len(columns))
    for i in range(TRANSACTION_ITEM_COUNT):
        transaction_id = random.randint(0, TRANSACTION_COUNT - 1)
        item_id = random.randint(0, ITEM_COUNT - 1)
        quantity = random.randint(1, 10)
        price = random.randint(0, 100) + 0.99

        values[i] = [str(transaction_id), str(item_id), str(quantity), str(price)]
    ExecuteInsertQuery("transaction_items", columns, values)

    # Cart items
    print("Generating cart_items")
    columns = ["username", "item_id", "quantity"]
    values = Empty2dArray(CART_ITEM_COUNT, len(columns))
    for i in range(CART_ITEM_COUNT):
        username = random.choice(usernames)
        item_id = random.randint(0, ITEM_COUNT - 1)
        quantity = random.randint(1, 10)

        values[i] = [Quote(username), str(item_id), str(quantity)]
    ExecuteInsertQuery("cart_items", columns, values)

def Quote(string: str) -> str:
    return f"'{string}'"

def Empty2dArray(rows, columns):
    return [["" for i in range(columns)] for j in range(rows)]

def ExecuteInsertQuery(table_name, column_names, values) -> None:
    query = f"INSERT IGNORE INTO {table_name} ("

    for name in column_names:
        query += name + ", "

    query = query[:-2] + ")\n"

    query += "VALUES "
    for value in values:
        query += "("
        for sub_value in value:
            query += sub_value + ", "
        query = query[:-2] + "),\n"
    query = query[:-2] + ";"

    database.execute_query(query)

if __name__ == "__main__":
    main()
