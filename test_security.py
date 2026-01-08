import time
import hmac
import hashlib
from src.security import SecurityManager, validate_request_signing, validate_replay_protection, check_rate_limit, get_api_key_role


def test_security_manager():
    print("Testing SecurityManager...")

    sm = SecurityManager()
    secret = "test_secret"
    sm.api_secret = secret

    # Test verify_signature_valid
    timestamp = "1234567890"
    body = '{"test": "data"}'
    message = f"{timestamp}{body}".encode('utf-8')
    signature = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    assert sm.verify_signature(timestamp, body, signature), "Valid signature should pass"
    print("PASS: Valid signature accepted")

    # Test verify_signature_invalid
    assert not sm.verify_signature(timestamp, body, "invalid_signature"), "Invalid signature should fail"
    print("PASS: Invalid signature rejected")

    # Test verify_nonce_valid
    nonce = "test_nonce"
    timestamp_int = int(time.time())
    assert sm.verify_nonce(nonce, timestamp_int), "Valid nonce should pass"
    print("PASS: Valid nonce accepted")

    # Test verify_nonce_reused
    assert not sm.verify_nonce(nonce, timestamp_int), "Reused nonce should fail"
    print("PASS: Reused nonce rejected")

    # Test verify_nonce_old_timestamp
    old_timestamp = int(time.time()) - 400
    assert not sm.verify_nonce("new_nonce", old_timestamp), "Old timestamp should fail"
    print("PASS: Old timestamp rejected")


def test_validation_functions():
    print("\nTesting validation functions...")

    # Test validate_request_signing_missing_headers (when not enforced)
    try:
        validate_request_signing(None, '{"test": "data"}', None)
        print("PASS: Missing signature headers allowed when not enforced")
    except:
        print("FAIL: Missing signature headers should be allowed when not enforced")
        raise

    # Test validate_replay_protection_missing_headers (when not enforced)
    try:
        validate_replay_protection(None, None)
        print("PASS: Missing nonce headers allowed when not enforced")
    except:
        print("FAIL: Missing nonce headers should be allowed when not enforced")
        raise


def test_rate_limiting():
    print("\nTesting rate limiting...")

    # Test under limit
    try:
        check_rate_limit("test_key", "/agent/test")
        print("PASS: Rate limit under threshold allowed")
    except:
        print("FAIL: Rate limit under threshold should be allowed")
        raise


def test_role_mapping():
    print("\nTesting role mapping...")

    # Test admin role (using the actual API_KEY from environment)
    import os
    admin_key = os.getenv("API_KEY", "default_key")
    role = get_api_key_role(admin_key)
    assert role == "admin", f"API_KEY '{admin_key}' should have admin role"
    print("PASS: API_KEY has admin role")

    # Test agent role
    role = get_api_key_role("agent_key_demo")
    assert role == "agent", "Agent key should have agent role"
    print("PASS: Agent API key has agent role")

    # Test nonexistent key
    role = get_api_key_role("nonexistent_key")
    assert role is None, "Nonexistent key should return None"
    print("PASS: Nonexistent key returns None")


def main():
    print("Running security tests...\n")

    try:
        test_security_manager()
        test_validation_functions()
        test_rate_limiting()
        test_role_mapping()

        print("\nSUCCESS: All security tests passed!")
        return True
    except Exception as e:
        print(f"\nFAILED: Test failed: {e}")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)