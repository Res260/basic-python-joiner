import pprint
from functions import *

CUSTOMERS_FILE_PATH = "./data/customers.json"
ORDERS_FILE_PATH = "./data/orders.json"

customers_data = get_json_from_file(CUSTOMERS_FILE_PATH)
orders_data = get_json_from_file(ORDERS_FILE_PATH)

print("\ncustomers_data INNER JOIN orders_data:")
pprint.pprint(inner_join(customers_data, orders_data, 'cid', 'customer_id'))
print("\norders_data INNER JOIN customers_data:")
pprint.pprint(inner_join(orders_data, customers_data, 'customer_id', 'cid'))
print("\n")
print("\ncustomers_data FULL OUTER JOIN orders_data:")
pprint.pprint(full_outer_join(customers_data, orders_data, 'cid', 'customer_id'))
print("\norders_data FULL OUTER JOIN customers_data:")
pprint.pprint(full_outer_join(orders_data, customers_data, 'customer_id', 'cid'))
