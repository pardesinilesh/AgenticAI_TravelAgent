"""Enhanced orchestrator with AI reasoning, memory, and personalization."""
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging
import json

from travel_agents.models.travel_plan import TravelPreferences
from travel_agents.agents.intelligent_agents import (
    IntelligentDestinationAgent,
    IntelligentItineraryAgent,
    IntelligentBudgetAgent
)
from travel_agents.services.google_api_service import GoogleAPIService
from travel_agents.services.llm_service import LLMService
from travel_agents.services.personalization_engine import PersonalizationEngine
from travel_agents.services.memory_system import MemorySystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntelligentTravelOrchestrator:
    """
    Enhanced travel planning orchestrator with:
    1. LLM-based reasoning
    2. Machine learning personalization
    3. Memory and user context
    4. Multi-step reasoning chains
    5. Autonomous decision-making
    """

    def __init__(self,
                 use_google_api: bool = True,
                 use_llm: bool = True,
                 user_id: str = "default"):
        """
        Initialize intelligent orchestrator.
        
        Args:
            use_google_api: Enable Google Maps API
            use_llm: Enable LLM reasoning
            user_id: Unique user identifier for personalization and memory
        """
        self.user_id = user_id
        self.use_llm = use_llm
        
        # Initialize services
        self.google_api_service = None
        if use_google_api:
            try:
                self.google_api_service = GoogleAPIService()
            except ValueError:
                logger.warning("Google API key not found.")
        
        self.llm_service = LLMService() if use_llm else None
        self.personalization_engine = PersonalizationEngine()
        self.memory_system = MemorySystem()
        
        # Initialize intelligent agents
        self.destination_agent = IntelligentDestinationAgent(
            llm_service=self.llm_service,
            personalization_engine=self.personalization_engine,
            memory_system=self.memory_system,
            google_api_service=self.google_api_service
        )
        
        self.itinerary_agent = IntelligentItineraryAgent(
            llm_service=self.llm_service,
            personalization_engine=self.personalization_engine,
            memory_system=self.memory_system
        )
        
        self.budget_agent = IntelligentBudgetAgent(
            llm_service=self.llm_service,
            memory_system=self.memory_system
        )
        
        logger.info(f"Intelligent Travel Orchestrator initialized for user: {user_id}")

    def plan_trip(
        self,
        destinations: List[str],
        start_date: date,
        end_date: date,
        budget: float,
        travel_style: str,
        interests: List[str],
        number_of_travelers: int = 1,
        user_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Plan trip using intelligent multi-step reasoning.
        
        Args:
            destinations: List of desired destinations
            start_date: Trip start date
            end_date: Trip end date
            budget: Total budget
            travel_style: Travel style preference
            interests: List of interests
            number_of_travelers: Number of travelers
            user_feedback: Optional feedback for autonomous decisions
            
        Returns:
            Complete intelligent trip plan
        """
        logger.info("=" * 80)
        logger.info("🤖 STARTING INTELLIGENT TRIP PLANNING")
        logger.info("=" * 80)
        
        # Create preferences
        preferences = TravelPreferences(
            destinations=destinations,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            travel_style=travel_style,
            interests=interests,
            number_of_travelers=number_of_travelers
        )
        
        # Start intelligent reasoning chain
        logger.info("\n" + "=" * 80)
        logger.info("STEP 1: DESTINATION RECOMMENDATION WITH AI REASONING")
        logger.info("=" * 80)
        
        recommendations = self.destination_agent.process({
            'preferences': preferences,
            'user_id': self.user_id
        })
        
        selected_destinations = [
            rec.destination.name for rec in recommendations[:min(3, len(recommendations))]
        ]
        logger.info(f"Selected destinations: {', '.join(selected_destinations)}")
        
        # Check for autonomous alternative suggestions
        alternatives_considered = self.destination_agent.should_suggest_alternatives(
            recommendations, self.user_id
        )
        if len(alternatives_considered) > len(recommendations):
            logger.info("✓ Autonomously considered alternative destinations for variety")
        
        # Step 2: Generate itinerary
        logger.info("\n" + "=" * 80)
        logger.info("STEP 2: INTELLIGENT ITINERARY PLANNING")
        logger.info("=" * 80)
        
        itinerary_result = self.itinerary_agent.process({
            'preferences': preferences,
            'selected_destinations': selected_destinations,
            'user_id': self.user_id
        })
        itinerary = itinerary_result['itinerary']
        
        if itinerary_result.get('enhanced'):
            logger.info("✓ Itinerary enhanced with LLM-generated descriptions")
        
        # Step 3: Optimize budget
        logger.info("\n" + "=" * 80)
        logger.info("STEP 3: INTELLIGENT BUDGET OPTIMIZATION")
        logger.info("=" * 80)
        
        budget_result = self.budget_agent.process({
            'itinerary': itinerary,
            'total_budget': budget,
            'user_id': self.user_id
        })
        budget_breakdown = budget_result['breakdown']
        
        if budget_result.get('revision_suggested'):
            logger.info("⚠ Autonomously flagged for budget revision")
        
        # Step 4: Generate AI insights
        logger.info("\n" + "=" * 80)
        logger.info("STEP 4: AI-POWERED INSIGHTS AND EVALUATION")
        logger.info("=" * 80)
        
        satisfaction_prediction, improvements = self.personalization_engine.predict_satisfaction(
            self.user_id, self._compile_plan(preferences, recommendations, itinerary, budget_breakdown)
        )
        logger.info(f"Predicted satisfaction score: {satisfaction_prediction:.1f}/10")
        if improvements:
            logger.info(f"Suggested improvements: {improvements[0]}")
        
        # Step 5: Autonomous decision-making
        logger.info("\n" + "=" * 80)
        logger.info("STEP 5: AUTONOMOUS DECISION ANALYSIS")
        logger.info("=" * 80)
        
        autonomous_decisions = self._make_autonomous_decisions(
            preferences, recommendations, itinerary, budget_breakdown
        )
        
        if autonomous_decisions['auto_actions']:
            logger.info("Autonomous actions taken:")
            for action in autonomous_decisions['auto_actions']:
                logger.info(f"  ✓ {action}")
        
        # Step 6: Generate travel tips with LLM
        logger.info("\n" + "=" * 80)
        logger.info("STEP 6: GENERATING PERSONALIZED TRAVEL TIPS")
        logger.info("=" * 80)
        
        travel_tips = ""
        if self.llm_service and self.llm_service.enabled:
            travel_tips = self.llm_service.generate_travel_tips(
                selected_destinations,
                {
                    'travel_style': travel_style,
                    'interests': interests,
                    'duration_days': (end_date - start_date).days,
                    'budget': budget
                }
            )
            logger.info("✓ Personalized travel tips generated")
        
        # Compile complete plan
        trip_plan = self._compile_plan(preferences, recommendations, itinerary, budget_breakdown)
        trip_plan['autonomous_decisions'] = autonomous_decisions
        trip_plan['ai_insights'] = {
            'predicted_satisfaction': satisfaction_prediction,
            'suggested_improvements': improvements,
            'travel_tips': travel_tips[:500] if travel_tips else "Tips not available"
        }
        trip_plan['personalization_metrics'] = self.personalization_engine.get_personalization_metrics(
            self.user_id
        )
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ INTELLIGENT TRIP PLAN COMPLETE")
        logger.info("=" * 80 + "\n")
        
        return trip_plan

    def record_trip_completion(
        self,
        trip_id: str,
        trip_plan: Dict[str, Any],
        satisfaction_score: float,
        feedback: str = "",
        actual_spend: Optional[float] = None
    ) -> None:
        """
        Record completed trip and learn from feedback.
        
        Args:
            trip_id: Unique trip identifier
            trip_plan: Original trip plan
            satisfaction_score: User satisfaction (0-10)
            feedback: Detailed feedback
            actual_spend: Actual amount spent
        """
        logger.info(f"Recording trip completion: {trip_id}")
        
        # Save to memory
        trip_memory = self.memory_system.save_trip_memory(
            self.user_id,
            trip_id,
            trip_plan,
            satisfaction_score,
            feedback,
            actual_spend
        )
        
        # Update user profile
        updated_profile = self.memory_system.update_user_profile(
            self.user_id,
            trip_memory
        )
        
        # Learn from trip
        trip_characteristics = {
            'budget_respected': actual_spend <= trip_plan.get('budget_breakdown', {}).get('total_budget', float('inf')),
            'style_matched': True,
            'interests_aligned': True
        }
        
        self.personalization_engine.learn_from_feedback(
            self.user_id,
            satisfaction_score,
            trip_characteristics
        )
        
        logger.info(f"✓ Trip learning complete. User now has {updated_profile.total_trips} trips.")

    def _make_autonomous_decisions(
        self,
        preferences: TravelPreferences,
        recommendations: List,
        itinerary,
        budget_breakdown
    ) -> Dict[str, Any]:
        """
        Make autonomous decisions based on trip characteristics.
        
        This is Step 5: Autonomous Decision-Making
        """
        decisions = {
            'auto_actions': [],
            'recommendations': []
        }
        
        # Autonomous decision 1: Check if revision needed
        if self.llm_service and self.llm_service.enabled:
            revision_check = self.llm_service.should_revise_plan(
                self._compile_plan(preferences, recommendations, itinerary, budget_breakdown),
                feedback_score=0.7,
                user_concerns=[]
            )
            
            if revision_check.get('revision_needed'):
                decisions['auto_actions'].append("Plan flagged for revision review")
                decisions['recommendations'].extend(revision_check.get('changes', []))
        
        # Autonomous decision 2: Recommend pace adjustment
        travel_days = (preferences.end_date - preferences.start_date).days
        days_per_destination = travel_days / len([rec.destination.name for rec in recommendations[:3]])
        
        if days_per_destination < 2:
            decisions['auto_actions'].append("Autonomously flagged: High-pace itinerary may be exhausting")
            decisions['recommendations'].append("Consider reducing number of destinations for a more relaxed pace")
        elif days_per_destination > 7:
            decisions['auto_actions'].append("Autonomously detected: Slower, more immersive travel style")
        
        # Autonomous decision 3: Budget health check
        if budget_breakdown.remaining_buffer < 0:
            decisions['auto_actions'].append("Autonomous cost reduction recommendations generated")
        elif budget_breakdown.remaining_buffer > preferences.budget * 0.2:
            decisions['auto_actions'].append("Budget flexibility detected - premium experiences can be added")
        
        return decisions

    def _compile_plan(self, preferences, recommendations, itinerary, budget) -> Dict[str, Any]:
        """Compile complete trip plan."""
        from datetime import timedelta
        
        return {
            'preferences': self._serialize_preferences(preferences),
            'destination_recommendations': self._serialize_recommendations(recommendations),
            'selected_destinations': [rec.destination.name for rec in recommendations[:3]],
            'itinerary': self._serialize_itinerary(itinerary),
            'budget_breakdown': self._serialize_budget_breakdown(budget),
            'summary': self._generate_summary(preferences, recommendations, itinerary, budget),
            'generated_at': datetime.now().isoformat()
        }

    def _serialize_preferences(self, preferences: TravelPreferences) -> Dict:
        """Serialize preferences."""
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

    def _serialize_recommendations(self, recommendations) -> List[Dict]:
        """Serialize recommendations."""
        return [
            {
                'name': rec.destination.name,
                'country': rec.destination.country,
                'match_score': rec.match_score,
                'estimated_daily_cost': rec.estimated_daily_cost,
                'best_days_to_visit': rec.best_days_to_visit,
                'attractions': rec.destination.attractions,
                'reasons': rec.reasons,
                'similar_destinations': rec.similar_destinations
            }
            for rec in recommendations
        ]

    def _serialize_itinerary(self, itinerary) -> Dict:
        """Serialize itinerary."""
        return {
            'destinations': itinerary.destinations,
            'total_duration': itinerary.total_duration,
            'total_estimated_cost': itinerary.total_estimated_cost,
            'transportation_cost': itinerary.transportation_cost,
            'accommodation_cost': itinerary.accommodation_cost,
            'activities_cost': itinerary.activities_cost,
            'dining_cost': itinerary.dining_cost,
            'daily_plans': [
                {
                    'date': day.date.isoformat(),
                    'location': day.location,
                    'activities': [
                        {
                            'name': activity.name,
                            'duration_hours': activity.duration_hours,
                            'estimated_cost': activity.estimated_cost,
                            'rating': activity.rating,
                            'description': activity.description
                        }
                        for activity in day.activities
                    ],
                    'accommodation': day.accommodation,
                    'estimated_cost': day.estimated_cost,
                    'notes': day.notes
                }
                for day in itinerary.days
            ]
        }

    def _serialize_budget_breakdown(self, breakdown) -> Dict:
        """Serialize budget breakdown."""
        return {
            'total_budget': breakdown.total_budget,
            'transportation': breakdown.transportation,
            'accommodation': breakdown.accommodation,
            'activities': breakdown.activities,
            'dining': breakdown.dining,
            'emergency_buffer': breakdown.emergency_buffer,
            'remaining_buffer': breakdown.remaining_buffer,
            'recommendations': breakdown.recommendations[:10]
        }

    def _generate_summary(self, preferences, recommendations, itinerary, budget) -> Dict[str, str]:
        """Generate trip summary."""
        total_days = (preferences.end_date - preferences.start_date).days
        overage = budget.total_budget - (
            budget.transportation + budget.accommodation +
            budget.activities + budget.dining + budget.emergency_buffer
        )
        
        status = "✓ Within Budget" if overage >= 0 else f"⚠ Over Budget by ${abs(overage):.2f}"
        
        return {
            'trip_duration': f"{total_days} days",
            'destinations': ', '.join([rec.destination.name for rec in recommendations[:3]]),
            'travel_style': preferences.travel_style,
            'budget_status': status,
            'daily_budget': f"${budget.total_budget / total_days:.2f}",
            'total_travelers': str(preferences.number_of_travelers),
            'ai_enhanced': 'Yes'
        }

    def save_plan_to_file(self, trip_plan: Dict[str, Any], filename: str = "intelligent_trip_plan.json"):
        """Save trip plan to file."""
        with open(filename, 'w') as f:
            json.dump(trip_plan, f, indent=2)
        logger.info(f"Trip plan saved to {filename}")

    def print_trip_plan(self, trip_plan: Dict[str, Any]):
        """Print formatted trip plan."""
        print("\n" + "=" * 80)
        print("🌍 INTELLIGENT TRAVEL PLAN")
        print("=" * 80)
        
        # Summary
        print("\n📋 SUMMARY")
        print("-" * 80)
        for key, value in trip_plan['summary'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Recommendations
        print("\n📍 RECOMMENDED DESTINATIONS")
        print("-" * 80)
        for i, dest in enumerate(trip_plan['destination_recommendations'][:3], 1):
            print(f"  {i}. {dest['name']}, {dest['country']}")
            print(f"     Match Score: {dest['match_score']:.1f}%")
            print(f"     Est. Daily Cost: ${dest['estimated_daily_cost']:.2f}")
        
        # AI Insights
        print("\n🤖 AI INSIGHTS")
        print("-" * 80)
        if trip_plan.get('ai_insights'):
            print(f"  Predicted Satisfaction: {trip_plan['ai_insights'].get('predicted_satisfaction', 'N/A'):.1f}/10")
            if trip_plan['ai_insights'].get('suggested_improvements'):
                print(f"  Suggestions: {trip_plan['ai_insights']['suggested_improvements'][0]}")
        
        # Autonomous Decisions
        print("\n⚡ AUTONOMOUS DECISIONS")
        print("-" * 80)
        if trip_plan.get('autonomous_decisions'):
            for action in trip_plan['autonomous_decisions'].get('auto_actions', []):
                print(f"  ✓ {action}")
        
        # Budget
        print("\n💰 BUDGET")
        print("-" * 80)
        budget = trip_plan['budget_breakdown']
        print(f"  Total: ${budget['total_budget']:.2f}")
        print(f"  Remaining: ${budget['remaining_buffer']:.2f}")
        
        print("\n" + "=" * 80 + "\n")


def main():
    """Demonstrate intelligent orchestrator."""
    orchestrator = IntelligentTravelOrchestrator(
        use_google_api=False,
        use_llm=False,  # Set to True if you have OpenAI API key
        user_id="demo_user"
    )
    
    trip_plan = orchestrator.plan_trip(
        destinations=["Paris", "Tokyo", "Bali", "New York", "Barcelona"],
        start_date=date(2024, 6, 1),
        end_date=date(2024, 6, 15),
        budget=5000,
        travel_style="comfort",
        interests=["culture", "food", "nature"],
        number_of_travelers=2
    )
    
    orchestrator.print_trip_plan(trip_plan)
    orchestrator.save_plan_to_file(trip_plan)
    
    # Simulate trip completion and learning
    orchestrator.record_trip_completion(
        trip_id="trip_001",
        trip_plan=trip_plan,
        satisfaction_score=8.5,
        feedback="Amazing trip! Paris was perfect. Itinerary was well-paced.",
        actual_spend=4800
    )


if __name__ == "__main__":
    from datetime import date
    main()
