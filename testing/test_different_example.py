"""
Test: Different Example Scenario for Travel Planning
This test checks the system with a new set of user preferences and ensures all outputs are correct and hotels are assigned to the right cities.
"""
import pytest
from travel_agents.orchestrator import TravelPlanningOrchestrator
from datetime import date

def test_different_example():
    orchestrator = TravelPlanningOrchestrator(use_google_api=True)
    # New scenario: Family trip, 3 cities, moderate budget, focus on history and fun
    destinations = ["Rome", "Athens", "Istanbul"]
    start_date = date(2026, 7, 10)
    end_date = date(2026, 7, 24)
    budget = 5000
    travel_style = "family"
    interests = ["history", "fun"]
    number_of_travelers = 4

    trip_plan = orchestrator.plan_trip(
        destinations=destinations,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        travel_style=travel_style,
        interests=interests,
        number_of_travelers=number_of_travelers
    )

    # Basic checks
    assert trip_plan is not None
    assert hasattr(trip_plan, "itinerary")
    assert hasattr(trip_plan, "budget_breakdown")
    # Check that each day has a valid city and hotel in that city
    for day in trip_plan.itinerary.days:
        assert day.city in destinations
        assert day.hotel is not None
        assert day.hotel.city == day.city
    # Check budget is not exceeded
    assert trip_plan.budget_breakdown.total <= budget
