"""Destination Recommender Agent for travel planning."""
from typing import List
from travel_agents.agents.base_agent import BaseAgent
from travel_agents.models.travel_plan import (
    TravelPreferences, DestinationRecommendation, Destination
)
from travel_agents.services.google_api_service import GoogleAPIService
import logging

logger = logging.getLogger(__name__)

# Sample destination database
DESTINATION_DATABASE = [
    Destination(
        name="Paris",
        country="France",
        latitude=48.8566,
        longitude=2.3522,
        description="City of love and art with iconic landmarks",
        estimated_cost_per_day=100,
        best_season="April-May, September-October",
        attractions=["Eiffel Tower", "Louvre", "Notre-Dame", "Arc de Triomphe"],
        average_temperature=15
    ),
    Destination(
        name="Tokyo",
        country="Japan",
        latitude=35.6762,
        longitude=139.6503,
        description="Vibrant metropolis blending tradition and technology",
        estimated_cost_per_day=120,
        best_season="March-May, September-November",
        attractions=["Shibuya", "Senso-ji", "Tsukiji Market", "Tokyo Tower"],
        average_temperature=16
    ),
    Destination(
        name="Bali",
        country="Indonesia",
        latitude=-8.6705,
        longitude=115.2126,
        description="Tropical paradise with beaches and culture",
        estimated_cost_per_day=40,
        best_season="April-October",
        attractions=["Ubud", "Sacred Monkey Forest", "Bali Beach", "Tanah Lot"],
        average_temperature=28
    ),
    Destination(
        name="New York",
        country="USA",
        latitude=40.7128,
        longitude=-74.0060,
        description="The city that never sleeps with endless entertainment",
        estimated_cost_per_day=150,
        best_season="April-May, September-November",
        attractions=["Statue of Liberty", "Times Square", "Central Park", "Broadway"],
        average_temperature=12
    ),
    Destination(
        name="Barcelona",
        country="Spain",
        latitude=41.3851,
        longitude=2.1734,
        description="Coastal city with unique architecture and culture",
        estimated_cost_per_day=80,
        best_season="April-May, September-October",
        attractions=["Sagrada Familia", "Park Güell", "Gothic Quarter", "Montjuïc"],
        average_temperature=18
    ),
    Destination(
        name="Dubai",
        country="UAE",
        latitude=25.2048,
        longitude=55.2708,
        description="Modern desert city with luxury shopping and attractions",
        estimated_cost_per_day=110,
        best_season="October-April",
        attractions=["Burj Khalifa", "Palm Islands", "Gold Souk", "Desert Safari"],
        average_temperature=30
    ),
    Destination(
        name="Bangkok",
        country="Thailand",
        latitude=13.7563,
        longitude=100.5018,
        description="Bustling city with temples, street food, and nightlife",
        estimated_cost_per_day=30,
        best_season="November-February",
        attractions=["Grand Palace", "Wat Pho", "Floating Markets", "Street Food"],
        average_temperature=28
    ),
    Destination(
        name="Rome",
        country="Italy",
        latitude=41.9028,
        longitude=12.4964,
        description="Ancient capital with timeless history and culture",
        estimated_cost_per_day=90,
        best_season="April-May, September-October",
        attractions=["Colosseum", "Roman Forum", "Vatican", "Trevi Fountain"],
        average_temperature=18
    ),
]


class DestinationRecommenderAgent(BaseAgent):
    """Agent for recommending destinations based on user preferences."""

    def __init__(self, google_api_service: GoogleAPIService = None):
        """Initialize destination recommender agent."""
        super().__init__("DestinationRecommender")
        self.google_api_service = google_api_service
        self.destinations = DESTINATION_DATABASE

    def validate_input(self, input_data) -> bool:
        """Validate travel preferences input."""
        if not isinstance(input_data, TravelPreferences):
            return False
        if not input_data.destinations or len(input_data.destinations) == 0:
            return False
        if input_data.budget <= 0:
            return False
        return True

    def calculate_match_score(
        self,
        destination: Destination,
        preferences: TravelPreferences
    ) -> float:
        """
        Calculate match score for a destination based on preferences.
        
        Args:
            destination: Destination to score
            preferences: User preferences
            
        Returns:
            Match score (0-100)
        """
        score = 0.0
        
        # Budget matching (40 points)
        daily_cost = destination.estimated_cost_per_day
        travel_days = (preferences.end_date - preferences.start_date).days
        total_cost = daily_cost * travel_days
        
        if total_cost <= preferences.budget * 0.6:
            score += 40
        elif total_cost <= preferences.budget:
            score += 30
        elif total_cost <= preferences.budget * 1.2:
            score += 15
        else:
            score += 5
        
        # Style matching (30 points)
        if preferences.travel_style == "luxury":
            score += 20 if daily_cost > 100 else 10
        elif preferences.travel_style == "budget":
            score += 20 if daily_cost < 50 else 10
        else:  # comfort
            score += 20
        
        # Interest matching (30 points)
        attractions_lower = [attr.lower() for attr in destination.attractions]
        interests_lower = [interest.lower() for interest in preferences.interests]
        
        matching_interests = len(set(interests_lower) & set(attractions_lower))
        score += min(30, matching_interests * 10)
        
        return min(100, score)

    def get_recommendations(
        self,
        preferences: TravelPreferences,
        top_n: int = 5
    ) -> List[DestinationRecommendation]:
        """
        Get top destination recommendations.
        
        Args:
            preferences: User travel preferences
            top_n: Number of top recommendations to return
            
        Returns:
            List of destination recommendations
        """
        recommendations = []
        
        for destination in self.destinations:
            score = self.calculate_match_score(destination, preferences)
            
            travel_days = (preferences.end_date - preferences.start_date).days
            estimated_daily_cost = destination.estimated_cost_per_day
            
            recommendation = DestinationRecommendation(
                destination=destination,
                match_score=score,
                reasons=self._generate_reasons(destination, preferences, score),
                estimated_daily_cost=estimated_daily_cost,
                best_days_to_visit=max(2, min(7, travel_days)),
                similar_destinations=self._find_similar_destinations(destination.name)
            )
            recommendations.append(recommendation)
        
        # Sort by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        
        return recommendations[:top_n]

    def _generate_reasons(
        self,
        destination: Destination,
        preferences: TravelPreferences,
        score: float
    ) -> List[str]:
        """Generate reasons for recommendation."""
        reasons = []
        
        if score >= 80:
            reasons.append("Excellent match for your preferences")
        elif score >= 60:
            reasons.append("Good match for your travel style")
        else:
            reasons.append("Matches some of your preferences")
        
        travel_days = (preferences.end_date - preferences.start_date).days
        total_cost = destination.estimated_cost_per_day * travel_days
        
        if total_cost <= preferences.budget:
            reasons.append(f"Fits within your budget (Est. ${total_cost:.2f})")
        else:
            reasons.append(f"Slightly above budget (Est. ${total_cost:.2f})")
        
        reasons.append(f"Best season: {destination.best_season}")
        reasons.append(f"Popular attractions: {', '.join(destination.attractions[:3])}")
        
        return reasons

    def _find_similar_destinations(self, destination_name: str) -> List[str]:
        """Find similar destinations."""
        similar = []
        current_dest = next(
            (d for d in self.destinations if d.name == destination_name),
            None
        )
        
        if current_dest:
            for dest in self.destinations:
                if dest.name != destination_name:
                    # Simple similarity based on cost and attractions
                    cost_diff = abs(dest.estimated_cost_per_day - current_dest.estimated_cost_per_day)
                    if cost_diff < 50:
                        similar.append(dest.name)
        
        return similar[:3]

    def process(self, input_data: TravelPreferences) -> List[DestinationRecommendation]:
        """
        Process travel preferences and return destination recommendations.
        
        Args:
            input_data: Travel preferences
            
        Returns:
            List of destination recommendations
        """
        self.logger.info(f"Generating recommendations for {len(input_data.destinations)} destinations")
        
        recommendations = self.get_recommendations(input_data)
        
        self.logger.info(f"Generated {len(recommendations)} recommendations")
        
        return recommendations
