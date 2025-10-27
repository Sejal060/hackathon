"""
Unit tests for the transaction manager
"""

import unittest
import os
import json
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.transaction_manager import Transaction, TransactionError, retry

class TestRetryDecorator(unittest.TestCase):
    """Test cases for the retry decorator"""
    
    def test_retry_success(self):
        """Test that retry decorator works when function succeeds"""
        call_count = 0
        
        @retry(max_retries=3, backoff=1)
        def succeeds_on_second_try():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Temporary failure")
            return "success"
        
        result = succeeds_on_second_try()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 2)
    
    def test_retry_failure(self):
        """Test that retry decorator raises exception after max retries"""
        call_count = 0
        
        @retry(max_retries=3, backoff=1)
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise Exception(f"Permanent failure {call_count}")
        
        with self.assertRaises(Exception) as context:
            always_fails()
        
        self.assertIn("Permanent failure 3", str(context.exception))
        self.assertEqual(call_count, 3)

class TestTransactionManager(unittest.TestCase):
    """Test cases for the Transaction class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Clean up any existing failed transactions file
        if os.path.exists("data/failed_transactions.json"):
            os.remove("data/failed_transactions.json")
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up failed transactions file
        if os.path.exists("data/failed_transactions.json"):
            os.remove("data/failed_transactions.json")
    
    def test_transaction_initialization(self):
        """Test that transaction is initialized correctly"""
        tx = Transaction("test_tx_123")
        self.assertEqual(tx.tx_id, "test_tx_123")
        self.assertEqual(len(tx._steps), 0)
    
    def test_add_step(self):
        """Test adding steps to transaction"""
        tx = Transaction("test_tx_123")
        
        def dummy_function(a, b):
            return a + b
        
        tx.add_step(dummy_function, 1, 2, keyword_arg="test")
        self.assertEqual(len(tx._steps), 1)
        
        fn, args, kwargs = tx._steps[0]
        self.assertEqual(fn, dummy_function)
        self.assertEqual(args, (1, 2))
        self.assertEqual(kwargs, {"keyword_arg": "test"})
    
    def test_commit_success(self):
        """Test successful transaction commit"""
        tx = Transaction("test_tx_123")
        
        # Add some steps
        results = []
        
        def step1():
            results.append("step1")
            return "result1"
        
        def step2():
            results.append("step2")
            return "result2"
        
        tx.add_step(step1)
        tx.add_step(step2)
        
        # Commit transaction
        commit_results = tx.commit()
        
        # Verify results
        self.assertEqual(results, ["step1", "step2"])
        self.assertEqual(commit_results, ["result1", "result2"])
    
    def test_commit_failure_logging(self):
        """Test that failed transactions are logged correctly"""
        tx = Transaction("test_tx_123")
        
        def failing_step():
            raise Exception("Intentional failure for testing")
        
        tx.add_step(failing_step)
        
        # Commit should raise TransactionError
        with self.assertRaises(TransactionError):
            tx.commit()
        
        # Verify that the failure was logged
        self.assertTrue(os.path.exists("data/failed_transactions.json"))
        
        with open("data/failed_transactions.json", "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            
            error_data = json.loads(lines[0])
            self.assertEqual(error_data["tx_id"], "test_tx_123")
            self.assertIn("Intentional failure for testing", error_data["error"])
    
    def test_commit_partial_failure(self):
        """Test that transaction fails fast on first error"""
        tx = Transaction("test_tx_123")
        
        execution_order = []
        
        def step1():
            execution_order.append("step1")
            return "result1"
        
        def step2():
            execution_order.append("step2")
            raise Exception("Step 2 failed")
        
        def step3():
            execution_order.append("step3")
            return "result3"
        
        tx.add_step(step1)
        tx.add_step(step2)
        tx.add_step(step3)
        
        # Commit should raise TransactionError
        with self.assertRaises(TransactionError):
            tx.commit()
        
        # Only step1 and step2 should have executed (step2 fails)
        self.assertEqual(execution_order, ["step1", "step2"])
        
        # Verify that the failure was logged
        self.assertTrue(os.path.exists("data/failed_transactions.json"))

if __name__ == '__main__':
    unittest.main()