import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "data/db.sqlite"

st.set_page_config(page_title="WNBA Predictor", layout="wide")
st.title("🏀 WNBA Over/Under Predictor")
st.markdown("View predictions made by the CLI model.")

st.sidebar.header("🔍 Filter Predictions")

# Load prediction data from SQLite
@st.cache_data
def load_predictions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY date DESC", conn)
    conn.close()
    return df

def update_result(game_id, new_result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE predictions SET result = ? WHERE game_id = ?", (new_result, game_id))
    conn.commit()
    conn.close()

# Load full data
df_full = load_predictions()

# Sidebar filters
selected_result = st.sidebar.multiselect(
    "Filter by result", options=["Correct", "Incorrect", "Pending"], default=["Correct", "Incorrect", "Pending"]
)

confidence_range = st.sidebar.slider("Confidence Range", 0.5, 1.0, (0.5, 1.0), step=0.01)

selected_sportsbooks = st.sidebar.multiselect(
    "Sportsbooks", options=sorted(df_full["sportsbook"].unique()), default=list(df_full["sportsbook"].unique())
)

df = df_full[
    (df_full["result"].isin(selected_result)) &
    (df_full["confidence"].between(confidence_range[0], confidence_range[1])) &
    (df_full["sportsbook"].isin(selected_sportsbooks))
]

show_summary = st.checkbox("📊 Show Performance Summary", value=False)

if show_summary:
    st.subheader("📈 Performance Summary")
    if not df.empty:
        correct = (df["result"] == "Correct").sum()
        incorrect = (df["result"] == "Incorrect").sum()
        total = correct + incorrect

        if total > 0:
            hit_rate = round((correct / total) * 100, 2)
            st.markdown(f"**🎯 Hit Rate:** {hit_rate}% ({correct}/{total})")
        else:
            st.markdown("🎯 Hit Rate: _Not enough completed results yet_")

        st.bar_chart(df["result"].value_counts())
    else:
        st.info("No predictions match the selected filters.")

if df.empty:
    st.warning("No predictions found in the database. Run the CLI script first.")
else:
    st.subheader("📋 Predictions Table (Click to edit result)")
    
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 3, 2, 2, 2])
        with col1:
            st.markdown(f"**{row['team_home']} vs {row['team_away']}** ({row['date']}, {row['sportsbook'].capitalize()})")
        with col2:
            st.markdown(f"**Pick:** {row['prediction']}  |  **Line:** {row['line']}  |  **Predicted:** {row['predicted_total']}")
        with col3:
            st.markdown(f"**Confidence:** {round(row['confidence'], 2)}")
        with col4:
            current_result = row.get("result", "Pending")
            new_result = st.selectbox(
                label="Result",
                options=["Pending", "Correct", "Incorrect"],
                index=["Pending", "Correct", "Incorrect"].index(current_result),
                key=f"result_{i}"
            )
        with col5:
            if st.button("💾 Save", key=f"save_{i}"):
                update_result(row["game_id"], new_result)
                st.success(f"Result saved for {row['team_home']} vs {row['team_away']}")

    st.info("Scroll to view all games. You can update each result individually.")