# Travel Planning Agent System - API Reference

Complete API documentation for the Travel Planning Agent System.

## Table of Contents

1. [Orchestrator](#orchestrator)
2. [Agents](#agents)
3. [Models](#models)
4. [Services](#services)
5. [Exceptions](#exceptions)

## Orchestrator

### TravelPlanningOrchestrator

Main orchestrator class that coordinates all agents.

#### Constructor

```python
def __init__(self, use_google_api: bool = True)
```

**Parameters:**
- `use_google_api` (bool, optional): Enable Google Maps API integration. Defaults to True.

**Raises:**
- `ValueError`: If Google API key not found and `use_google_api=True`

**Example:**
```python
orchestrator = TravelPlanningOrchestrator(use_google_api=False)
```

#### plan_trip()

```python
def plan_trip(
    destinations: List[str],
    start_date: date,
    end_date: date,
    budget: float,
    travel_style: str,
    interests: List[str],
    number_of_travelers: int = 1
) -> Dict[str, Any]
```

Plan a complete trip using all agents.

**Parameters:**
- `destinations` (List[str]): Desired destinations. Example: `["Paris", "London"]`
- `start_date` (date): Trip start date. Example: `date(2024, 6, 1)`
- `end_date` (date): Trip end date. Example: `date(2024, 6, 15)`
- `budget` (float): Total budget in USD. Example: `5000.0`
- `travel_style` (str): Travel style - "luxury", "budget", or "comfort"
- `interests` (List[str]): List of interests. Options: "culture", "food", "nature", "adventure", "nightlife"
- `number_of_travelers` (int, optional): Number of travelers. Defaults to 1.

**Returns:**
- `Dict[str, Any]`: Complete trip plan with recommendations, itinerary, and budget analysis

**Raises:**
- `ValueError`: If input validation fails
- `Exception`: If orchestration process fails

**Example:**
```python
trip_plan = orchestrator.plan_trip(
    destinations=["Paris", "London"],
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 10),
    budget=3000,
    travel_style="comfort",
    interests=["culture", "food"],
    number_of_travelers=2
)
```

#### save_plan_to_file()

```python
def save_plan_to_file(
    trip_plan: Dict[str, Any],
    filename: str = "trip_plan.json"
) -> None
```

Save trip plan to JSON file.

**Parameters:**
- `trip_plan` (Dict[str, Any]): Trip plan to save
- `filename` (str, optional): Output filename. Defaults to "trip_plan.json"

**Example:**
```python
orchestrator.save_plan_to_file(trip_plan, "my_trip_plan.json")
```

#### print_trip_plan()

```python
def print_trip_plan(trip_plan: Dict[str, Any]) -> None
```

Print formatted trip plan to console.

**Parameters:**
- `trip_plan` (Dict[str, Any]): Trip plan to print

**Example:**
```python
orchestrator.print_trip_plan(trip_plan)
```

---

## Agents

### BaseAgent

Abstract base class for all agents.

#### Methods

```python
def validate_input(self, input_data: Any) -> bool
```

Validate input data.

```python
def process(self, input_data: Any) -> Any
```

Process input data and return result.

```python
def run(self, input_data: Any) -> Any
```

Execute the agent with validation and error handling.

---

### DestinationRecommenderAgent

Agent for recommending travel destinations.

#### Constructor

```python
def __init__(self, google_api_service: GoogleAPIService = None)
```

**Parameters:**
- `google_api_service` (GoogleAPIService, optional): Google API service instance

#### run()

```python
def run(self, preferences: TravelPreferences) -> List[DestinationRecommendation]
```

Generate destination recommendations.

**Parameters:**
- `preferences` (TravelPreferences): User travel preferences

**Returns:**
- `List[DestinationRecommendation]`: Ranked list of recommendations

**Example:**
```python
agent = DestinationRecommenderAgent()
recommendations = agent.run(preferences)

for rec in recommendations:
    print(f"{rec.destination.name}: {rec.match_score}% match")
```

#### get_recommendations()

```python
def get_recommendations(
    preferences: TravelPreferences,
    top_n: int = 5
) -> List[DestinationRecommendation]
```

Get top N recommendations.

**Parameters:**
- `preferences` (TravelPreferences): User preferences
- `top_n` (int, optional): Number of recommendations. Defaults to 5.

**Returns:**
- `List[DestinationRecommendation]`: Top N recommendations

---

### ItineraryPlannerAgent

Agent for creating detailed travel itineraries.

#### Constructor

```python
def __init__(self, google_api_service: GoogleAPIService = None)
```

#### run()

```python
def run(self, input_data: Dict) -> TravelItinerary
```

Generate detailed itinerary.

**Parameters:**
- `input_data` (Dict): Dictionary with keys:
  - `preferences` (TravelPreferences): User preferences
  - `selected_destinations` (List[str]): Selected destinations

**Returns:**
- `TravelItinerary`: Complete itinerary

**Example:**
```python
agent = ItineraryPlannerAgent()
itinerary = agent.run({
    'preferences': preferences,
    'selected_destinations': ['Paris', 'London']
})
```

#### create_daily_activities()

```python
def create_daily_activities(
    destination: str,
    day: int,
    total_days: int,
    interests: List[str]
) -> List[Activity]
```

Generate activities for a specific day.

**Parameters:**
- `destination` (str): Destination name
- `day` (int): Day number
- `total_days` (int): Total trip days
- `interests` (List[str]): User interests

**Returns:**
- `List[Activity]`: Daily activities

---

### BudgetOptimizerAgent

Agent for optimizing travel budget.

#### Constructor

```python
def __init__(self, google_api_service: GoogleAPIService = None)
```

#### run()

```python
def run(self, input_data: Dict) -> BudgetBreakdown
```

Analyze and optimize budget.

**Parameters:**
- `input_data` (Dict): Dictionary with keys:
  - `itinerary` (TravelItinerary): Travel itinerary
  - `total_budget` (float): Total available budget

**Returns:**
- `BudgetBreakdown`: Budget analysis with recommendations

**Example:**
```python
agent = BudgetOptimizerAgent()
breakdown = agent.run({
    'itinerary': itinerary,
    'total_budget': 5000
})
```

#### analyze_budget()

```python
def analyze_budget(
    itinerary: TravelItinerary,
    total_budget: float
) -> BudgetBreakdown
```

Perform comprehensive budget analysis.

**Returns:**
- `BudgetBreakdown`: Detailed breakdown

---

## Models

### TravelPreferences

```python
@dataclass
class TravelPreferences:
    destinations: List[str]
    start_date: date
    end_date: date
    budget: float
    travel_style: str  # "luxury", "budget", "comfort"
    interests: List[str]
    number_of_travelers: int
```

User travel preferences and constraints.

**Attributes:**
- `destinations`: List of desired destinations
- `start_date`: Trip start date
- `end_date`: Trip end date
- `budget`: Total budget in USD
- `travel_style`: One of "luxury", "budget", or "comfort"
- `interests`: List of interests (e.g., "culture", "food")
- `number_of_travelers`: Number of people traveling

---

### Destination

```python
@dataclass
class Destination:
    name: str
    country: str
    latitude: float
    longitude: float
    description: str
    estimated_cost_per_day: float
    best_season: str
    attractions: List[str]
    average_temperature: float
```

Information about a travel destination.

**Attributes:**
- `name`: Destination name
- `country`: Country name
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude
- `description`: Destination description
- `estimated_cost_per_day`: Daily cost estimate in USD
- `best_season`: Best time to visit
- `attractions`: List of attractions
- `average_temperature`: Average temperature in Celsius

---

### Activity

```python
@dataclass
class Activity:
    name: str
    location: str
    duration_hours: float
    estimated_cost: float
    description: str
    rating: float  # 1-5
    booking_url: Optional[str] = None
```

Individual activity or attraction.

**Attributes:**
- `name`: Activity name
- `location`: Activity location
- `duration_hours`: Duration in hours
- `estimated_cost`: Cost in USD
- `description`: Activity description
- `rating`: Rating from 1-5
- `booking_url`: Optional booking URL

---

### ItineraryDay

```python
@dataclass
class ItineraryDay:
    date: date
    location: str
    activities: List[Activity]
    accommodation: str
    estimated_cost: float
    notes: str
```

Daily itinerary plan.

**Attributes:**
- `date`: Date of the day
- `location`: Location for the day
- `activities`: List of activities
- `accommodation`: Accommodation details
- `estimated_cost`: Daily cost estimate
- `notes`: Additional notes

---

### TravelItinerary

```python
@dataclass
class TravelItinerary:
    destinations: List[str]
    days: List[ItineraryDay]
    total_duration: int
    total_estimated_cost: float
    transportation_cost: float
    accommodation_cost: float
    activities_cost: float
    dining_cost: float
```

Complete travel itinerary.

**Attributes:**
- `destinations`: List of destinations
- `days`: List of daily plans
- `total_duration`: Trip duration in days
- `total_estimated_cost`: Total estimated cost
- `transportation_cost`: Transportation cost estimate
- `accommodation_cost`: Accommodation cost estimate
- `activities_cost`: Activities cost estimate
- `dining_cost`: Dining cost estimate

---

### BudgetBreakdown

```python
@dataclass
class BudgetBreakdown:
    total_budget: float
    transportation: float
    accommodation: float
    activities: float
    dining: float
    emergency_buffer: float
    remaining_buffer: float
    recommendations: List[str]
```

Budget analysis and recommendations.

**Attributes:**
- `total_budget`: Total available budget
- `transportation`: Transportation allocation
- `accommodation`: Accommodation allocation
- `activities`: Activities allocation
- `dining`: Dining allocation
- `emergency_buffer`: Emergency fund (10% of budget)
- `remaining_buffer`: Unallocated budget
- `recommendations`: List of optimization recommendations

---

### DestinationRecommendation

```python
@dataclass
class DestinationRecommendation:
    destination: Destination
    match_score: float  # 0-100
    reasons: List[str]
    estimated_daily_cost: float
    best_days_to_visit: int
    similar_destinations: List[str]
```

Recommended destination with scoring.

**Attributes:**
- `destination`: Destination object
- `match_score`: Match percentage (0-100)
- `reasons`: List of recommendation reasons
- `estimated_daily_cost`: Daily cost estimate
- `best_days_to_visit`: Recommended number of days
- `similar_destinations`: List of similar alternatives

---

## Services

### GoogleAPIService

Service for Google Maps API integration.

#### Constructor

```python
def __init__(self, api_key: Optional[str] = None)
```

**Parameters:**
- `api_key` (str, optional): Google Maps API key. Uses GOOGLE_MAPS_API_KEY env var if not provided.

#### search_places()

```python
def search_places(
    query: str,
    location: str,
    radius: int = 50000
) -> List[Dict]
```

Search for places using Google Places API.

**Parameters:**
- `query` (str): Search query (e.g., "restaurants")
- `location` (str): Location to search
- `radius` (int): Search radius in meters

**Returns:**
- `List[Dict]`: List of place results

#### get_distance_matrix()

```python
def get_distance_matrix(
    origins: List[str],
    destinations: List[str],
    mode: str = "driving"
) -> Dict
```

Get distance and duration between locations.

**Parameters:**
- `origins` (List[str]): Origin addresses
- `destinations` (List[str]): Destination addresses
- `mode` (str): Travel mode ("driving", "walking", "transit", "bicycling")

**Returns:**
- `Dict`: Distance matrix results

#### geocode_location()

```python
def geocode_location(location: str) -> Optional[Dict]
```

Get coordinates for a location.

**Parameters:**
- `location` (str): Location address

**Returns:**
- `Optional[Dict]`: Geocoding result with coordinates

#### get_attractions()

```python
def get_attractions(
    location: str,
    radius: int = 50000
) -> List[Dict]
```

Get attractions at a location.

---

## Exceptions

### ValueError

Raised for invalid input parameters:
- Invalid dates (end before start)
- Invalid budget (zero or negative)
- Missing required fields

### Exception

General exceptions from orchestration or API calls.

---

## Response Examples

### Trip Plan Response

```json
{
  "preferences": {
    "destinations": ["Paris", "London"],
    "start_date": "2024-06-01",
    "end_date": "2024-06-10",
    "budget": 3000,
    "travel_style": "comfort",
    "interests": ["culture", "food"],
    "number_of_travelers": 2,
    "duration_days": 9
  },
  "destination_recommendations": [
    {
      "name": "Paris",
      "country": "France",
      "match_score": 92.5,
      "estimated_daily_cost": 100,
      "best_days_to_visit": 5,
      "attractions": ["Eiffel Tower", "Louvre", "Notre-Dame"],
      "reasons": [
        "Excellent match for your preferences",
        "Fits within your budget",
        "Best season: April-May, September-October"
      ]
    }
  ],
  "itinerary": {
    "destinations": ["Paris", "London"],
    "total_duration": 9,
    "total_estimated_cost": 2700,
    "daily_plans": [...]
  },
  "budget_breakdown": {
    "total_budget": 3000,
    "recommendations": [...]
  }
}
```

---

For more information, see:
- [README.md](../README.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [USAGE_GUIDE.md](USAGE_GUIDE.md)
