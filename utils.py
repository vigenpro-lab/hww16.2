import json


def read_json_file(file) -> list:
    with open(file, encoding="utf-8") as f:
        json_data = json.load(f)

    return json_data


def add_orders_data(class_name, data) -> list:
    orders = []
    for order in data:
        order_to_add = class_name(
            id=order['id'],
            name=order["name"],
            description=order["description"],
            start_date=order['start_date'],
            end_date=order['end_date'],
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )
        orders.append(order_to_add)

    return orders


def add_users_data(class_name, data) -> list:
    users = []
    for user in data:
        user_to_add = class_name(
            id=user['id'],
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        users.append(user_to_add)

    return users


def add_offers_data(class_name, data) -> list:
    offers = []
    for offer in data:
        offer_to_add = class_name(
            id=offer['id'],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"],
        )
        offers.append(offer_to_add)

    return offers


def add_new_user(class_name, data):
    new_user = class_name(
        id=data['id'],
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data['age'],
        email=data['email'],
        role=data['role'],
        phone=data['phone']
    )
    return new_user


def add_new_order(class_name, data):
    new_order = class_name(
        id=data['id'],
        name=data["name"],
        description=data["description"],
        start_date=data['start_date'],
        end_date=data['end_date'],
        address=data['address'],
        price=data['price'],
        customer_id=data['customer_id'],
        executor_id=data['executor_id']
    )
    return new_order


def add_new_offer(class_name, data):
    new_offer = class_name(
        id=data['id'],
        order_id=data["order_id"],
        executor_id=data["executor_id"],
    )
    return new_offer
