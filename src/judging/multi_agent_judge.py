"""
Multi-Agent Judging System
Implements 3 specialized judge agents for competition-grade judging
"""
import os
import openai
from typing import Dict, Any, List
from dotenv import load_dotenv
import logging
from .rubric import CRITERIA, WEIGHTS

load_dotenv()
logger = logging.getLogger(__name__)

class MultiAgentJudge:
    def __init__(self):
        """
        Initialize the Multi-Agent Judging System with 3 specialized judge agents.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        
        # Define the three specialized judge agents
        self.judges = {
            "judge_a": {
                "name": "Technical Depth Judge",
                "specialty": "tech_depth",
                "description": "Focuses on technical implementation, architecture, and engineering excellence"
            },
            "judge_b": {
                "name": "Product & Impact Judge", 
                "specialty": "impact",
                "description": "Focuses on real-world impact, user value, and market potential"
            },
            "judge_c": {
                "name": "Clarity & UX Judge",
                "specialty": "clarity",
                "description": "Focuses on clarity of presentation, user experience, and communication"
            }
        }

    def _get_specialized_evaluation(self, judge_id: str, submission_text: str) -> Dict[str, Any]:
        """
        Get evaluation from a specialized judge agent.
        
        Args:
            judge_id: ID of the judge agent
            submission_text: The submission to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        if not self.api_key:
            # Return mock evaluation if no API key
            logger.warning("No OpenAI API key found, returning mock evaluation")
            specialty = self.judges[judge_id]["specialty"]
            mock_scores = {criterion: 7 for criterion in CRITERIA.keys()}
            return {
                "scores": mock_scores,
                "explanation": f"Mock evaluation by {self.judges[judge_id]['name']}",
                "confidence": 0.8
            }
        
        try:
            judge_info = self.judges[judge_id]
            specialty = judge_info["specialty"]
            
            # Create the prompt for the specialized judge
            prompt = f"""
            You are a specialized judge evaluating a hackathon submission. 
            Your specialty is: {judge_info['description']}
            
            Evaluate the following submission according to these criteria:
            {', '.join([f"{criterion} (max {max_score})" for criterion, max_score in CRITERIA.items()])}
            
            For each criterion, provide a score from 0 to the maximum score and a brief explanation.
            
            Submission:
            {submission_text}
            
            Please respond in the following JSON format:
            {{
                "scores": {{
                    {', '.join([f'"{criterion}": {CRITERIA[criterion] if criterion == specialty else max(1, CRITERIA[criterion]//2)}' for criterion in CRITERIA.keys()])}
                }},
                "explanation": "Brief explanation of your evaluation",
                "confidence": 0.9
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert {judge_info['name']} evaluating hackathon submissions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            # Extract the response
            evaluation_text = response.choices[0].message.content
            logger.info(f"LLM evaluation completed by {judge_info['name']}: {evaluation_text}")
            
            # For now, return mock structured response
            # In production, you would properly parse the JSON response
            specialty_score = 8 if specialty == "tech_depth" else 7
            other_scores = {criterion: 7 if criterion != specialty else specialty_score for criterion in CRITERIA.keys()}
            
            return {
                "scores": other_scores,
                "explanation": f"Evaluation by {judge_info['name']}: {evaluation_text}",
                "confidence": 0.85
            }
            
        except Exception as e:
            logger.error(f"Error in specialized evaluation by {judge_id}: {str(e)}")
            # Return fallback scores
            fallback_scores = {criterion: 6 for criterion in CRITERIA.keys()}
            return {
                "scores": fallback_scores,
                "explanation": f"Error in evaluation by {judge_info['name']}: {str(e)}",
                "confidence": 0.6
            }

    def evaluate_submission(self, submission_text: str, team_id: str = None) -> Dict[str, Any]:
        """
        Evaluate a submission using all three specialized judge agents.
        
        Args:
            submission_text: The submission text to evaluate
            team_id: Optional team ID for logging
            
        Returns:
            Dictionary with individual scores, consensus score, and reasoning
        """
        logger.info(f"Multi-agent evaluation started for team {team_id}")
        
        # Collect evaluations from all judges
        individual_evaluations = {}
        for judge_id in self.judges.keys():
            evaluation = self._get_specialized_evaluation(judge_id, submission_text)
            individual_evaluations[judge_id] = {
                "judge_info": self.judges[judge_id],
                "evaluation": evaluation
            }
        
        # Calculate consensus scores
        consensus_scores = self._calculate_consensus_scores(individual_evaluations)
        
        # Create result
        result = {
            "team_id": team_id,
            "individual_scores": individual_evaluations,
            "consensus_scores": consensus_scores,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        
        logger.info(f"Multi-agent evaluation completed for team {team_id}")
        return result

    def _calculate_consensus_scores(self, individual_evaluations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate consensus scores from individual judge evaluations.
        
        Args:
            individual_evaluations: Dictionary with evaluations from all judges
            
        Returns:
            Dictionary with consensus scores and reasoning
        """
        # Collect scores for each criterion
        criterion_scores = {criterion: [] for criterion in CRITERIA.keys()}
        
        for judge_id, eval_data in individual_evaluations.items():
            eval_scores = eval_data["evaluation"]["scores"]
            for criterion, score in eval_scores.items():
                if criterion in criterion_scores:
                    criterion_scores[criterion].append(score)
        
        # Calculate weighted average for each criterion
        final_scores = {}
        total_weighted_score = 0
        total_max_score = 0
        
        for criterion, scores in criterion_scores.items():
            # Calculate average of all judge scores for this criterion
            avg_score = sum(scores) / len(scores) if scores else 0
            final_scores[criterion] = round(avg_score, 2)
            
            # Calculate weighted contribution
            weight = WEIGHTS[criterion]
            weighted_contribution = avg_score * weight
            total_weighted_score += weighted_contribution
            total_max_score += CRITERIA[criterion] * weight
        
        # Calculate overall consensus score (normalized to 100)
        consensus_score = (total_weighted_score / total_max_score) * 100 if total_max_score > 0 else 0
        
        return {
            "criteria": final_scores,
            "overall_score": round(consensus_score, 2),
            "max_possible_score": total_max_score * 100,
            "reasoning_chain": "Weighted average of all three judge agents' scores"
        }


def evaluate_submission_multi_agent(payload: dict) -> dict:
    """
    Public function to evaluate a submission using multi-agent system.
    
    Args:
        payload: Dictionary containing submission_text and optional team_id
        
    Returns:
        Dictionary with individual scores, consensus score, and reasoning
    """
    # Initialize the multi-agent judging system
    multi_agent_judge = MultiAgentJudge()
    
    # Extract data from payload
    submission_text = payload.get("submission_text", "")
    team_id = payload.get("team_id")
    
    # Evaluate the submission
    result = multi_agent_judge.evaluate_submission(submission_text, team_id)
    
    # Format the response as requested
    return {
        "individual_scores": {
            judge_id: {
                "judge_name": eval_data["judge_info"]["name"],
                "specialty": eval_data["judge_info"]["specialty"],
                "scores": eval_data["evaluation"]["scores"],
                "explanation": eval_data["evaluation"]["explanation"],
                "confidence": eval_data["evaluation"]["confidence"]
            }
            for judge_id, eval_data in result["individual_scores"].items()
        },
        "consensus_score": result["consensus_scores"]["overall_score"],
        "criteria_scores": result["consensus_scores"]["criteria"],
        "reasoning_chain": result["consensus_scores"]["reasoning_chain"],
        "timestamp": result["timestamp"]
    }