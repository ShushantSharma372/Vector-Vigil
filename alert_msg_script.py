import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from twilio.rest import Client
from app import Alert  

# Define the database connection
DATABASE_URL = 'mysql+pymysql://root:Y1012Jqkhkp@localhost/project_db'
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Read the new data from CSV file
data = pd.read_csv('predicted_cases.csv')

# Get the current month
current_month = datetime.now().month

# Filter the data for the current month and cases > 10
filtered_data = data[(data['month'] == current_month) & (data['cases'] > 10)]

# Get the affected regions
affected_regions = filtered_data['region'].unique()

# Fetch mobile numbers from the alertformsubmissions table for the affected regions
all_submissions = session.query(Alert).all()
mobile_numbers = [submission.mobileNo for submission in all_submissions if submission.region in affected_regions]

# Twilio credentials
account_sid = 'Enter your sid'
auth_token = 'Enter your token'
client = Client(account_sid, auth_token)

# Message body
message_body = (
    "This is the alert message.\n"
    "The number of dengue cases in your region are expected to rise in the next month.\n"
    "Be sure to take preventive measures.\n"
    "Be safe and Healthy,\n"
    "Vector Vigil."
)

# Send messages
for number in mobile_numbers:
    message = client.messages.create(
        from_='your twilio number',  
        body=message_body,
        to='+91' + number
    )
    print(message.sid)
