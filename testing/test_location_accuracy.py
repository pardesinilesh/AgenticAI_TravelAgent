"""
Test: Location Accuracy for Hotels
Ensures that hotels are always assigned to the correct city for each day in the itinerary.
"""
import pytest
from travel_agents.orchestrator import TravelPlanningOrchestrator
from datetime import date

def test_hotel_location_accuracy():
    orchestrator = TravelPlanningOrchestrator(use_google_api=True)
    destinations = ["Berlin", "Prague", "Vienna"]
    start_date = date(2026, 8, 1)
    end_date = date(2026, 8, 10)
    budget = 3000
    travel_style = "comfort"
    interests = ["art", "architecture"]
    number_of_travelers = 2

    trip_plan = orchestrator.plan_trip(
        destinations=destinations,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        travel_style=travel_style,
        interests=interests,
        number_of_travelers=number_of_travelers
    )

    for day in trip_plan.itinerary.days:
        assert day.city in destinations, f"Day city {day.city} not in requested destinations"
        assert day.hotel is not None, f"No hotel assigned for {day.city}"
        assert day.hotel.city == day.city, f"Hotel city {day.hotel.city} does not match day city {day.city}"
