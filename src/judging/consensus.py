"""
Consensus Aggregation Logic
Handles the aggregation of multiple judge scores into a final consensus score
"""
from typing import Dict, Any, List
from .rubric import CRITERIA, WEIGHTS
import logging

logger = logging.getLogger(__name__)

class ConsensusAggregator:
    def __init__(self):
        """
        Initialize the consensus aggregator.
        """
        pass

    def calculate_weighted_average(self, scores: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Calculate the weighted average of multiple score sets.
        
        Args:
            scores: List of dictionaries containing scores for each criterion
            
        Returns:
            Dictionary with consensus scores and reasoning
        """
        if not scores:
            return {
                "criteria": {criterion: 0 for criterion in CRITERIA.keys()},
                "overall_score": 0,
                "reasoning": "No scores provided for aggregation"
            }
        
        # Initialize aggregated scores
        aggregated_scores = {criterion: [] for criterion in CRITERIA.keys()}
        
        # Collect all scores for each criterion
        for score_set in scores:
            for criterion in CRITERIA.keys():
                if criterion in score_set:
                    aggregated_scores[criterion].append(score_set[criterion])
        
        # Calculate average for each criterion
        consensus_scores = {}
        total_weighted_score = 0
        total_max_score = 0
        
        for criterion, score_list in aggregated_scores.items():
            if score_list:  # If there are scores for this criterion
                avg_score = sum(score_list) / len(score_list)
                consensus_scores[criterion] = round(avg_score, 2)
                
                # Calculate weighted contribution
                weight = WEIGHTS[criterion]
                weighted_contribution = avg_score * weight
                total_weighted_score += weighted_contribution
                total_max_score += CRITERIA[criterion] * weight
            else:
                # If no scores for this criterion, set to 0
                consensus_scores[criterion] = 0
        
        # Calculate overall consensus score (normalized to 100)
        overall_score = (total_weighted_score / total_max_score) * 100 if total_max_score > 0 else 0
        
        return {
            "criteria": consensus_scores,
            "overall_score": round(overall_score, 2),
            "reasoning": f"Weighted average of {len(scores)} individual scores",
            "individual_count": len(scores)
        }

    def calculate_consensus_with_confidence(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate consensus taking into account confidence scores of each evaluation.
        
        Args:
            evaluations: List of evaluation dictionaries that include scores and confidence
            
        Returns:
            Dictionary with consensus scores, confidence-adjusted reasoning
        """
        if not evaluations:
            return {
                "criteria": {criterion: 0 for criterion in CRITERIA.keys()},
                "overall_score": 0,
                "confidence": 0,
                "reasoning": "No evaluations provided for aggregation"
            }
        
        # Collect scores and confidence values
        scores = []
        confidences = []
        
        for eval_data in evaluations:
            if "scores" in eval_data and "confidence" in eval_data:
                scores.append(eval_data["scores"])
                confidences.append(eval_data["confidence"])
        
        if not scores:
            return {
                "criteria": {criterion: 0 for criterion in CRITERIA.keys()},
                "overall_score": 0,
                "confidence": 0,
                "reasoning": "No valid scores found in evaluations"
            }
        
        # Calculate weighted average considering confidence
        consensus_result = self.calculate_weighted_average(scores)
        
        # Calculate average confidence
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            **consensus_result,
            "confidence": round(avg_confidence, 2),
            "reasoning": f"Weighted average of {len(scores)} evaluations with confidence adjustment"
        }

    def calculate_disagreement_metrics(self, scores: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Calculate metrics to measure disagreement between judges.
        
        Args:
            scores: List of score dictionaries
            
        Returns:
            Dictionary with disagreement metrics
        """
        if not scores or len(scores) < 2:
            return {
                "disagreement_score": 0,
                "notes": "Insufficient scores to calculate disagreement metrics"
            }
        
        disagreement_metrics = {}
        
        for criterion in CRITERIA.keys():
            criterion_scores = [score_set.get(criterion, 0) for score_set in scores if criterion in score_set]
            
            if len(criterion_scores) > 1:
                # Calculate standard deviation as a measure of disagreement
                mean_score = sum(criterion_scores) / len(criterion_scores)
                variance = sum((score - mean_score) ** 2 for score in criterion_scores) / len(criterion_scores)
                std_dev = variance ** 0.5
                
                disagreement_metrics[criterion] = {
                    "std_deviation": round(std_dev, 2),
                    "range": round(max(criterion_scores) - min(criterion_scores), 2),
                    "coefficient_of_variation": round(std_dev / mean_score if mean_score != 0 else 0, 2)
                }
            else:
                disagreement_metrics[criterion] = {
                    "std_deviation": 0,
                    "range": 0,
                    "coefficient_of_variation": 0
                }
        
        # Overall disagreement score (average of std deviations)
        overall_disagreement = sum(
            metrics["std_deviation"] for metrics in disagreement_metrics.values()
        ) / len(disagreement_metrics) if disagreement_metrics else 0
        
        return {
            "criterion_metrics": disagreement_metrics,
            "disagreement_score": round(overall_disagreement, 2),
            "notes": f"Calculated from {len(scores)} score sets"
        }


def aggregate_consensus(evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Public function to aggregate multiple evaluations into a consensus.
    
    Args:
        evaluations: List of evaluation dictionaries containing scores and confidence
        
    Returns:
        Dictionary with consensus scores, confidence, and reasoning
    """
    aggregator = ConsensusAggregator()
    
    # Calculate consensus with confidence
    consensus_result = aggregator.calculate_consensus_with_confidence(evaluations)
    
    # Calculate disagreement metrics
    scores_only = [eval_data["scores"] for eval_data in evaluations if "scores" in eval_data]
    disagreement_metrics = aggregator.calculate_disagreement_metrics(scores_only)
    
    # Combine results
    result = {
        **consensus_result,
        "disagreement_metrics": disagreement_metrics
    }
    
    return result