"""Memory and context system for agents."""
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class TripMemory:
    """Memory of a past trip."""
    user_id: str
    trip_id: str
    destinations: List[str]
    start_date: str
    end_date: str
    budget: float
    travel_style: str
    interests: List[str]
    preferences: Dict[str, Any]
    satisfaction_score: float  # 0-10
    feedback: str
    created_date: str
    duration_days: int
    actual_spend: float
    lessons_learned: List[str]


@dataclass
class UserProfile:
    """User profile and preferences."""
    user_id: str
    total_trips: int
    preferred_travel_style: str
    favorite_interests: List[str]
    average_budget: float
    travel_frequency: str  # "rare", "occasional", "frequent", "very_frequent"
    preferred_seasons: List[str]
    avoided_destinations: List[str]
    favorite_destinations: List[str]
    budget_preferences: Dict[str, float]  # Weight for each cost category
    created_date: str
    last_updated: str


class MemorySystem:
    """System for storing and retrieving trip memories and user profiles."""

    def __init__(self, storage_file: str = "user_memory.json"):
        """
        Initialize memory system.
        
        Args:
            storage_file: File to persist memory data
        """
        self.storage_file = storage_file
        self.user_profiles: Dict[str, UserProfile] = {}
        self.trip_memories: Dict[str, List[TripMemory]] = {}
        self.load_from_file()
        logger.info("Memory system initialized")

    def save_trip_memory(
        self,
        user_id: str,
        trip_id: str,
        trip_data: Dict[str, Any],
        satisfaction_score: float,
        feedback: str = "",
        actual_spend: Optional[float] = None
    ) -> TripMemory:
        """
        Save memory of a completed trip.
        
        Args:
            user_id: User identifier
            trip_id: Trip identifier
            trip_data: Trip plan data
            satisfaction_score: User satisfaction (0-10)
            feedback: Optional feedback
            actual_spend: Actual amount spent
            
        Returns:
            Saved TripMemory object
        """
        preferences = trip_data.get('preferences', {})
        
        trip_memory = TripMemory(
            user_id=user_id,
            trip_id=trip_id,
            destinations=preferences.get('destinations', []),
            start_date=preferences.get('start_date', ''),
            end_date=preferences.get('end_date', ''),
            budget=preferences.get('budget', 0),
            travel_style=preferences.get('travel_style', 'comfort'),
            interests=preferences.get('interests', []),
            preferences=preferences,
            satisfaction_score=satisfaction_score,
            feedback=feedback,
            created_date=datetime.now().isoformat(),
            duration_days=preferences.get('duration_days', 0),
            actual_spend=actual_spend or preferences.get('budget', 0),
            lessons_learned=self._extract_lessons(satisfaction_score, feedback)
        )
        
        if user_id not in self.trip_memories:
            self.trip_memories[user_id] = []
        
        self.trip_memories[user_id].append(trip_memory)
        self.save_to_file()
        
        logger.info(f"Trip memory saved for user {user_id}: {trip_id}")
        return trip_memory

    def update_user_profile(self, user_id: str, trip_memory: TripMemory) -> UserProfile:
        """
        Update user profile based on trip memory.
        
        Args:
            user_id: User identifier
            trip_memory: Recently completed trip
            
        Returns:
            Updated UserProfile
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = self._create_new_profile(user_id)
        
        profile = self.user_profiles[user_id]
        
        # Update statistics
        profile.total_trips += 1
        profile.preferred_travel_style = trip_memory.travel_style
        profile.favorite_interests = list(set(profile.favorite_interests + trip_memory.interests))
        profile.average_budget = (profile.average_budget + trip_memory.budget) / 2
        profile.last_updated = datetime.now().isoformat()
        
        # Add to favorites if satisfied
        if trip_memory.satisfaction_score >= 8:
            for dest in trip_memory.destinations:
                if dest not in profile.favorite_destinations:
                    profile.favorite_destinations.append(dest)
        
        # Add to avoid list if unsatisfied
        if trip_memory.satisfaction_score <= 4:
            for dest in trip_memory.destinations:
                if dest not in profile.avoided_destinations:
                    profile.avoided_destinations.append(dest)
        
        self.save_to_file()
        logger.info(f"User profile updated: {user_id}")
        
        return profile

    def get_user_profile(self, user_id: str) -> UserProfile:
        """Get user profile."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = self._create_new_profile(user_id)
        return self.user_profiles[user_id]

    def get_trip_history(self, user_id: str) -> List[TripMemory]:
        """Get all trips for a user."""
        return self.trip_memories.get(user_id, [])

    def get_avg_satisfaction(self, user_id: str) -> float:
        """Get average satisfaction score for user."""
        trips = self.get_trip_history(user_id)
        if not trips:
            return 0.0
        return sum(t.satisfaction_score for t in trips) / len(trips)

    def get_learning_insights(self, user_id: str) -> List[str]:
        """Get consolidated learning insights from past trips."""
        trips = self.get_trip_history(user_id)
        all_lessons = []
        
        for trip in trips:
            all_lessons.extend(trip.lessons_learned)
        
        # Remove duplicates and return
        return list(set(all_lessons))

    def should_avoid_destination(self, user_id: str, destination: str) -> bool:
        """Check if destination is in avoid list."""
        profile = self.get_user_profile(user_id)
        return destination in profile.avoided_destinations

    def get_personalization_weights(self, user_id: str) -> Dict[str, float]:
        """Get learned personalization weights for user."""
        profile = self.get_user_profile(user_id)
        trips = self.get_trip_history(user_id)
        
        if not trips:
            return {
                'budget_weight': 0.35,
                'style_weight': 0.33,
                'interest_weight': 0.32
            }
        
        # Analyze what mattered most in high-satisfaction trips
        high_satisfaction_trips = [t for t in trips if t.satisfaction_score >= 8]
        
        if high_satisfaction_trips:
            # Check what these trips had in common
            avg_budget_match = sum(
                1 for t in high_satisfaction_trips 
                if t.actual_spend <= t.budget * 1.1
            ) / len(high_satisfaction_trips)
            
            style_consistency = sum(
                1 for t in high_satisfaction_trips 
                if t.travel_style == profile.preferred_travel_style
            ) / len(high_satisfaction_trips)
            
            # Adjust weights based on what worked
            budget_weight = 0.35 if avg_budget_match > 0.8 else 0.25
            style_weight = 0.33 if style_consistency > 0.7 else 0.35
            interest_weight = 1 - budget_weight - style_weight
            
            return {
                'budget_weight': budget_weight,
                'style_weight': style_weight,
                'interest_weight': interest_weight
            }
        
        return {
            'budget_weight': 0.35,
            'style_weight': 0.33,
            'interest_weight': 0.32
        }

    def _extract_lessons(self, satisfaction_score: float, feedback: str) -> List[str]:
        """Extract lessons from trip."""
        lessons = []
        
        if satisfaction_score >= 8:
            lessons.append("Plan type was well-received - repeat this approach")
        elif satisfaction_score >= 5:
            lessons.append("Mixed results - consider adjustments for next time")
        else:
            lessons.append("Low satisfaction - significant changes needed")
        
        feedback_lower = feedback.lower()
        
        if 'budget' in feedback_lower:
            if 'exceed' in feedback_lower or 'expensive' in feedback_lower:
                lessons.append("Budget was too tight - allocate more next time")
            else:
                lessons.append("Budget management was good")
        
        if 'pace' in feedback_lower or 'rushed' in feedback_lower:
            lessons.append("Itinerary was too packed - fewer destinations next time")
        
        if 'relaxing' in feedback_lower or 'slow' in feedback_lower:
            lessons.append("Slower pace appreciated - maintain this style")
        
        return lessons

    def _create_new_profile(self, user_id: str) -> UserProfile:
        """Create a new user profile."""
        return UserProfile(
            user_id=user_id,
            total_trips=0,
            preferred_travel_style='comfort',
            favorite_interests=[],
            average_budget=3000,
            travel_frequency='occasional',
            preferred_seasons=['spring', 'fall'],
            avoided_destinations=[],
            favorite_destinations=[],
            budget_preferences={
                'accommodation': 0.40,
                'activities': 0.30,
                'dining': 0.15,
                'transport': 0.15
            },
            created_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )

    def save_to_file(self):
        """Save memory to file."""
        try:
            data = {
                'profiles': {
                    user_id: asdict(profile)
                    for user_id, profile in self.user_profiles.items()
                },
                'trips': {
                    user_id: [asdict(trip) for trip in trips]
                    for user_id, trips in self.trip_memories.items()
                }
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Memory saved to file")
        except Exception as e:
            logger.error(f"Error saving memory to file: {str(e)}")

    def load_from_file(self):
        """Load memory from file."""
        try:
            if not os.path.exists(self.storage_file):
                return
            
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Load profiles
            for user_id, profile_data in data.get('profiles', {}).items():
                self.user_profiles[user_id] = UserProfile(**profile_data)
            
            # Load trips
            for user_id, trips_data in data.get('trips', {}).items():
                self.trip_memories[user_id] = [TripMemory(**trip) for trip in trips_data]
            
            logger.info("Memory loaded from file")
        except Exception as e:
            logger.error(f"Error loading memory from file: {str(e)}")


import os
