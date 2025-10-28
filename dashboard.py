import streamlit as st
import pandas as pd
import json
import glob
import os
import plotly.express as px
import plotly.graph_objects as go

# Function to load data from JSON files
def load_data():
    # Load team data
    teams_data = []
    if os.path.exists("data/teams.json"):
        with open("data/teams.json", "r") as f:
            teams_data = json.load(f)
    
    # Load submission data from bucket
    submission_files = glob.glob("data/bucket/submission_*.json")
    submissions_data = []
    for file_path in submission_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                # Add filename to track submissions per team
                data["filename"] = os.path.basename(file_path)
                submissions_data.append(data)
        except Exception as e:
            st.warning(f"Error loading {file_path}: {e}")
    
    # Load reward data from bucket
    reward_files = glob.glob("data/bucket/reward_*.json")
    rewards_data = []
    for file_path in reward_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                rewards_data.append(data)
        except Exception as e:
            st.warning(f"Error loading {file_path}: {e}")
    
    return teams_data, submissions_data, rewards_data

# Function to process data for visualizations
def process_data(teams_data, submissions_data, rewards_data):
    # Create teams dataframe
    teams_df = pd.DataFrame(teams_data)
    
    # Create submissions dataframe
    submissions_df = pd.DataFrame(submissions_data)
    
    # Create rewards dataframe
    rewards_df = pd.DataFrame(rewards_data)
    
    # Calculate metrics
    if not submissions_df.empty:
        # Extract team_id from submissions
        submissions_df["team_id"] = submissions_df.get("team_id", "Unknown")
        
        # Count submissions per team
        submission_counts = submissions_df["team_id"].value_counts().reset_index()
        submission_counts.columns = ["team_id", "submission_count"]
    else:
        submission_counts = pd.DataFrame(columns=["team_id", "submission_count"])
    
    if not rewards_df.empty:
        # Calculate average reward per team (assuming we can extract team info)
        # For now, we'll just show overall reward statistics
        avg_reward = rewards_df["reward"].mean() if "reward" in rewards_df.columns else 0
        reward_distribution = rewards_df["reward"].value_counts().reset_index()
        reward_distribution.columns = ["reward_value", "count"]
    else:
        avg_reward = 0
        reward_distribution = pd.DataFrame(columns=["reward_value", "count"])
    
    return teams_df, submissions_df, rewards_df, submission_counts, reward_distribution

# Streamlit app
st.set_page_config(page_title="HackaVerse Dashboard", layout="wide")

# Title
st.title("📊 HackaVerse Dashboard")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# Load data
teams_data, submissions_data, rewards_data = load_data()

# Process data
teams_df, submissions_df, rewards_df, submission_counts, reward_distribution = process_data(
    teams_data, submissions_data, rewards_data
)

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Teams", len(teams_data))
with col2:
    st.metric("Total Submissions", len(submissions_data))
with col3:
    st.metric("Total Rewards", len(rewards_data))

# Display dataframes
st.subheader("Teams Data")
if not teams_df.empty:
    st.dataframe(teams_df)
else:
    st.info("No team data available")

st.subheader("Submissions Data")
if not submissions_df.empty:
    st.dataframe(submissions_df)
else:
    st.info("No submission data available")

st.subheader("Rewards Data")
if not rewards_df.empty:
    st.dataframe(rewards_df)
else:
    st.info("No reward data available")

# Visualizations
st.subheader("Visualizations")

# Leaderboard (Top teams by submission count)
if not submission_counts.empty:
    st.subheader("🏆 Leaderboard (by Submission Count)")
    fig_leaderboard = px.bar(
        submission_counts,
        x="team_id",
        y="submission_count",
        title="Teams by Submission Count",
        labels={"team_id": "Team ID", "submission_count": "Number of Submissions"}
    )
    st.plotly_chart(fig_leaderboard, use_container_width=True)
else:
    st.info("No submission data available for leaderboard")

# Score trend (using rewards data)
if not rewards_df.empty and "timestamp" in rewards_df.columns:
    st.subheader("📈 Reward Trend Over Time")
    rewards_df["timestamp"] = pd.to_datetime(rewards_df["timestamp"], unit="s")
    fig_trend = px.line(
        rewards_df,
        x="timestamp",
        y="reward",
        title="Reward Trend Over Time",
        labels={"timestamp": "Time", "reward": "Reward Value"}
    )
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("No reward data available for trend visualization")

# Acceptance rate (pie chart)
if not submissions_df.empty:
    st.subheader("📊 Submission Distribution")
    submission_status_counts = submissions_df.groupby("team_id").size().reset_index(name="count")
    fig_pie = px.pie(
        submission_status_counts,
        values="count",
        names="team_id",
        title="Submissions by Team"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("No submission data available for distribution visualization")

# Additional information
st.sidebar.header("Information")
st.sidebar.info("This dashboard visualizes data from the HackaVerse system.")
st.sidebar.markdown("**Data Sources:**")
st.sidebar.markdown("- `data/teams.json`")
st.sidebar.markdown("- `data/bucket/*.json`")