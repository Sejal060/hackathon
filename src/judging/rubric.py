"""
Rubric schema for AI judging system
Defines criteria and weights for competition-grade judging
"""

# Define the rubric criteria with maximum scores
CRITERIA = {
    "usefulness": 10,      # Maximum score of 10
    "innovation": 10,      # Maximum score of 10
    "tech_depth": 10,      # Maximum score of 10
    "clarity": 10,         # Maximum score of 10
    "impact": 10           # Maximum score of 10
}

# Define weights for each criterion (should sum to 1.0 for proper weighting)
WEIGHTS = {
    "usefulness": 0.2,
    "innovation": 0.25,
    "tech_depth": 0.25,
    "clarity": 0.15,
    "impact": 0.15
}

# Validate that weights sum to 1.0
def validate_weights():
    total_weight = sum(WEIGHTS.values())
    if abs(total_weight - 1.0) > 0.001:  # Allow for floating point precision errors
        raise ValueError(f"Weights must sum to 1.0, but sum to {total_weight}")
    return True

# Run validation on import
validate_weights()

# Get total possible score
TOTAL_POSSIBLE_SCORE = sum(CRITERIA.values())

def get_criteria_names():
    """Return list of all criteria names"""
    return list(CRITERIA.keys())

def get_max_score_for_criterion(criterion):
    """Get the maximum possible score for a given criterion"""
    return CRITERIA.get(criterion, 0)

def get_weight_for_criterion(criterion):
    """Get the weight for a given criterion"""
    return WEIGHTS.get(criterion, 0)