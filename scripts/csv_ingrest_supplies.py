import csv
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth

from supplies_helper import get_supplies_id

# Define API endpoints
API_BASE_URL = "http://localhost:8000/api/v1"
SUPPLIES_URL = f"{API_BASE_URL}/supplies/"
SUPPLY_ORDERS_URL = f"{API_BASE_URL}/supply_orders/"
SUPPLY_ORDER_ITEMS_URL = f"{API_BASE_URL}/supply_order_items/"
CLIENTS_URL = f"{API_BASE_URL}/clients/"
AREAS_URL = f"{API_BASE_URL}/clients_area_serviced/"

# CSV file path
CSV_FILE_PATH = "./data/supplies.csv"

# Authentication credentials
USERNAME = "admin"
PASSWORD = "password"

# Format helper functions
def format_gender(input):
    # make the input lowercase
    input = input.lower()
    if input == "m":
        return "MA"
    elif input == "f":
        return "FE"
    elif input == "female":
        return "FE"
    elif input == "male":
        return "MA"
    return None

def format_ethnicity(input):
    input = input.lower()
    if "asian" in input:
        return "AS"
    elif "black" in input:
        return "BL"
    elif "hispanic" in input or "latino" in input or "spanish" in input:
        return "HI"
    elif "white" in input:
        return "WH"
    else:
        return "OT"
    
def format_date(date_str):
    # Parse the input date string
    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
    # Format the date to the desired format
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def format_age(age_str):
    try:
        return int(age_str)
    except ValueError:
        print (f"Invalid age value: {age_str}")
        return None
    
# Helper functions to interact with the API
def get_area_by_zipcode(zipcode):
    response = requests.get(AREAS_URL, params={"search": zipcode}, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    response.raise_for_status()
    areas = response.json()
    if areas:
        return areas[0]["id"]
    return None

def get_client_by_name(client_name):
    response = requests.get(CLIENTS_URL, params={"search": client_name}, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    response.raise_for_status()
    clients = response.json()
    if clients:
        return clients[0]["id"]
    return None

def create_client(client_data):
    client_id = get_client_by_name(client_data["name"])
    if client_id:
        return client_id
    response = requests.post(CLIENTS_URL, json=client_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    response.raise_for_status()
    return response.json()["id"]

def create_supply(supply_data):
    response = requests.post(SUPPLIES_URL, json=supply_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    response.raise_for_status()
    return response.json()["id"]

def create_supply_order(order_data):
    response = requests.post(SUPPLY_ORDERS_URL, json=order_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    response.raise_for_status()
    return response.json()["id"]

def create_supply_order_item(order_item_data):
    response = requests.post(SUPPLY_ORDER_ITEMS_URL, json=order_item_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    response.raise_for_status()
    return response.json()["id"]

# Main script
def ingest_data():
    with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=",")

        for row in reader:
            # Map client data
            client_data = {
                "name": row["Recipient's Name"],
                "age": format_age(row["Age"]) if row["Age"] else None,
                "gender": format_gender(row["Gender"]),
                "email": row["Email Address"],
                "phone": row["Phone Number"],
                "address": row["Address of Recipient"],
                "zipcode": row["ZIPCODE"],
                "ethnicity": format_ethnicity(row["Race/Ethnicity"]),
                "below_poverty_line": row["Under Poverty Level? (Below $1,250 a month)"].lower() == "yes",
                "homeless": row["Homeless?"].lower() == "yes",
                "veteran": row["Military Veteran?"].lower() == "yes" if "Military Veteran?" in row else False,
                "disabled": row["Disabled?"].lower() == "yes",
                "is_active": True,
                "area_serviced": get_area_by_zipcode(row["ZIPCODE"])
            }
            client_id = create_client(client_data)

            # Map supply order data
            supply_order_data = {
                "delivery_date": format_date(row["Date Received"]),
                "client": client_id
            }
            supply_order_id = create_supply_order(supply_order_data)

            print (f"Processing data for client: {client_data['name']}")

            # Map supplies and supply order items
            for i in range(19, 48):  
                # Get header name at index i
                supply_name = reader.fieldnames[i]
                supply_quantity = row[supply_name]
                if supply_name and supply_quantity:
                    supply_id = get_supplies_id(supply_name)
                    supply_quantity = row[supply_name]
                    if supply_id and supply_quantity:
                        supply_order_item_data = {
                            "quantity": int(supply_quantity),
                            "other_notes": "",
                            "order": supply_order_id,
                            "supplies": supply_id
                        }
                        print (f"Creating supply order item for supply: {supply_name}")
                        create_supply_order_item(supply_order_item_data)

if __name__ == "__main__":
    try:
        ingest_data()
        print("Data ingested successfully!")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
