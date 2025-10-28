# Dashboard Implementation

This document describes the implementation of the Streamlit dashboard for visualizing HackaVerse data.

## Overview

The dashboard has been updated to read data from JSON files in the `data/` and `data/bucket/` directories instead of MongoDB, and includes visualizations for key metrics.

## Features Implemented

### Data Sources
- `data/teams.json` - Team registration data
- `data/bucket/submission_*.json` - Project submissions
- `data/bucket/reward_*.json` - Reward data

### Visualizations
1. **Leaderboard** - Bar chart showing teams by submission count
2. **Reward Trend** - Line chart showing reward values over time
3. **Submission Distribution** - Pie chart showing submission distribution by team

### Interactive Elements
- Refresh button to reload data without restarting the dashboard
- Responsive layout with metrics display

## Implementation Details

### File: `dashboard.py`

The dashboard now uses the following approach:

```python
# Load data from JSON files
submission_files = glob.glob("data/bucket/submission_*.json")
reward_files = glob.glob("data/bucket/reward_*.json")

# Process data into DataFrames
submissions_df = pd.DataFrame(submissions_data)
rewards_df = pd.DataFrame(rewards_data)

# Create visualizations
fig_leaderboard = px.bar(submission_counts, x="team_id", y="submission_count")
fig_trend = px.line(rewards_df, x="timestamp", y="reward")
fig_pie = px.pie(submission_status_counts, values="count", names="team_id")
```

## Running the Dashboard

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execution
```bash
streamlit run dashboard.py
```

The dashboard will be available at http://localhost:8501

## Verification

To verify the dashboard functionality:

1. Run the simulation script:
   ```bash
   python simulate_teams.py
   ```

2. Start the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

3. Check that:
   - Team data is displayed in a table
   - Submission data is displayed in a table
   - Reward data is displayed in a table
   - Leaderboard chart shows teams by submission count
   - Reward trend chart shows reward values over time
   - Submission distribution pie chart shows team distribution
   - Refresh button reloads data

## Data Structure

### Teams Data (teams.json)
```json
{
  "id": "team_id",
  "team_name": "Team Name",
  "members": ["Member 1", "Member 2"],
  "email": "team@example.com",
  "college": "College Name",
  "contact_number": "+91-9876543210",
  "registered_at": "2025-07-31T13:55:15.709406",
  "status": "registered"
}
```

### Submission Data (bucket/submission_*.json)
```json
{
  "team_id": "demo_team_42",
  "project_title": "Demo Project",
  "description": "A demonstration project",
  "github_link": "https://github.com/demo/demo-project",
  "tech_stack": ["Python", "FastAPI", "BHIV"],
  "timestamp": 1761592447
}
```

### Reward Data (bucket/reward_*.json)
```json
{
  "action": "action1 | action2",
  "outcome": null,
  "reward": 2,
  "feedback": "Reward based on 2 executed step(s)",
  "timestamp": 1761590867.7999656,
  "steps_count": 2
}
```

## Screenshots

![Dashboard Overview](dashboard_overview.png)
*Dashboard showing team data and metrics*

![Leaderboard Visualization](dashboard_leaderboard.png)
*Leaderboard showing teams by submission count*

![Reward Trend](dashboard_trend.png)
*Reward trend over time*

![Submission Distribution](dashboard_pie.png)
*Submission distribution by team*