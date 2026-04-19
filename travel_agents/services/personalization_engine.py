"""Machine learning personalization system."""
from typing import Dict, List, Any, Tuple
import logging
from dataclasses import dataclass
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PreferenceWeights:
    """Learnable preference weights."""
    budget_weight: float = 0.35
    style_weight: float = 0.33
    interest_weight: float = 0.32
    season_weight: float = 0.0
    distance_weight: float = 0.0


class PersonalizationEngine:
    """ML-based personalization engine for learning user preferences."""

    def __init__(self):
        """Initialize personalization engine."""
        self.user_weights: Dict[str, PreferenceWeights] = {}
        self.learning_rate = 0.05
        logger.info("Personalization engine initialized")

    def get_user_weights(self, user_id: str) -> PreferenceWeights:
        """Get or create personalization weights for user."""
        if user_id not in self.user_weights:
            self.user_weights[user_id] = PreferenceWeights()
        return self.user_weights[user_id]

    def learn_from_feedback(
        self,
        user_id: str,
        satisfaction_score: float,
        trip_characteristics: Dict[str, Any]
    ) -> PreferenceWeights:
        """
        Learn from trip feedback and adjust weights.
        
        Args:
            user_id: User identifier
            satisfaction_score: User satisfaction (0-10)
            trip_characteristics: Characteristics of the trip
            
        Returns:
            Updated preference weights
        """
        weights = self.get_user_weights(user_id)
        normalized_score = satisfaction_score / 10.0  # Normalize to 0-1
        
        # Adjust weights based on trip characteristics and satisfaction
        if trip_characteristics.get('budget_respected', False):
            if normalized_score > 0.8:
                # Budget handling contributed to satisfaction
                weights.budget_weight = min(0.5, weights.budget_weight + self.learning_rate)
        
        if trip_characteristics.get('style_matched', False):
            if normalized_score > 0.8:
                weights.style_weight = min(0.5, weights.style_weight + self.learning_rate)
        
        if trip_characteristics.get('interests_aligned', False):
            if normalized_score > 0.8:
                weights.interest_weight = min(0.5, weights.interest_weight + self.learning_rate)
        
        # Normalize weights
        total = weights.budget_weight + weights.style_weight + weights.interest_weight
        if total > 0:
            weights.budget_weight /= total
            weights.style_weight /= total
            weights.interest_weight /= total
        
        logger.info(f"Learned weights for user {user_id}: {weights}")
        return weights

    def predict_satisfaction(
        self,
        user_id: str,
        trip_plan: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None
    ) -> Tuple[float, List[str]]:
        """
        Predict satisfaction score for a trip plan.
        
        Args:
            user_id: User identifier
            trip_plan: Proposed trip plan
            historical_data: Historical trip data for comparison
            
        Returns:
            Tuple of (predicted_score, improvement_suggestions)
        """
        weights = self.get_user_weights(user_id)
        
        budget_aspect = self._evaluate_budget_aspect(trip_plan, weights)
        style_aspect = self._evaluate_style_aspect(trip_plan, weights)
        interest_aspect = self._evaluate_interest_aspect(trip_plan, weights)
        
        # Calculate weighted score
        predicted_score = (
            budget_aspect * weights.budget_weight +
            style_aspect * weights.style_weight +
            interest_aspect * weights.interest_weight
        )
        
        # Normalize to 0-10 scale
        predicted_score = max(0, min(10, predicted_score * 10))
        
        # Generate improvement suggestions
        suggestions = []
        
        if budget_aspect < 0.7:
            suggestions.append("Consider adjusting budget allocation for better value")
        if style_aspect < 0.7:
            suggestions.append("Better alignment with your travel style could improve experience")
        if interest_aspect < 0.7:
            suggestions.append("Adding activities aligned with your interests may increase satisfaction")
        
        logger.info(f"Predicted satisfaction for user {user_id}: {predicted_score:.1f}/10")
        
        return predicted_score, suggestions

    def recommend_adjustments(
        self,
        user_id: str,
        trip_plan: Dict[str, Any],
        constraints: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Recommend adjustments to trip plan based on learned preferences.
        
        Args:
            user_id: User identifier
            trip_plan: Current trip plan
            constraints: Any constraints on adjustments
            
        Returns:
            Dictionary of recommended adjustments
        """
        weights = self.get_user_weights(user_id)
        constraints = constraints or {}
        
        recommendations = {
            'budget_adjustments': [],
            'itinerary_adjustments': [],
            'activity_adjustments': []
        }
        
        # Analyze and recommend
        budget_breakdown = trip_plan.get('budget_breakdown', {})
        
        # Check if budget allocation matches preferences
        if weights.budget_weight > 0.4:
            # User emphasizes budget - suggest cost reductions
            if budget_breakdown.get('accommodation', 0) > trip_plan.get('preferences', {}).get('budget', 0) * 0.45:
                recommendations['budget_adjustments'].append(
                    "Consider more budget-friendly accommodation to align with your preferences"
                )
        
        return recommendations

    def identify_alternatives(
        self,
        user_id: str,
        current_destination: str,
        similar_destinations: List[str]
    ) -> List[Tuple[str, float]]:
        """
        Identify alternative destinations based on learned preferences.
        
        Args:
            user_id: User identifier
            current_destination: Currently selected destination
            similar_destinations: List of similar destinations
            
        Returns:
            Ranked list of alternatives with compatibility scores
        """
        weights = self.get_user_weights(user_id)
        
        # Score each alternative (simplified - would normally use more factors)
        scored_alternatives = []
        for dest in similar_destinations:
            # This is a simplified scoring - in production would use more data
            score = 0.5 + (weights.interest_weight * 0.2) + (weights.style_weight * 0.2)
            scored_alternatives.append((dest, score))
        
        # Sort by score
        scored_alternatives.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"Identified alternatives for {user_id}: {scored_alternatives}")
        
        return scored_alternatives

    def _evaluate_budget_aspect(self, trip_plan: Dict[str, Any], weights: PreferenceWeights) -> float:
        """Evaluate budget aspect (0-1 score)."""
        budget_breakdown = trip_plan.get('budget_breakdown', {})
        total_budget = budget_breakdown.get('total_budget', 0)
        remaining = budget_breakdown.get('remaining_buffer', 0)
        
        if total_budget == 0:
            return 0.5
        
        # Higher score if budget utilization is healthy (not too tight, not too loose)
        utilization_ratio = (total_budget - remaining) / total_budget
        
        if 0.7 <= utilization_ratio <= 0.95:
            return 1.0
        elif 0.6 <= utilization_ratio <= 1.0:
            return 0.8
        elif 0.5 <= utilization_ratio <= 1.1:
            return 0.6
        else:
            return 0.3

    def _evaluate_style_aspect(self, trip_plan: Dict[str, Any], weights: PreferenceWeights) -> float:
        """Evaluate travel style alignment (0-1 score)."""
        preferences = trip_plan.get('preferences', {})
        recommendations = trip_plan.get('destination_recommendations', [])
        
        if not recommendations:
            return 0.5
        
        # Check if top recommendations match travel style
        travel_style = preferences.get('travel_style', 'comfort')
        high_match_count = sum(1 for r in recommendations[:3] if r.get('match_score', 0) > 80)
        
        return min(1.0, high_match_count / 3.0)

    def _evaluate_interest_aspect(self, trip_plan: Dict[str, Any], weights: PreferenceWeights) -> float:
        """Evaluate interest alignment (0-1 score)."""
        preferences = trip_plan.get('preferences', {})
        interests = preferences.get('interests', [])
        recommendations = trip_plan.get('destination_recommendations', [])
        
        if not interests or not recommendations:
            return 0.5
        
        # Check if recommendations mention user interests
        interest_matches = 0
        for rec in recommendations[:3]:
            reasons = rec.get('reasons', [])
            for reason in reasons:
                for interest in interests:
                    if interest.lower() in reason.lower():
                        interest_matches += 1
                        break
        
        return min(1.0, interest_matches / len(interests))

    def get_personalization_metrics(self, user_id: str) -> Dict[str, Any]:
        """Get current personalization metrics for a user."""
        weights = self.get_user_weights(user_id)
        
        return {
            'user_id': user_id,
            'weights': {
                'budget': weights.budget_weight,
                'style': weights.style_weight,
                'interest': weights.interest_weight,
                'season': weights.season_weight,
                'distance': weights.distance_weight
            },
            'timestamp': datetime.now().isoformat()
        }

    def reset_weights(self, user_id: str) -> None:
        """Reset weights to defaults for a user."""
        self.user_weights[user_id] = PreferenceWeights()
        logger.info(f"Weights reset for user {user_id}")
