"""Data models for travel planning."""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import date


@dataclass
class TravelPreferences:
    """User travel preferences."""
    destinations: List[str]
    start_date: date
    end_date: date
    budget: float
    travel_style: str  # "luxury", "budget", "comfort"
    interests: List[str]  # "adventure", "culture", "nightlife", "nature", etc.
    number_of_travelers: int


@dataclass
class Destination:
    """Destination information."""
    name: str
    country: str
    latitude: float
    longitude: float
    description: str
    estimated_cost_per_day: float
    best_season: str
    attractions: List[str]
    average_temperature: float


@dataclass
class Activity:
    """Activity information."""
    name: str
    location: str
    duration_hours: float
    estimated_cost: float
    description: str
    rating: float  # 1-5
    booking_url: Optional[str] = None


@dataclass
class ItineraryDay:
    """Daily itinerary plan."""
    date: date
    location: str
    activities: List[Activity]
    accommodation: str
    estimated_cost: float
    notes: str


@dataclass
class TravelItinerary:
    """Complete travel itinerary."""
    destinations: List[str]
    days: List[ItineraryDay]
    total_duration: int
    total_estimated_cost: float
    transportation_cost: float
    accommodation_cost: float
    activities_cost: float
    dining_cost: float


@dataclass
class BudgetBreakdown:
    """Budget breakdown analysis."""
    total_budget: float
    transportation: float
    accommodation: float
    activities: float
    dining: float
    emergency_buffer: float
    remaining_buffer: float
    recommendations: List[str]


@dataclass
class DestinationRecommendation:
    """Destination recommendation with reasoning."""
    destination: Destination
    match_score: float  # 0-100
    reasons: List[str]
    estimated_daily_cost: float
    best_days_to_visit: int
    similar_destinations: List[str]
