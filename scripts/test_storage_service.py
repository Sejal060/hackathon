#!/usr/bin/env python3
"""
Test script to demonstrate the storage service functionality
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.storage_service import StorageService

def main():
    """Demonstrate storage service functionality"""
    print("🧪 Storage Service Demonstration")
    print("=" * 40)
    
    # Initialize storage service
    storage = StorageService()
    
    # Test data
    team_id = "demo_team_42"
    submission_data = {
        "team_id": team_id,
        "project_title": "Demo Project",
        "description": "A demonstration project for the storage service",
        "github_link": "https://github.com/demo/demo-project",
        "tech_stack": ["Python", "FastAPI", "BHIV"],
        "timestamp": int(time.time())
    }
    
    print(f"💾 Saving submission for team: {team_id}")
    
    # Save submission
    result = storage.save_submission(team_id, submission_data)
    print(f"✅ Submission saved successfully!")
    print(f"   Path: {result['path']}")
    print(f"   Filename: {result['filename']}")
    
    # Retrieve submission
    print(f"\n🔍 Retrieving submission for team: {team_id}")
    retrieved = storage.get_submission(team_id)
    if retrieved:
        print(f"✅ Submission retrieved successfully!")
        print(f"   Project Title: {retrieved['project_title']}")
        print(f"   Description: {retrieved['description']}")
    else:
        print("❌ Failed to retrieve submission")
    
    # List submissions
    print(f"\n📋 Listing all submissions for team: {team_id}")
    submissions = storage.list_submissions(team_id)
    print(f"✅ Found {len(submissions)} submissions")
    for sub in submissions:
        print(f"   - {sub['filename']} (Timestamp: {sub['timestamp']})")
    
    # List all submissions
    print(f"\n📋 Listing all submissions")
    all_submissions = storage.list_submissions()
    print(f"✅ Found {len(all_submissions)} total submissions")
    for sub in all_submissions[:3]:  # Show first 3
        print(f"   - {sub['team_id']}: {sub['filename']}")
    
    print("\n🎉 Storage service demonstration completed successfully!")
    print(f"\n📁 Check the data/bucket/ directory for saved files")

if __name__ == "__main__":
    main()