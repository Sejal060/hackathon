from src.security import security_manager
import time

# Clear ledger
security_manager.ledger = []
security_manager.used_nonces = set()

# Use the same timestamp for both entries to ensure consistent hashing
timestamp = int(time.time())

# Add first entry
data1 = {"team_id": "team123", "action": "submit"}
nonce1 = security_manager.generate_nonce()
signature1 = security_manager.sign_payload(data1, nonce1, timestamp)
entry1 = security_manager.add_to_ledger(data1, nonce1, timestamp, signature1)

# Add second entry
data2 = {"team_id": "team456", "action": "register"}
nonce2 = security_manager.generate_nonce()
signature2 = security_manager.sign_payload(data2, nonce2, timestamp)
entry2 = security_manager.add_to_ledger(data2, nonce2, timestamp, signature2)

# Get the actual entries from the ledger after both have been added
ledger_entries = security_manager.get_ledger()
actual_entry1 = ledger_entries[0]
actual_entry2 = ledger_entries[1]

print("Entry1:", actual_entry1)
print("Entry2:", actual_entry2)

# Verify ledger integrity
integrity = security_manager.verify_ledger_integrity()
print("Ledger integrity:", integrity)

if not integrity:
    # Debug each entry
    for i, entry in enumerate(ledger_entries):
        # Verify entry hash
        expected_hash = security_manager._hash_ledger_entry(entry, include_hash=False)
        print(f"Entry {i} hash check: {entry['entry_hash']} == {expected_hash} ? {entry['entry_hash'] == expected_hash}")
        
        # Verify chain integrity
        if i > 0:
            previous_entry = ledger_entries[i-1]
            expected_previous_hash = security_manager._hash_ledger_entry(previous_entry, include_hash=False)
            print(f"Entry {i} chain check: {entry['previous_hash']} == {expected_previous_hash} ? {entry['previous_hash'] == expected_previous_hash}")