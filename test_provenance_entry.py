#!/usr/bin/env python3
"""
Test script to create a provenance entry
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.database import connect_to_db_with_retry, get_db
from src.security import create_entry

def test_provenance_entry():
    """Test creating a provenance entry"""
    try:
        # Connect to database
        connect_to_db_with_retry(retries=1, delay=1)
        db = get_db()
        
        # Create a test entry
        entry = create_entry(
            db,
            actor="test_script",
            event="test_event",
            payload={"test": "data", "timestamp": 1234567890}
        )
        
        print(f"Created provenance entry: {entry['entry_hash']}")
        print(f"Entry signature: {entry['signature'][:20]}...")
        
        # Count entries
        count = db.provenance_logs.count_documents({})
        print(f"Total provenance entries: {count}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_provenance_entry()