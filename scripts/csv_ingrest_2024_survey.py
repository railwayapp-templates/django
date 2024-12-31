import csv
import requests
from requests.auth import HTTPBasicAuth

# File path to the CSV file containing the survey data
CSV_FILE_PATH = './data/2024_surveys.csv'

# Authentication credentials
USERNAME = 'admin'
PASSWORD = 'admin'

# Define the URL for the API endpoint
DJANGO_ENDPOINT = 'http://localhost:8000'
CLIENT_SURVEY_API_URL = DJANGO_ENDPOINT + '/clientsurveys2024/'
SURVEYOR_API_URL = DJANGO_ENDPOINT + '/surveyors/'
ZIPCODE_SURVEY_API_URL = DJANGO_ENDPOINT +'/zipcodesurveys/'

# Function to create a surveyor
def create_surveyor(name):
    response = requests.post(SURVEYOR_API_URL, data={'name': name},  auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"Failed to create surveyor: {response.content}")
        return None

# Function to get or create a zipcode survey
def get_or_create_zipcode(zipcode):
    response = requests.get(ZIPCODE_SURVEY_API_URL, params={'zipcode': zipcode}, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200 and response.json():
        return response.json()[0]['id']
    else:
        response = requests.post(ZIPCODE_SURVEY_API_URL, data={'zipcode': zipcode}, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        if response.status_code == 201:
            return response.json()['id']
        else:
            print(f"Failed to create zipcode survey: {response.content}")
            return None

# Function to create a client survey
def create_client_survey(data):
    response = requests.post(CLIENT_SURVEY_API_URL, data=data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 201:
        print(f"Successfully created client survey: {response.json()}")
    else:
        print(f"Failed to create client survey: {response.content}")

def ingest_data():
    # Read the CSV file and create surveys
    with open(CSV_FILE_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            surveyor_name = row['Surveyor']
            surveyor_id = create_surveyor(surveyor_name)
            zipcode_id = get_or_create_zipcode(row['ZIPCODE'])
            if surveyor_id and zipcode_id:
                client_survey_data = {
                    'uti_lastyear': row['Have you had a Urinary Tract Infection (UTI) in the last year?)'] == 'Yes',
                    'medical_treatment': row['If you sought medical care, did you have to see a doctor or go to the ER?'].split(', '),
                    'distance_to_healthcare': row['How far away from health care do you live?'],
                    'used_leakage_items': row['Have you ever used items to assist with leakage other than adult diapers, bladder pads/products ( such as towels, sheets, washcloths etc.)'] == 'Yes',
                    'helped_leave_home': row['Has having incontinent products helped you to leave home more to:'].split(', '),
                    'zipcode': zipcode_id,
                    'surveyor': surveyor_id,
                    'date': row['Date']
                }
                create_client_survey(client_survey_data)

if __name__ == "__main__":
    try:
        ingest_data()
        print("Data ingested successfully!")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")