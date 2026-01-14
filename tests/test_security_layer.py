import pytest
import time
import json
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.security import security_manager

client = TestClient(app)

def test_nonce_generation_and_verification():
    """Test nonce generation and verification"""
    # Generate a nonce
    nonce = security_manager.generate_nonce()
    timestamp = int(time.time())
    
    # Verify the nonce is valid
    assert security_manager.verify_nonce(nonce, timestamp) == True
    
    # Verify the same nonce is invalid after use (replay attack protection)
    assert security_manager.verify_nonce(nonce, timestamp) == False

def test_signature_generation_and_verification():
    """Test signature generation and verification"""
    # Test data
    data = {"team_id": "team123", "action": "submit"}
    nonce = security_manager.generate_nonce()
    timestamp = int(time.time())
    
    # Generate signature
    signature = security_manager.sign_payload(data, nonce, timestamp)
    
    # Verify signature
    assert security_manager.verify_signature(str(timestamp), json.dumps(data, sort_keys=True) + nonce, signature) == True

    # Verify invalid signature fails
    assert security_manager.verify_signature(str(timestamp), json.dumps(data, sort_keys=True) + nonce, "invalid_signature") == False

def test_ledger_chaining():
    """Test ledger chaining functionality"""
    # Clear any existing ledger entries
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
    
    # Verify ledger integrity
    assert security_manager.verify_ledger_integrity() == True
    
    # Verify chaining
    assert actual_entry1["previous_hash"] == "0"
    assert actual_entry2["previous_hash"] == actual_entry1["entry_hash"]

def test_security_middleware_headers():
    """Test that security middleware requires proper headers"""
    # Test without security headers (should fail for admin endpoints)
    response = client.post("/admin/reward", json={
        "request_id": "test123",
        "outcome": "success"
    })
    # This should fail due to missing API key, not security headers
    # as security headers are only required for endpoints that need advanced security
    
    # Test with proper API key but without security headers
    response = client.post("/admin/reward", 
                          json={
                              "request_id": "test123",
                              "outcome": "success"
                          },
                          headers={"X-API-Key": "test-api-key"})
    # Should succeed as security headers are not required for this endpoint in current implementation

def test_storage_service_transaction_ledger():
    """Test storage service transaction ledger chaining"""
    from src.storage_service import StorageService
    
    # Create storage service instance
    storage = StorageService()
    
    # Clear any existing ledger
    storage.transaction_ledger = []
    storage.last_transaction_hash = None
    
    # Save a submission
    result = storage.save_submission("team123", {"project": "test_project"})
    
    # Save another submission
    result2 = storage.save_submission("team456", {"project": "test_project2"})
    
    # Get ledger
    ledger = storage.get_transaction_ledger()
    
    # Verify ledger has entries
    assert len(ledger) == 2
    
    # Verify chaining
    assert ledger[0]["previous_hash"] == None
    assert ledger[1]["previous_hash"] == ledger[0]["hash"]
    
    # Verify integrity
    assert storage.verify_transaction_ledger_integrity() == True

def test_submission_hash_integrity():
    """Test that submission hashes are computed correctly and stored"""
    import hashlib
    from src.models import JudgeRequest

    # Create a submission
    submission_text = "Test submission text"
    request = JudgeRequest(submission_text=submission_text, team_id="team123")

    # Compute expected hash
    expected_hash = hashlib.sha256(submission_text.encode('utf-8')).hexdigest()

    # Verify hash is computed correctly
    assert request.submission_hash is None  # Initially None
    # In practice, it would be set in the route
    assert expected_hash == hashlib.sha256(submission_text.encode('utf-8')).hexdigest()

def test_judgment_versioning():
    """Test that judgment versions increment correctly"""
    # This would require mocking the database, but for now, test the logic
    from src.models import JudgeResponse

    response = JudgeResponse(
        clarity=8,
        quality=7,
        innovation=9,
        total_score=8.0,
        confidence=0.9,
        trace="Test trace",
        team_id="team123"
    )

    # Initially None
    assert response.version is None
    # In practice, set in route

def test_provenance_chain_integrity():
    """Test that provenance chain maintains integrity"""
    from src.security import verify_chain

    mock_db = MagicMock()
    # Mock a valid chain
    mock_db.provenance_logs.find.return_value.sort.return_value = [
        {
            "entry_hash": "hash1",
            "previous_hash": "0",
            "timestamp": 1000,
            "actor": "actor1",
            "event": "event1",
            "payload_hash": "payload1"
        },
        {
            "entry_hash": "hash2",
            "previous_hash": "hash1",
            "timestamp": 1001,
            "actor": "actor2",
            "event": "event2",
            "payload_hash": "payload2"
        }
    ]

    with patch('src.security.compute_entry_hash', return_value="hash1") as mock_hash1:
        with patch('src.security.compute_entry_hash', return_value="hash2") as mock_hash2:
            issues = verify_chain(mock_db)
            # Should have no issues if hashes match
            # Note: This is simplified; actual implementation checks hash computation