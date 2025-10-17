#!/usr/bin/env python3
"""
Test script to trigger the N8N webhook for hackathon team registration
"""

import requests
import json

def test_webhook(webhook_url, team_data):
    """
    Send a test team registration to the N8N webhook
    
    Args:
        webhook_url (str): The N8N webhook URL
        team_data (dict): Team registration data
    """
    try:
        response = requests.post(
            webhook_url,
            json=team_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Team registration request sent successfully!")
        else:
            print("❌ Failed to send team registration request")
            
    except Exception as e:
        print(f"❌ Error sending request: {e}")

if __name__ == "__main__":
    # Example webhook URL - replace with your actual N8N webhook URL
    WEBHOOK_URL = "http://localhost:5678/webhook/team-registered"
    
    # Example team data
    teams = [
        {
            "team_name": "Team Alpha",
            "members": ["Alice", "Bob"],
            "email": "alpha@example.com",
            "college": "XYZ University"
        },
        {
            "team_name": "Team Beta",
            "members": ["Charlie", "David"],
            "email": "beta@example.com",
            "college": "ABC University"
        },
        {
            "team_name": "Team Gamma",
            "members": ["Eve", "Frank"],
            "email": "gamma@example.com",
            "college": "DEF University"
        }
    ]
    
    print("Testing N8N Hackathon Registration Workflow")
    print("=" * 50)
    
    for i, team in enumerate(teams, 1):
        print(f"\nSending registration for {team['team_name']} (Team {i}/{len(teams)})...")
        test_webhook(WEBHOOK_URL, team)
        
    print("\n🎉 All team registrations sent!")
    print("Check your N8N interface and email for results.")