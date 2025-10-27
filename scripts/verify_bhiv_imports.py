#!/usr/bin/env python3
"""
Verify that BHIV connector modules can be imported without errors.
"""

import sys
import os

# Add current directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all BHIV related modules can be imported."""
    try:
        # Test importing the connectors
        from hackathon.src.integrations.bhiv_connectors import send_to_core, save_to_bucket
        print("✅ Successfully imported bhiv_connectors")
        
        # Test importing executor (which now uses connectors)
        from hackathon.src.executor import Executor
        print("✅ Successfully imported executor")
        
        # Test importing reward system (which now uses connectors)
        from hackathon.src.reward import RewardSystem
        print("✅ Successfully imported reward system")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run import verification."""
    print("🔍 BHIV Module Import Verification")
    print("=" * 35)
    
    success = test_imports()
    
    print("=" * 35)
    if success:
        print("🎉 All imports successful!")
        return 0
    else:
        print("❌ Import verification failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())