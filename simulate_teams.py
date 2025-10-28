import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import random
import time
from data_manager import DataManager

# Initialize data manager
data_manager = DataManager()

def register_team(team_id):
    """Register a new team using the data manager"""
    team_name = f"Team_{team_id}"
    members = [f"Member_{i}" for i in range(1, 4)]
    email = f"team_{team_id}@example.com"
    college = f"College_{team_id}"
    contact_number = f"+91-98765432{team_id:02d}"
    
    try:
        team_id_result = data_manager.register_team(
            team_name=team_name,
            members=members,
            email=email,
            college=college,
            contact_number=contact_number
        )
        print(f"✅ Registered: {team_name} | Team ID: {team_id_result}")
        return team_id_result
    except ValueError as e:
        print(f"⚠️  Team {team_name} already exists: {e}")
        return None
    except Exception as e:
        print(f"❌ Error registering {team_name}: {e}")
        return None

def submit_sample_project(team_name):
    """Submit a sample project for a team"""
    try:
        project_id = data_manager.submit_project(
            team_name=team_name,
            project_title=f"AI Project {random.randint(10, 99)}",
            description=f"A demonstration project for team {team_name}",
            github_link=f"https://github.com/{team_name.lower().replace(' ', '-')}/project",
            tech_stack=["Python", "FastAPI", "BHIV"]
        )
        print(f"📤 Project submitted for {team_name} | Project ID: {project_id}")
        return project_id
    except Exception as e:
        print(f"❌ Error submitting project for {team_name}: {e}")
        return None

if __name__ == "__main__":
    print("Starting simulation...")
    registered_teams = []
    
    # Register teams
    for i in range(1, 8):
        print(f"\n--- Team {i} ---")
        team_id = register_team(i)
        if team_id:
            registered_teams.append(f"Team_{i}")
    
    # Submit sample projects for registered teams
    print("\n--- Submitting Sample Projects ---")
    for team_name in registered_teams:
        submit_sample_project(team_name)
        time.sleep(0.5)
    
    print(f"\n✅ Simulation completed! Registered {len(registered_teams)} teams.")