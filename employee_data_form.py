import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.title("TCS Uruguay AI Initiatives.")

# Google Sheets configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Form fields
name = st.text_input("Name")
employee_number = st.text_input("Employee Number")
profile_type = st.selectbox("Profile Type", ["Non-Technical", "Somewhat technical", "Technical"])

# Google Sheets setup
@st.cache_resource
def get_google_sheets_client():
    """Initialize Google Sheets client with service account credentials."""
    try:
        # Use Streamlit secrets for deployment, fallback to JSON file for local development
        if 'google_sheets_credentials' in st.secrets:
            # For Streamlit Cloud deployment
            import json
            creds_dict = st.secrets['google_sheets_credentials']
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        else:
            # For local development - read from JSON file
            creds = Credentials.from_service_account_file(
                'service_account_key.json',
                scopes=SCOPES
            )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error setting up Google Sheets client: {e}")
        return None

# Google Sheet ID - you'll need to replace this with your actual Google Sheet ID
# You can find this in the URL of your Google Sheet
SHEET_ID = "1IcUAkAbmYfnt-udtb5fISeZs8ZIdm8w_kStZfhQfemg"  # Replace with your actual sheet ID
SHEET_NAME = "Employee Data"  # Name of the worksheet

if st.button("Submit"):
    if not name or not employee_number:
        st.error("Please fill in all fields.")
    else:
        try:
            # Get Google Sheets client
            client = get_google_sheets_client()
            if client is None:
                st.error("Failed to initialize Google Sheets client.")
                st.stop()
            
            # Open the spreadsheet
            spreadsheet = client.open_by_key(SHEET_ID)
            
            # Try to get the worksheet, create if it doesn't exist
            try:
                worksheet = spreadsheet.worksheet(SHEET_NAME)
            except gspread.WorksheetNotFound:
                # Create new worksheet if it doesn't exist
                worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=10)
                # Add headers
                worksheet.append_row(["Name", "Employee Number", "Profile Type", "Timestamp"])
            
            # Prepare data for insertion
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [name, employee_number, profile_type, timestamp]
            
            # Append the new row
            worksheet.append_row(new_row)
            
            st.success("Data saved to Google Sheets successfully!")
            
            # Display the updated data
            st.subheader("Current Data in Google Sheets:")
            data = worksheet.get_all_records()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.info("No data found in the sheet.")
                
        except Exception as e:
            st.error(f"Error saving data: {e}")
            st.info("Make sure you have:")
            st.info("1. Created a Google Cloud Project")
            st.info("2. Enabled Google Sheets API")
            st.info("3. Created a service account and downloaded the JSON key file")
            st.info("4. Shared your Google Sheet with the service account email")
            st.info("5. Updated the SHEET_ID variable with your actual Google Sheet ID")

# Instructions for setup
with st.expander("Setup Instructions"):
    st.markdown("""
    ### To use Google Sheets instead of Excel, follow these steps:
    
    1. **Create a Google Cloud Project:**
       - Go to [Google Cloud Console](https://console.cloud.google.com/)
       - Create a new project or select an existing one
    
    2. **Enable Google Sheets API:**
       - In the Google Cloud Console, go to "APIs & Services" > "Library"
       - Search for "Google Sheets API" and enable it
    
    3. **Create a Service Account:**
       - Go to "APIs & Services" > "Credentials"
       - Click "Create Credentials" > "Service Account"
       - Fill in the details and create the account
       - Click on the service account email
       - Go to "Keys" tab and create a new JSON key
       - Download the JSON file and save it as `service_account_key.json` in your project directory
    
    4. **Create a Google Sheet:**
       - Create a new Google Sheet
       - Copy the Sheet ID from the URL (the long string between /d/ and /edit)
       - Replace `YOUR_GOOGLE_SHEET_ID_HERE` in the code with your actual Sheet ID
    
    5. **Share the Sheet:**
       - Share your Google Sheet with the service account email (found in the JSON file)
       - Give it "Editor" permissions
    
    6. **Install Dependencies:**
       - Run: `pip install -r requirements.txt`
    """)
