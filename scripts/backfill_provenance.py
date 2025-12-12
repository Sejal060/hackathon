#!/usr/bin/env python3
"""
Backfill script for provenance logs.
Creates provenance entries for existing logs.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import connect_to_db_with_retry, get_db
from src.security import create_entry

def backfill_provenance():
    """Backfill provenance entries for existing logs"""
    try:
        # Connect to database
        connect_to_db_with_retry(retries=1, delay=1)
        db = get_db()
        
        # Check if we already have provenance entries
        count = db.provenance_logs.count_documents({})
        if count > 0:
            print(f"Found {count} existing provenance entries. Skipping backfill.")
            return
            
        # Create genesis entry
        print("Creating genesis provenance entry...")
        genesis_payload = {
            "event": "genesis",
            "description": "Genesis entry for provenance chain"
        }
        
        entry = create_entry(
            db, 
            actor="system", 
            event="provenance_genesis", 
            payload=genesis_payload
        )
        
        print(f"Created genesis entry: {entry['entry_hash']}")
        
        # Optionally backfill existing logs
        print("Checking for existing logs to backfill...")
        log_count = db.logs.count_documents({})
        if log_count > 0:
            print(f"Found {log_count} existing logs. Backfilling...")
            for log in db.logs.find().sort("timestamp", 1):
                try:
                    actor = log.get("actor", "system")
                    event = log.get("event", "legacy_log")
                    payload = {
                        "message": log.get("message", ""),
                        "level": log.get("level", "INFO")
                    }
                    
                    provenance_entry = create_entry(db, actor=actor, event=event, payload=payload)
                    print(f"Backfilled log entry: {provenance_entry['entry_hash']}")
                except Exception as e:
                    print(f"Failed to backfill log entry: {e}")
        else:
            print("No existing logs to backfill.")
            
        print("Backfill completed successfully.")
        
    except Exception as e:
        print(f"Error during backfill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    backfill_provenance()