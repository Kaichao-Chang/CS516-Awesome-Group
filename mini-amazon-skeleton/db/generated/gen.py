import csv

from faker import Faker
from werkzeug.security import generate_password_hash

num_users = 3
num_products = 20
num_purchases = 25
max_num_reviews = 10

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect="unix")


def gen_users(num_users):
    with open("Users.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Users...", end=" ", flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f"{uid}", end=" ", flush=True)
            profile = fake.profile()
            email = profile["mail"]
            plain_password = f"pass{uid}"
            password = generate_password_hash(plain_password)
            name_components = profile["name"].split(" ")
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f"{num_users} generated")
    return


def gen_products(num_products):
    available_pids = []
    with open("Products.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Products...", end=" ", flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f"{pid}", end=" ", flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f"{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}"
            available = fake.random_element(elements=("true", "false"))
            if available == "true":
                available_pids.append(pid)
            writer.writerow([pid, name, price, available])
        print(f"{num_products} generated; {len(available_pids)} available")
    return available_pids


def gen_purchases(num_purchases, available_pids):
    available_uid_pid_pair = []
    with open("Purchases.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Purchases...", end=" ", flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            uid = fake.random_int(min=0, max=num_users - 1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
            available_uid_pid_pair.append((uid, pid))
        print(f"{num_purchases} generated")
    return available_uid_pid_pair


def gen_reviews(max_num_reviews, available_uid_pid_pair):
    available_uid_pid_pair = list(set(available_uid_pid_pair))

    num_reviews = min(len(available_pids), max_num_reviews)
    with open("Reviews.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Reviews...", end=" ", flush=True)

        for id in range(num_reviews):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            uid, pid = available_uid_pid_pair[id]
            comment = fake.text().replace("\n", "\\n")
            writer.writerow([id, uid, pid, comment])
        print(f"{num_reviews} generated")


gen_users(num_users)
available_pids = gen_products(num_products)
available_uid_pid_pair = gen_purchases(num_purchases, available_pids)
gen_reviews(max_num_reviews, available_uid_pid_pair)
