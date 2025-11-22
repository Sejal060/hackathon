# test_judging_engine.py
# Simple test script for the Judging Engine

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.judging_engine import JudgingEngine

def test_judging_engine():
    """Test the Judging Engine with a sample submission."""
    
    # Sample submission text
    sample_submission = """
    Project Title: AI-Powered Mental Health Companion
    
    Overview:
    Our project is an AI-powered mental health companion that uses natural language processing to provide 
    personalized support to users experiencing stress, anxiety, or depression. The system uses a combination 
    of sentiment analysis, conversational AI, and evidence-based therapeutic techniques to engage users in 
    meaningful conversations.
    
    Technical Implementation:
    - Built with Python and FastAPI for the backend
    - Uses OpenAI's GPT-3.5 for conversational AI
    - Implements sentiment analysis using TextBlob
    - Stores user interactions in MongoDB
    - Frontend built with React and Tailwind CSS
    - Deployed on Render with CI/CD pipeline
    
    Key Features:
    1. Personalized conversation flows based on user mood
    2. Crisis detection and escalation to human counselors
    3. Mood tracking and progress visualization
    4. Guided meditation and breathing exercises
    5. Resource recommendations based on user needs
    
    Innovation:
    Unlike existing mental health apps, our system focuses on building a genuine emotional connection 
    through AI, using advanced NLP to understand context and emotional undertones in user messages. 
    We also integrate with local mental health resources for seamless referrals.
    """
    
    # Initialize the judging engine
    engine = JudgingEngine()
    
    # Evaluate the submission
    print("Testing Judging Engine...")
    print("=" * 50)
    
    result = engine.evaluate(sample_submission, "test_team_123")
    
    print(f"Team ID: {result['team_id']}")
    print(f"Clarity Score: {result['clarity']}")
    print(f"Quality Score: {result['quality']}")
    print(f"Innovation Score: {result['innovation']}")
    print(f"Total Score: {result['total_score']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['trace']}")
    
    print("\n" + "=" * 50)
    print("Test completed successfully!")

if __name__ == "__main__":
    test_judging_engine()