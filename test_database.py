import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Import the database module
from database import connect_to_db, get_db, close_db

def test_database_connection():
    """Test the database connection."""
    try:
        # Override the MONGO_URI environment variable for local testing
        os.environ['MONGO_URI'] = 'mongodb://localhost:27017'
        
        # Connect to the database
        print("Connecting to database...")
        connect_to_db()
        
        # Get the database instance
        db = get_db()
        print("Database connection successful!")
        
        # List collections
        collections = db.list_collection_names()
        print(f"Collections: {collections}")
        
        # Close the database connection
        close_db()
        print("Database connection closed.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_database_connection()