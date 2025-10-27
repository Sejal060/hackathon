"""
Transaction Manager for HackaVerse
Provides atomic transaction handling with retry logic for critical operations
"""

import functools
import time
import json
import os
import logging
from typing import Any, Callable, List, Tuple, Optional

# Set up logging
logger = logging.getLogger(__name__)

def retry(max_retries=3, backoff=1):
    """
    Decorator to add retry logic to functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff: Backoff multiplier for retry delays
        
    Returns:
        Decorated function with retry logic
    """
    def deco(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            last_exception: Optional[Exception] = None
            for i in range(max_retries):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {i+1} failed for {f.__name__}: {str(e)}")
                    if i < max_retries - 1:  # Don't sleep on the last attempt
                        time.sleep(backoff * (i + 1))
            if last_exception:
                logger.error(f"All {max_retries} attempts failed for {f.__name__}: {str(last_exception)}")
                raise last_exception
            else:
                # This shouldn't happen, but just in case
                raise Exception(f"All {max_retries} attempts failed for {f.__name__}")
        return wrapper
    return deco

class TransactionError(Exception):
    """Exception raised when a transaction fails."""
    pass

class Transaction:
    """Manages a series of steps as a single atomic transaction."""
    
    def __init__(self, tx_id: str):
        """
        Initialize a new transaction.
        
        Args:
            tx_id: Unique identifier for this transaction
        """
        self.tx_id = tx_id
        self._steps: List[Tuple[Callable, Tuple, dict]] = []
        logger.info(f"Created transaction {tx_id}")
    
    def add_step(self, fn: Callable, *args, **kwargs) -> None:
        """
        Add a step to the transaction.
        
        Args:
            fn: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        """
        self._steps.append((fn, args, kwargs))
        logger.debug(f"Added step {fn.__name__} to transaction {self.tx_id}")
    
    def commit(self) -> List[Any]:
        """
        Execute all steps in the transaction sequentially.
        
        Returns:
            List of results from each step
            
        Raises:
            TransactionError: If any step fails
        """
        logger.info(f"Committing transaction {self.tx_id} with {len(self._steps)} steps")
        results = []
        
        try:
            # Execute steps sequentially
            for i, (fn, args, kwargs) in enumerate(self._steps):
                logger.debug(f"Executing step {i+1}: {fn.__name__}")
                result = fn(*args, **kwargs)
                results.append(result)
                logger.debug(f"Step {i+1} completed successfully")
            
            logger.info(f"Transaction {self.tx_id} committed successfully")
            return results
            
        except Exception as e:
            # Log failed transaction for manual review
            error_info = {
                "tx_id": self.tx_id,
                "error": str(e),
                "timestamp": time.time()
            }
            
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            
            try:
                with open("data/failed_transactions.json", "a") as fh:
                    fh.write(json.dumps(error_info) + "\n")
                logger.info(f"Failed transaction {self.tx_id} logged to data/failed_transactions.json")
            except Exception as log_error:
                logger.error(f"Failed to log transaction error: {str(log_error)}")
            
            logger.error(f"Transaction {self.tx_id} failed: {str(e)}")
            raise TransactionError(f"Transaction {self.tx_id} failed: {str(e)}") from e