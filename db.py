from astrapy import DataAPIClient
from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv()

# Initialize the client
@st.cache_resource
def get_db():
    client = DataAPIClient(os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
    db = client.get_database_by_api_endpoint(
    os.getenv("ASTRA_DB_API_ENDPOINT")
    )

    return db

db = get_db()
collection_names = ["personal_data", "notes"]

for collection in collection_names:
    try:
        db.create_collection(collection)
    except:
        pass

personal_data = db.get_collection("personal_data")
notes = db.get_collection("notes")
