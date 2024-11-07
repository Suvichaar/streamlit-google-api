import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Function to create Google Sheets service
def get_google_sheets_service():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return build('sheets', 'v4', credentials=credentials)

# Function to create Google Docs service
def get_google_docs_service():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/documents.readonly"]
    )
    return build('docs', 'v1', credentials=credentials)

# Use the services in your app
st.title("Google Sheets and Docs Data Viewer")

# Example for Google Sheets (Add your sheet ID and range)
sheet_id = "1Fg4dplOnUFBX-L4i-mFaik75qjxdF6gO46irKm3qm3A"
range_name = "Sheet1!A1:D10"
sheets_service = get_google_sheets_service()
sheet = sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
values = sheet.get("values", [])
df = pd.DataFrame(values[1:], columns=values[0]) if values else pd.DataFrame()
st.dataframe(df)

# Example for Google Docs (Add your document ID)
doc_id = "1b-dHM3HIjgTcYPcu1lbikGNHkU3AdWbO72V2B1i7sfc"
docs_service = get_google_docs_service()
doc = docs_service.documents().get(documentId=doc_id).execute()
content = "\n".join([elem["textRun"]["content"] for elem in doc.get("body").get("content") if "textRun" in elem])
st.text_area("Document Content", content, height=400)
