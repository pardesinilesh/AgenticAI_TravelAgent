"""Itinerary Planner Agent for travel planning."""
from typing import List
from datetime import datetime, timedelta
from travel_agents.agents.base_agent import BaseAgent
from travel_agents.models.travel_plan import (
    TravelPreferences, TravelItinerary, ItineraryDay, Activity
)
from travel_agents.services.google_api_service import GoogleAPIService
import logging

logger = logging.getLogger(__name__)


class ItineraryPlannerAgent(BaseAgent):
    """Agent for creating detailed travel itineraries."""

    def __init__(self, google_api_service: GoogleAPIService = None):
        """Initialize itinerary planner agent."""
        super().__init__("ItineraryPlanner")
        self.google_api_service = google_api_service

    def validate_input(self, input_data) -> bool:
        """Validate itinerary planning input."""
        if not isinstance(input_data, dict):
            return False
        
        required_keys = ['preferences', 'selected_destinations']
        if not all(key in input_data for key in required_keys):
            return False
        
        if not isinstance(input_data['preferences'], TravelPreferences):
            return False
        
        if not isinstance(input_data['selected_destinations'], list):
            return False
        
        return True

    def create_daily_activities(
        self,
        destination: str,
        day: int,
        total_days: int,
        interests: List[str]
    ) -> List[Activity]:
        """
        Create activities for a day based on destination and interests.
        
        Args:
            destination: Destination name
            day: Day number
            total_days: Total days in trip
            interests: User interests
            
        Returns:
            List of activities for the day
        """
        activities = []
        
        # Activity templates based on interests
        activity_database = {
            'culture': [
                Activity("Museum Visit", destination, 3, 15, "Explore local art and history", 4.5),
                Activity("Historical Tour", destination, 4, 20, "Guided tour of historical sites", 4.7),
                Activity("Local Market Tour", destination, 2, 10, "Experience local culture", 4.3),
            ],
            'adventure': [
                Activity("Hiking Excursion", destination, 6, 40, "Outdoor mountain hiking", 4.6),
                Activity("Water Sports", destination, 3, 50, "Swimming and water activities", 4.5),
                Activity("Rock Climbing", destination, 4, 60, "Rock climbing experience", 4.8),
            ],
            'nightlife': [
                Activity("Bar Hopping", destination, 4, 30, "Visit local bars and clubs", 4.2),
                Activity("Night Club", destination, 3, 40, "Dance and entertainment", 4.4),
                Activity("Live Music Show", destination, 2, 35, "Local live music venue", 4.6),
            ],
            'nature': [
                Activity("Nature Walking", destination, 3, 0, "Scenic nature walk", 4.5),
                Activity("Beach Day", destination, 5, 20, "Beach relaxation and swimming", 4.7),
                Activity("Wildlife Safari", destination, 6, 80, "See local wildlife", 4.9),
            ],
            'food': [
                Activity("Cooking Class", destination, 3, 45, "Learn local cuisine", 4.7),
                Activity("Food Tour", destination, 4, 25, "Taste local dishes", 4.6),
                Activity("Fine Dining", destination, 2, 80, "Upscale restaurant experience", 4.5),
            ],
        }
        
        # Select activities based on interests
        selected_activities = []
        for interest in interests:
            interest_lower = interest.lower()
            if interest_lower in activity_database:
                selected_activities.extend(activity_database[interest_lower])
        
        # If no interests matched, use default activities
        if not selected_activities:
            selected_activities = [
                Activity("City Exploration", destination, 4, 0, "Explore the city on foot", 4.5),
                Activity("Local Restaurant", destination, 2, 30, "Enjoy local cuisine", 4.4),
            ]
        
        # Select activities for this day
        activities_per_day = 2
        if day == 1 or day == total_days:
            activities_per_day = 1  # Less activities on first and last day for travel
        
        for i in range(min(activities_per_day, len(selected_activities))):
            activities.append(selected_activities[i])
        
        return activities

    def create_itinerary_day(
        self,
        destination: str,
        date: datetime,
        day_number: int,
        total_days: int,
        interests: List[str],
        daily_budget: float
    ) -> ItineraryDay:
        """
        Create itinerary for a single day.
        
        Args:
            destination: Destination name
            date: Date of the day
            day_number: Day number
            total_days: Total days
            interests: User interests
            daily_budget: Budget for the day
            
        Returns:
            ItineraryDay object
        """
        activities = self.create_daily_activities(destination, day_number, total_days, interests)
        
        total_activity_cost = sum(activity.estimated_cost for activity in activities)
        accommodation_cost = daily_budget * 0.4  # 40% for accommodation
        dining_cost = daily_budget * 0.3  # 30% for dining
        activities_cost = min(total_activity_cost, daily_budget * 0.3)  # 30% for activities
        
        day = ItineraryDay(
            date=date,
            location=destination,
            activities=activities,
            accommodation=f"Hotel in {destination}",
            estimated_cost=accommodation_cost + dining_cost + activities_cost,
            notes=f"Day {day_number} - {destination}"
        )
        
        return day

    def process(self, input_data: dict) -> TravelItinerary:
        """
        Process travel preferences and create detailed itinerary.
        
        Args:
            input_data: Dictionary with preferences and selected destinations
            
        Returns:
            Complete travel itinerary
        """
        preferences: TravelPreferences = input_data['preferences']
        selected_destinations: List[str] = input_data['selected_destinations']
        
        self.logger.info(f"Creating itinerary for {selected_destinations}")
        
        # Calculate total days
        total_days = (preferences.end_date - preferences.start_date).days
        daily_budget = preferences.budget / total_days
        
        # Distribute destinations
        days_per_destination = total_days // len(selected_destinations)
        
        itinerary_days = []
        current_date = preferences.start_date
        destination_index = 0
        
        for day_num in range(1, total_days + 1):
            # Switch destination after allocated days
            if day_num > 1 and (day_num - 1) % days_per_destination == 0 and destination_index < len(selected_destinations) - 1:
                destination_index += 1
            
            current_destination = selected_destinations[destination_index]
            
            day = self.create_itinerary_day(
                destination=current_destination,
                date=current_date,
                day_number=day_num,
                total_days=total_days,
                interests=preferences.interests,
                daily_budget=daily_budget
            )
            
            itinerary_days.append(day)
            current_date += timedelta(days=1)
        
        # Calculate totals
        total_cost = sum(day.estimated_cost for day in itinerary_days)
        transportation_cost = total_cost * 0.15  # Estimate 15% for transportation
        accommodation_cost = total_cost * 0.40
        activities_cost = total_cost * 0.30
        dining_cost = total_cost * 0.15
        
        itinerary = TravelItinerary(
            destinations=selected_destinations,
            days=itinerary_days,
            total_duration=total_days,
            total_estimated_cost=total_cost,
            transportation_cost=transportation_cost,
            accommodation_cost=accommodation_cost,
            activities_cost=activities_cost,
            dining_cost=dining_cost
        )
        
        self.logger.info(f"Itinerary created for {total_days} days across {len(selected_destinations)} destinations")
        
        return itinerary
