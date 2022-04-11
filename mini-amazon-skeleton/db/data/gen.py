import csv
import os
from itertools import product

from faker import Faker
from werkzeug.security import generate_password_hash

Faker.seed(0)
fake = Faker()

CURRENT_FOLD = os.path.dirname(os.path.abspath(__file__))


def get_csv_writer(f):
    return csv.writer(f, dialect="unix")


def gen_users(num_users):
    with open(f"{CURRENT_FOLD}/Users.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Users...", end=" ", flush=True)
        available_uids = []
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
            available_uids.append(uid)
        print(f"{num_users} generated")
    return available_uids


def gen_products(num_products, avaliable_uid):
    available_pids = []
    with open(f"{CURRENT_FOLD}/Products.csv", "w") as f:
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
            seller_id = fake.random_element(elements=avaliable_uid)
            overall_star = 0
            inv = fake.random_int(1, 20)
            cate = "c"
            desc = fake.sentence(nb_words=4)[:-1]

            writer.writerow(
                [pid, name, price, available, seller_id, overall_star, cate, desc, inv])
        print(f"{num_products} generated; {len(available_pids)} available")

    return available_pids


def gen_purchases(num_users, num_purchases, available_pids):
    available_uid_pid_pairs = []
    with open(f"{CURRENT_FOLD}/Purchases.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Purchases...", end=" ", flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            uid = fake.random_int(min=0, max=num_users - 1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
            available_uid_pid_pairs.append((uid, pid))
        print(f"{num_purchases} generated")
    return available_uid_pid_pairs


def gen_product_reviews(max_num_product_reviews, available_uid_pid_pairs):
    available_uid_pid_pairs = list(set(available_uid_pid_pairs))

    num_product_reviews = min(
        len(available_uid_pid_pairs), max_num_product_reviews)
    with open(f"{CURRENT_FOLD}/ProductReviews.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Reviews...", end=" ", flush=True)
        for id in range(num_product_reviews):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            uid, pid = available_uid_pid_pairs[id]
            comment = fake.text().replace("\n", "<br>")
            star = fake.random_int(1, 5)
            writer.writerow([id, uid, pid, comment, star])
        print(f"{num_product_reviews} generated")


def gen_seller_reviews(max_num_seller_reviews, available_uids):
    available_uid_uid_pairs = [
        uu_pair for uu_pair in product(available_uids, available_uids)]

    num_seller_reviews = min(
        len(available_uid_uid_pairs), max_num_seller_reviews)
    with open(f"{CURRENT_FOLD}/SellerReviews.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Reviews...", end=" ", flush=True)
        for id in range(num_seller_reviews):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            customer_id, seller_id = available_uid_uid_pairs[id]
            comment = fake.text().replace("\n", "<br>")
            star = fake.random_int(1, 5)
            writer.writerow([id, customer_id, seller_id, comment, star])
        print(f"{num_seller_reviews} generated")


def generate_all_data():
    num_users = 5
    num_products = 10
    num_purchases = 1000
    max_num_product_reviews = 1000
    max_num_seller_reviews = 1000

    available_uids = gen_users(num_users)
    available_pids = gen_products(num_products, available_uids)
    available_uid_pid_pairs = gen_purchases(
        num_users, num_purchases, available_pids)
    gen_product_reviews(max_num_product_reviews, available_uid_pid_pairs)
    gen_seller_reviews(max_num_seller_reviews, available_uids)


if __name__ == "__main__":
    generate_all_data()
