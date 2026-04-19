"""Main orchestrator for travel planning agents."""
from typing import List, Dict, Any
from datetime import datetime, date
from travel_agents.models.travel_plan import (
    TravelPreferences, DestinationRecommendation, TravelItinerary, BudgetBreakdown
)
from travel_agents.agents.destination_recommender_agent import DestinationRecommenderAgent
from travel_agents.agents.itinerary_planner_agent import ItineraryPlannerAgent
from travel_agents.agents.budget_optimizer_agent import BudgetOptimizerAgent
from travel_agents.services.google_api_service import GoogleAPIService
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TravelPlanningOrchestrator:
    """Orchestrator to manage all travel planning agents."""

    def __init__(self, use_google_api: bool = True):
        """
        Initialize the orchestrator with all agents.
        
        Args:
            use_google_api: Whether to use Google API (requires API key)
        """
        self.google_api_service = None
        if use_google_api:
            try:
                self.google_api_service = GoogleAPIService()
            except ValueError:
                logger.warning("Google API key not found. Using agents without API integration.")
        
        # Initialize agents
        self.destination_recommender = DestinationRecommenderAgent(self.google_api_service)
        self.itinerary_planner = ItineraryPlannerAgent(self.google_api_service)
        self.budget_optimizer = BudgetOptimizerAgent(self.google_api_service)
        
        logger.info("Travel Planning Orchestrator initialized")

    def plan_trip(
        self,
        destinations: List[str],
        start_date: date,
        end_date: date,
        budget: float,
        travel_style: str,
        interests: List[str],
        number_of_travelers: int = 1
    ) -> Dict[str, Any]:
        """
        Plan a complete trip using all agents.
        
        Args:
            destinations: List of desired destinations
            start_date: Trip start date
            end_date: Trip end date
            budget: Total budget for the trip
            travel_style: Travel style ("luxury", "budget", "comfort")
            interests: List of interests (e.g., ["culture", "nature", "food"])
            number_of_travelers: Number of travelers
            
        Returns:
            Dictionary with complete trip plan including recommendations, itinerary, and budget
        """
        logger.info("=" * 60)
        logger.info("Starting trip planning process...")
        logger.info("=" * 60)
        
        # Step 1: Create user preferences
        preferences = TravelPreferences(
            destinations=destinations,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            travel_style=travel_style,
            interests=interests,
            number_of_travelers=number_of_travelers
        )
        
        logger.info("\n📍 Step 1: Generating Destination Recommendations...")
        logger.info("-" * 60)
        
        # Step 2: Get destination recommendations
        recommendations = self.destination_recommender.run(preferences)
        
        # Select top destinations (up to 3)
        selected_destinations = [
            rec.destination.name for rec in recommendations[:min(3, len(recommendations))]
        ]
        logger.info(f"Selected destinations: {', '.join(selected_destinations)}")
        
        # Step 3: Create itinerary
        logger.info("\n📅 Step 2: Creating Detailed Itinerary...")
        logger.info("-" * 60)
        
        itinerary_input = {
            'preferences': preferences,
            'selected_destinations': selected_destinations
        }
        itinerary = self.itinerary_planner.run(itinerary_input)
        logger.info(f"Itinerary created for {itinerary.total_duration} days")
        
        # Step 4: Optimize budget
        logger.info("\n💰 Step 3: Optimizing Budget...")
        logger.info("-" * 60)
        
        budget_input = {
            'itinerary': itinerary,
            'total_budget': budget
        }
        budget_breakdown = self.budget_optimizer.run(budget_input)
        
        # Compile complete trip plan
        trip_plan = {
            'preferences': self._serialize_preferences(preferences),
            'destination_recommendations': self._serialize_recommendations(recommendations),
            'selected_destinations': selected_destinations,
            'itinerary': self._serialize_itinerary(itinerary),
            'budget_breakdown': self._serialize_budget_breakdown(budget_breakdown),
            'summary': self._generate_summary(
                preferences, selected_destinations, itinerary, budget_breakdown
            )
        }
        
        logger.info("\n" + "=" * 60)
        logger.info("Trip planning complete!")
        logger.info("=" * 60)
        
        return trip_plan

    def _serialize_preferences(self, preferences: TravelPreferences) -> Dict:
        """Serialize preferences to dictionary."""
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

    def _serialize_recommendations(
        self,
        recommendations: List[DestinationRecommendation]
    ) -> List[Dict]:
        """Serialize recommendations to dictionary."""
        result = []
        for rec in recommendations:
            result.append({
                'name': rec.destination.name,
                'country': rec.destination.country,
                'match_score': rec.match_score,
                'estimated_daily_cost': rec.estimated_daily_cost,
                'best_days_to_visit': rec.best_days_to_visit,
                'attractions': rec.destination.attractions,
                'reasons': rec.reasons,
                'similar_destinations': rec.similar_destinations
            })
        return result

    def _serialize_itinerary(self, itinerary: TravelItinerary) -> Dict:
        """Serialize itinerary to dictionary."""
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

    def _serialize_budget_breakdown(self, breakdown: BudgetBreakdown) -> Dict:
        """Serialize budget breakdown to dictionary."""
        return {
            'total_budget': breakdown.total_budget,
            'transportation': breakdown.transportation,
            'accommodation': breakdown.accommodation,
            'activities': breakdown.activities,
            'dining': breakdown.dining,
            'emergency_buffer': breakdown.emergency_buffer,
            'remaining_buffer': breakdown.remaining_buffer,
            'recommendations': breakdown.recommendations
        }

    def _generate_summary(
        self,
        preferences: TravelPreferences,
        selected_destinations: List[str],
        itinerary: TravelItinerary,
        budget: BudgetBreakdown
    ) -> Dict[str, str]:
        """Generate a summary of the trip plan."""
        total_days = (preferences.end_date - preferences.start_date).days
        overage = budget.total_budget - (
            budget.transportation + budget.accommodation +
            budget.activities + budget.dining + budget.emergency_buffer
        )
        
        status = "✓ Within Budget" if overage >= 0 else f"⚠ Over Budget by ${abs(overage):.2f}"
        
        return {
            'trip_duration': f"{total_days} days",
            'destinations': ', '.join(selected_destinations),
            'travel_style': preferences.travel_style,
            'budget_status': status,
            'daily_budget': f"${budget.total_budget / total_days:.2f}",
            'total_travelers': str(preferences.number_of_travelers)
        }

    def save_plan_to_file(self, trip_plan: Dict[str, Any], filename: str = "trip_plan.json"):
        """Save trip plan to JSON file."""
        with open(filename, 'w') as f:
            json.dump(trip_plan, f, indent=2)
        logger.info(f"Trip plan saved to {filename}")

    def print_trip_plan(self, trip_plan: Dict[str, Any]):
        """Print trip plan in a formatted way."""
        print("\n" + "=" * 70)
        print("🌍 COMPLETE TRIP PLAN")
        print("=" * 70)
        
        # Summary
        print("\n📋 SUMMARY")
        print("-" * 70)
        for key, value in trip_plan['summary'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Destinations
        print("\n📍 TOP RECOMMENDED DESTINATIONS")
        print("-" * 70)
        for i, dest in enumerate(trip_plan['destination_recommendations'][:3], 1):
            print(f"  {i}. {dest['name']}, {dest['country']}")
            print(f"     Match Score: {dest['match_score']:.1f}%")
            print(f"     Est. Daily Cost: ${dest['estimated_daily_cost']:.2f}")
            print(f"     Key Attractions: {', '.join(dest['attractions'][:2])}")
        
        # Budget
        print("\n💰 BUDGET BREAKDOWN")
        print("-" * 70)
        budget = trip_plan['budget_breakdown']
        print(f"  Total Budget: ${budget['total_budget']:.2f}")
        print(f"  - Transportation: ${budget['transportation']:.2f}")
        print(f"  - Accommodation: ${budget['accommodation']:.2f}")
        print(f"  - Activities: ${budget['activities']:.2f}")
        print(f"  - Dining: ${budget['dining']:.2f}")
        print(f"  - Emergency Buffer: ${budget['emergency_buffer']:.2f}")
        print(f"  Remaining: ${budget['remaining_buffer']:.2f}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS")
        print("-" * 70)
        for rec in budget['recommendations'][:5]:
            print(f"  • {rec}")
        
        print("\n" + "=" * 70 + "\n")


def main():
    """Main function to demonstrate the travel planning system."""
    # Example usage
    orchestrator = TravelPlanningOrchestrator(use_google_api=False)
    
    trip_plan = orchestrator.plan_trip(
        destinations=["Paris", "Tokyo", "Bali", "New York", "Barcelona"],
        start_date=date(2024, 6, 1),
        end_date=date(2024, 6, 15),
        budget=5000,
        travel_style="comfort",
        interests=["culture", "food", "nature"],
        number_of_travelers=2
    )
    
    # Print and save the plan
    orchestrator.print_trip_plan(trip_plan)
    orchestrator.save_plan_to_file(trip_plan)


if __name__ == "__main__":
    main()
