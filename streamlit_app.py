import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "data/db.sqlite"

st.set_page_config(page_title="WNBA Predictor", layout="wide")
st.title("🏀 WNBA Over/Under Predictor")
st.markdown("View predictions made by the CLI model. Manual result tagging coming next.")

# Load prediction data from SQLite
@st.cache_data
def load_predictions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY date DESC", conn)
    conn.close()
    return df

# Display predictions
df = load_predictions()

if df.empty:
    st.warning("No predictions found in the database. Run the CLI script first.")
else:
    st.dataframe(df, use_container_width=True)
