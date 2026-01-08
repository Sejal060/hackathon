import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
import tempfile
from unittest.mock import patch, MagicMock
from src.security import (
    _sha256_hex,
    compute_payload_hash,
    compute_entry_hash,
    create_entry,
    verify_chain
)

def test_sha256_hex():
    """Test SHA-256 hash function"""
    result = _sha256_hex("test")
    assert isinstance(result, str)
    assert len(result) == 64  # SHA-256 produces 64 hex characters

def test_compute_payload_hash():
    """Test payload hash computation is deterministic"""
    payload1 = {"key": "value", "number": 42}
    payload2 = {"number": 42, "key": "value"}  # Same content, different order
    
    hash1 = compute_payload_hash(payload1)
    hash2 = compute_payload_hash(payload2)
    
    # Should be the same regardless of key order
    assert hash1 == hash2
    
    # Different payloads should produce different hashes
    payload3 = {"key": "different"}
    hash3 = compute_payload_hash(payload3)
    assert hash1 != hash3

def test_compute_entry_hash():
    """Test entry hash computation"""
    entry = {
        "previous_hash": "prev_hash",
        "timestamp": 1234567890,
        "actor": "test_actor",
        "event": "test_event",
        "payload_hash": "payload_hash"
    }
    
    hash1 = compute_entry_hash(entry)
    hash2 = compute_entry_hash(entry.copy())  # Same content
    
    assert hash1 == hash2
    assert isinstance(hash1, str)
    assert len(hash1) == 64

@patch('src.security.compute_entry_hash')
def test_create_entry(mock_compute_hash):
    """Test create_entry function"""
    mock_compute_hash.return_value = "a1b2c3d4e5f67890" * 4  # Valid 64-char hex string
    
    # Mock database
    mock_db = MagicMock()
    mock_db.provenance_logs.find_one.return_value = None  # No previous entry
    
    # Test create_entry
    entry = create_entry(
        mock_db,
        actor="test_actor",
        event="test_event",
        payload={"key": "value"}
    )
    
    # Verify the entry structure
    assert entry["actor"] == "test_actor"
    assert entry["event"] == "test_event"
    assert entry["entry_hash"] == "a1b2c3d4e5f67890" * 4
    assert entry["signature"] == "mock_signature"
    
    # Verify database call
    mock_db.provenance_logs.insert_one.assert_called_once()

def test_verify_chain_empty():
    """Test verify_chain with empty database"""
    mock_db = MagicMock()
    mock_db.provenance_logs.find.return_value.sort.return_value = []
    
    with patch('builtins.open', mock_open(read_data="test_public_key")):
        issues = verify_chain(mock_db)
        assert issues == []  # Should be empty for empty chain

# Helper for mock_open
def mock_open(read_data=""):
    mock_file = MagicMock()
    mock_file.__enter__ = lambda x: mock_file
    mock_file.__exit__ = lambda x, y, z, w: None
    mock_file.read.return_value = read_data
    return MagicMock(return_value=mock_file)