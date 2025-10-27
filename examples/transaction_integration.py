#!/usr/bin/env python3
"""
Demo script to demonstrate the transaction manager functionality
"""

import time
from src.transaction_manager import Transaction, TransactionError
from src.storage_service import StorageService

# Mock functions to simulate the core flow
def submit_to_db(team_payload):
    """Simulate submitting team data to database"""
    print(f"Submitting team data to DB: {team_payload}")
    # Simulate some work
    time.sleep(0.1)
    return {"status": "submitted", "team_id": team_payload["team_id"]}

def run_reasoning(team_payload):
    """Simulate running reasoning on team data"""
    print(f"Running reasoning for team: {team_payload['team_id']}")
    # Simulate some work
    time.sleep(0.1)
    return {"reasoning_result": f"Reasoning completed for {team_payload['team_id']}"}

def calculate_reward(team_payload):
    """Simulate calculating reward for team"""
    print(f"Calculating reward for team: {team_payload['team_id']}")
    # Simulate some work
    time.sleep(0.1)
    return {"reward": 10.5, "feedback": "Good work!"}

def failing_step(team_payload):
    """Simulate a failing step for testing error handling"""
    print(f"Executing failing step for team: {team_payload['team_id']}")
    raise Exception("Intentional failure for demonstration")

def main():
    """Demonstrate transaction manager functionality"""
    print("🧪 Transaction Manager Demonstration")
    print("=" * 40)
    
    # Initialize components
    storage_service = StorageService()
    
    # Test data
    team_id = "demo_team_42"
    team_payload = {
        "team_id": team_id,
        "project_title": "Demo Project",
        "description": "A demonstration project for transactions",
        "github_link": "https://github.com/demo/demo-project"
    }
    
    print("✅ Testing successful transaction flow")
    
    # Create a successful transaction
    txn = Transaction(f"txn_{team_id}_{int(time.time())}")
    txn.add_step(submit_to_db, team_payload)
    txn.add_step(run_reasoning, team_payload)
    txn.add_step(calculate_reward, team_payload)
    txn.add_step(storage_service.save_submission, team_id, team_payload)
    
    try:
        results = txn.commit()
        print(f"✅ Transaction committed successfully!")
        print(f"   Results: {len(results)} steps completed")
        for i, result in enumerate(results):
            print(f"   Step {i+1}: {result}")
    except TransactionError as e:
        print(f"❌ Transaction failed: {e}")
    
    print("\n" + "=" * 40)
    print("❌ Testing failed transaction flow")
    
    # Create a failing transaction
    txn2 = Transaction(f"txn_fail_{team_id}_{int(time.time())}")
    txn2.add_step(submit_to_db, team_payload)
    txn2.add_step(run_reasoning, team_payload)
    txn2.add_step(failing_step, team_payload)  # This will fail
    txn2.add_step(storage_service.save_submission, team_id, team_payload)
    
    try:
        results = txn2.commit()
        print(f"✅ Transaction committed successfully!")
    except TransactionError as e:
        print(f"❌ Transaction failed as expected: {e}")
        print("   Check data/failed_transactions.json for logged error")
    
    print("\n🎉 Transaction manager demonstration completed!")

if __name__ == "__main__":
    main()