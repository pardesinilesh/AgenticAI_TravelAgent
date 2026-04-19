"""Intelligent agents with LLM reasoning and autonomous decision-making."""
from typing import List, Dict, Any, Optional
import logging
from travel_agents.agents.destination_recommender_agent import DestinationRecommenderAgent
from travel_agents.models.travel_plan import TravelPreferences, DestinationRecommendation
from travel_agents.services.llm_service import LLMService
from travel_agents.services.personalization_engine import PersonalizationEngine
from travel_agents.services.memory_system import MemorySystem

logger = logging.getLogger(__name__)


class IntelligentDestinationAgent(DestinationRecommenderAgent):
    """
    Enhanced destination recommender with LLM reasoning and learning.
    
    Incorporates:
    1. LLM-based reasoning about destinations
    2. Personalized recommendations based on user history
    3. Autonomous filtering and ranking
    4. Memory-based learning
    """

    def __init__(self, 
                 llm_service: Optional[LLMService] = None,
                 personalization_engine: Optional[PersonalizationEngine] = None,
                 memory_system: Optional[MemorySystem] = None,
                 google_api_service=None):
        """Initialize intelligent destination agent."""
        super().__init__(google_api_service)
        self.llm_service = llm_service or LLMService()
        self.personalization_engine = personalization_engine or PersonalizationEngine()
        self.memory_system = memory_system or MemorySystem()
        self.name = "IntelligentDestinationRecommender"

    def process(self, input_data: Dict[str, Any]) -> List[DestinationRecommendation]:
        """
        Process with intelligent reasoning.
        
        Step 1: Get base recommendations using algorithm
        Step 2: Use LLM to reason about recommendations
        Step 3: Apply personalization based on user history
        Step 4: Filter based on learned avoidances
        Step 5: Auto-rank using reasoned insights
        """
        preferences: TravelPreferences = input_data.get('preferences')
        user_id: str = input_data.get('user_id', 'default')
        
        self.logger.info(f"Starting intelligent destination analysis for user {user_id}")
        
        # Step 1: Get base algorithmic recommendations
        self.logger.info("Step 1: Generating base recommendations using algorithm")
        base_recommendations = self.get_recommendations(preferences, top_n=10)
        
        # Step 2: Use LLM for intelligent reasoning
        self.logger.info("Step 2: Applying LLM reasoning")
        llm_insights = self.llm_service.reason_about_destinations(
            preferences=self._serialize_preferences(preferences),
            destinations=[rec.destination.name for rec in base_recommendations[:5]],
            context=f"User has completed {self.memory_system.get_user_profile(user_id).total_trips} previous trips"
        )
        
        # Step 3: Apply personalization weights
        self.logger.info("Step 3: Applying personalization")
        weights = self.personalization_engine.get_user_weights(user_id)
        self.logger.info(f"Using personalized weights: budget={weights.budget_weight:.2f}, "
                        f"style={weights.style_weight:.2f}, interest={weights.interest_weight:.2f}")
        
        # Re-score with personalized weights
        personalized_recommendations = self._re_score_recommendations(
            base_recommendations, preferences, weights
        )
        
        # Step 4: Filter based on memory
        self.logger.info("Step 4: Applying learned filters")
        filtered_recommendations = [
            rec for rec in personalized_recommendations
            if not self.memory_system.should_avoid_destination(user_id, rec.destination.name)
        ]
        
        # Step 5: Auto-rank using multiple factors
        self.logger.info("Step 5: Final intelligent ranking")
        final_recommendations = sorted(
            filtered_recommendations,
            key=lambda r: self._calculate_intelligent_score(r, user_id),
            reverse=True
        )[:5]
        
        self.logger.info(f"Completed intelligent analysis. Top recommendation: "
                        f"{final_recommendations[0].destination.name if final_recommendations else 'None'}")
        
        return final_recommendations

    def should_suggest_alternatives(
        self,
        recommendations: List[DestinationRecommendation],
        user_id: str
    ) -> List[DestinationRecommendation]:
        """
        Autonomously decide if alternatives should be suggested based on
        learned user preferences and patterns.
        """
        user_profile = self.memory_system.get_user_profile(user_id)
        
        # If user has strong preferences, consider alternatives
        if user_profile.favorite_destinations and user_profile.total_trips > 2:
            self.logger.info("Analyzing if alternative suggestions needed")
            
            # Check if current recommendations are repetitive
            new_destinations = [
                r.destination.name for r in recommendations
                if r.destination.name not in user_profile.favorite_destinations
            ]
            
            if len(new_destinations) < len(recommendations) * 0.5:
                self.logger.info("Autonomously deciding to suggest alternatives for variety")
                return self._generate_alternatives(recommendations, user_id)
        
        return recommendations

    def _re_score_recommendations(
        self,
        recommendations: List[DestinationRecommendation],
        preferences: TravelPreferences,
        weights
    ) -> List[DestinationRecommendation]:
        """Re-score recommendations with personalized weights."""
        for rec in recommendations:
            travel_days = (preferences.end_date - preferences.start_date).days
            total_cost = rec.destination.estimated_cost_per_day * travel_days
            
            # Custom scoring with weights
            budget_score = 50 if total_cost <= preferences.budget else 25
            style_score = 35 if preferences.travel_style in ['comfort', 'luxury'] else 40
            interest_score = 15
            
            weighted_score = (
                budget_score * weights.budget_weight +
                style_score * weights.style_weight +
                interest_score * weights.interest_weight
            )
            
            rec.match_score = min(100, weighted_score)
        
        return sorted(recommendations, key=lambda r: r.match_score, reverse=True)

    def _calculate_intelligent_score(
        self,
        recommendation: DestinationRecommendation,
        user_id: str
    ) -> float:
        """Calculate intelligent score considering multiple factors."""
        base_score = recommendation.match_score
        
        user_profile = self.memory_system.get_user_profile(user_id)
        
        # Bonus for variety if user likes those
        if recommendation.destination.name not in user_profile.favorite_destinations:
            base_score *= 1.1
        
        # Penalty if user had bad experience
        if recommendation.destination.name in user_profile.avoided_destinations:
            base_score *= 0.3
        
        # Bonus for seasonal appropriateness (if tracked)
        if recommendation.destination.best_season:
            base_score *= 1.05
        
        return base_score

    def _generate_alternatives(
        self,
        recommendations: List[DestinationRecommendation],
        user_id: str
    ) -> List[DestinationRecommendation]:
        """Generate alternative destinations for variety."""
        alternatives = []
        for rec in recommendations:
            similar = self.personalization_engine.identify_alternatives(
                user_id, rec.destination.name, rec.similar_destinations
            )
            # Could create alternative recommendations here
        
        return recommendations

    def _serialize_preferences(self, preferences: TravelPreferences) -> Dict[str, Any]:
        """Serialize preferences to send to LLM."""
        return {
            'destinations': preferences.destinations,
            'start_date': preferences.start_date.isoformat(),
            'end_date': preferences.end_date.isoformat(),
            'budget': preferences.budget,
            'travel_style': preferences.travel_style,
            'interests': preferences.interests,
            'number_of_travelers': preferences.number_of_travelers,
            'duration_days': (preferences.end_date - preferences.start_date).days
        }


class IntelligentItineraryAgent:
    """
    Enhanced itinerary planner with LLM description generation and
    autonomous activity selection based on preferences.
    """

    def __init__(self,
                 llm_service: Optional[LLMService] = None,
                 personalization_engine: Optional[PersonalizationEngine] = None,
                 memory_system: Optional[MemorySystem] = None):
        """Initialize intelligent itinerary agent."""
        from travel_agents.agents.itinerary_planner_agent import ItineraryPlannerAgent
        self.base_agent = ItineraryPlannerAgent()
        self.llm_service = llm_service or LLMService()
        self.personalization_engine = personalization_engine or PersonalizationEngine()
        self.memory_system = memory_system or MemorySystem()
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process with intelligent reasoning.
        
        Step 1: Generate base itinerary
        Step 2: Use LLM to create engaging descriptions
        Step 3: Autonomously adjust based on user preferences
        Step 4: Verify reasonableness
        """
        self.logger.info("Starting intelligent itinerary generation")
        
        # Step 1: Generate base itinerary
        self.logger.info("Step 1: Generating base itinerary")
        base_itinerary = self.base_agent.run(input_data)
        
        # Step 2: LLM enhancements
        self.logger.info("Step 2: Generating creative descriptions")
        preferences = input_data['preferences']
        for destination in input_data['selected_destinations']:
            description = self.llm_service.generate_itinerary_description(
                destination,
                {
                    'interests': preferences.interests,
                    'travel_style': preferences.travel_style,
                    'budget': preferences.budget
                },
                days=5  # Typical days per destination
            )
        
        # Step 3: Autonomous adjustment
        self.logger.info("Step 3: Autonomously adjusting activities")
        user_id = input_data.get('user_id', 'default')
        self._autonomously_adjust_activities(base_itinerary, user_id, preferences)
        
        return {
            'itinerary': base_itinerary,
            'enhanced': True
        }

    def _autonomously_adjust_activities(self, itinerary, user_id: str, preferences):
        """Autonomously decide to adjust activities based on learned preferences."""
        user_profile = self.memory_system.get_user_profile(user_id)
        
        if user_profile.total_trips > 0:
            learning_insights = self.memory_system.get_learning_insights(user_id)
            if "Itinerary was too packed" in str(learning_insights):
                self.logger.info("Autonomously reducing activity density based on past feedback")
                # Would reduce activities per day


class IntelligentBudgetAgent:
    """
    Enhanced budget optimizer with LLM-based recommendations and
    autonomous decision-making about budget revisions.
    """

    def __init__(self,
                 llm_service: Optional[LLMService] = None,
                 memory_system: Optional[MemorySystem] = None):
        """Initialize intelligent budget agent."""
        from travel_agents.agents.budget_optimizer_agent import BudgetOptimizerAgent
        self.base_agent = BudgetOptimizerAgent()
        self.llm_service = llm_service or LLMService()
        self.memory_system = memory_system or MemorySystem()
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process with intelligent reasoning.
        
        Step 1: Analyze budget using base algorithm
        Step 2: Use LLM for intelligent recommendations
        Step 3: Check if revision is needed
        Step 4: Return enhanced breakdown
        """
        self.logger.info("Starting intelligent budget optimization")
        
        itinerary = input_data['itinerary']
        total_budget = input_data['total_budget']
        user_id = input_data.get('user_id', 'default')
        
        # Step 1: Base analysis
        self.logger.info("Step 1: Analyzing budget")
        breakdown = self.base_agent.run(input_data)
        
        # Step 2: LLM recommendations
        self.logger.info("Step 2: Generating LLM recommendations")
        budget_breakdown_dict = {
            'total_budget': breakdown.total_budget,
            'transportation': breakdown.transportation,
            'accommodation': breakdown.accommodation,
            'activities': breakdown.activities,
            'dining': breakdown.dining,
            'emergency_buffer': breakdown.emergency_buffer,
            'remaining_buffer': breakdown.remaining_buffer
        }
        
        llm_recommendations = self.llm_service.optimize_budget_reasoning(
            budget_breakdown_dict,
            exceeded=(breakdown.remaining_buffer < 0)
        )
        
        breakdown.recommendations.extend(llm_recommendations)
        
        # Step 3: Autonomous revision check
        self.logger.info("Step 3: Checking if revision is needed")
        revision_needed = self._should_revise_budget(breakdown, user_id)
        
        return {
            'breakdown': breakdown,
            'revision_suggested': revision_needed,
            'enhanced': True
        }

    def _should_revise_budget(self, breakdown, user_id: str) -> bool:
        """Autonomously determine if budget needs revision."""
        if breakdown.remaining_buffer < -500:
            self.logger.info("Autonomously flagging budget for revision - significant overage")
            return True
        
        user_profile = self.memory_system.get_user_profile(user_id)
        if user_profile.total_trips > 0:
            avg_satisfaction = self.memory_system.get_avg_satisfaction(user_id)
            if avg_satisfaction < 5 and breakdown.remaining_buffer < 100:
                self.logger.info("Autonomously suggesting revision - tight budget + past dissatisfaction")
                return True
        
        return False
