import streamlit as st
import pandas as pd
from pymongo import MongoClient

st.title("📊 BHIV Logs Dashboard")

client = MongoClient("mongodb://localhost:27017")
db = client["bhiv_db"]
logs = list(db["logs"].find())

if logs:
    st.success(f"✅ Total Logs: {len(logs)}")
    df = pd.DataFrame(logs)
    st.dataframe(df)
else:
    st.warning("No logs found in MongoDB.")
