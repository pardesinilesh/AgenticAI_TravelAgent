# Travel Planning Agent System - Usage Guide

This guide provides comprehensive examples and best practices for using the Travel Planning Agent System.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Usage](#advanced-usage)
3. [Integration Examples](#integration-examples)
4. [Customization](#customization)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Basic Usage

### Simple Trip Planning

The simplest way to plan a trip:

```python
from travel_agents.orchestrator import TravelPlanningOrchestrator
from datetime import date

# Create orchestrator
orchestrator = TravelPlanningOrchestrator(use_google_api=False)

# Plan trip
trip_plan = orchestrator.plan_trip(
    destinations=["Paris", "London", "Amsterdam"],
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 14),
    budget=3500,
    travel_style="comfort",
    interests=["culture", "food"],
    number_of_travelers=2
)

# Print results
orchestrator.print_trip_plan(trip_plan)
```

### Using with Google API

To use real-time data from Google Maps:

```python
import os
from travel_agents.orchestrator import TravelPlanningOrchestrator

# Ensure API key is set
os.environ['GOOGLE_MAPS_API_KEY'] = 'your-api-key'

# Create orchestrator with Google API enabled
orchestrator = TravelPlanningOrchestrator(use_google_api=True)

# Plan trip as usual - real data will be used
trip_plan = orchestrator.plan_trip(
    destinations=["Paris", "Berlin", "Prague"],
    start_date=date(2024, 7, 1),
    end_date=date(2024, 7, 10),
    budget=4000,
    travel_style="comfort",
    interests=["culture", "history"],
    number_of_travelers=2
)
```

## Advanced Usage

### Using Individual Agents

You can use agents independently:

#### Destination Recommender Only

```python
from travel_agents.agents.destination_recommender_agent import DestinationRecommenderAgent
from travel_agents.models.travel_plan import TravelPreferences
from datetime import date

# Create agent
agent = DestinationRecommenderAgent()

# Create preferences
preferences = TravelPreferences(
    destinations=["Paris", "London", "Amsterdam", "Barcelona", "Rome"],
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 15),
    budget=3000,
    travel_style="comfort",
    interests=["culture", "food", "history"],
    number_of_travelers=2
)

# Get recommendations
recommendations = agent.run(preferences)

# View results
for rec in recommendations:
    print(f"{rec.destination.name}: {rec.match_score}% match")
    print(f"  Reasons: {', '.join(rec.reasons[:2])}")
    print()
```

#### Itinerary Planner Only

```python
from travel_agents.agents.itinerary_planner_agent import ItineraryPlannerAgent

# Create agent
agent = ItineraryPlannerAgent()

# Create input
input_data = {
    'preferences': preferences,
    'selected_destinations': ['Paris', 'London', 'Amsterdam']
}

# Get itinerary
itinerary = agent.run(input_data)

# View daily plans
for day in itinerary.days[:3]:  # First 3 days
    print(f"\n{day.date} - {day.location}")
    for activity in day.activities:
        print(f"  • {activity.name} ({activity.duration_hours}h, ${activity.estimated_cost})")
```

#### Budget Optimizer Only

```python
from travel_agents.agents.budget_optimizer_agent import BudgetOptimizerAgent

# Create agent
agent = BudgetOptimizerAgent()

# Create input
input_data = {
    'itinerary': itinerary,
    'total_budget': 3000
}

# Optimize budget
breakdown = agent.run(input_data)

# View breakdown
print(f"Total Budget: ${breakdown.total_budget}")
print(f"Transportation: ${breakdown.transportation:.2f}")
print(f"Accommodation: ${breakdown.accommodation:.2f}")
print(f"Activities: ${breakdown.activities:.2f}")
print(f"Dining: ${breakdown.dining:.2f}")
print(f"Emergency Buffer: ${breakdown.emergency_buffer:.2f}")
print(f"Remaining: ${breakdown.remaining_buffer:.2f}")
print("\nRecommendations:")
for rec in breakdown.recommendations:
    print(f"  • {rec}")
```

## Integration Examples

### REST API Integration

```python
from flask import Flask, request, jsonify
from travel_agents.orchestrator import TravelPlanningOrchestrator
from datetime import datetime

app = Flask(__name__)
orchestrator = TravelPlanningOrchestrator(use_google_api=True)

@app.route('/plan-trip', methods=['POST'])
def plan_trip():
    """API endpoint for trip planning."""
    data = request.json
    
    try:
        trip_plan = orchestrator.plan_trip(
            destinations=data.get('destinations', []),
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date(),
            budget=float(data.get('budget', 0)),
            travel_style=data.get('travel_style', 'comfort'),
            interests=data.get('interests', []),
            number_of_travelers=int(data.get('number_of_travelers', 1))
        )
        
        return jsonify(trip_plan), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### CLI Application

```python
import click
from datetime import datetime
from travel_agents.orchestrator import TravelPlanningOrchestrator

@click.command()
@click.option('--destinations', required=True, help='Comma-separated destinations')
@click.option('--start-date', required=True, help='Start date (YYYY-MM-DD)')
@click.option('--end-date', required=True, help='End date (YYYY-MM-DD)')
@click.option('--budget', required=True, type=float, help='Total budget in USD')
@click.option('--style', default='comfort', help='Travel style: luxury, budget, comfort')
@click.option('--interests', default='culture,food', help='Comma-separated interests')
@click.option('--travelers', default=1, type=int, help='Number of travelers')
def plan_trip(destinations, start_date, end_date, budget, style, interests, travelers):
    """Plan a trip using the Travel Planning Agent System."""
    
    orchestrator = TravelPlanningOrchestrator(use_google_api=False)
    
    trip_plan = orchestrator.plan_trip(
        destinations=destinations.split(','),
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
        budget=budget,
        travel_style=style,
        interests=interests.split(','),
        number_of_travelers=travelers
    )
    
    orchestrator.print_trip_plan(trip_plan)
    orchestrator.save_plan_to_file(trip_plan, f'trip_{start_date}.json')

if __name__ == '__main__':
    plan_trip()
```

### Batch Processing

```python
import json
from datetime import date
from travel_agents.orchestrator import TravelPlanningOrchestrator

def batch_plan_trips(trips_config_file):
    """Plan multiple trips from a configuration file."""
    
    orchestrator = TravelPlanningOrchestrator(use_google_api=False)
    
    with open(trips_config_file, 'r') as f:
        trips = json.load(f)
    
    results = []
    for trip_config in trips:
        print(f"Planning trip: {trip_config['name']}")
        
        trip_plan = orchestrator.plan_trip(
            destinations=trip_config['destinations'],
            start_date=date.fromisoformat(trip_config['start_date']),
            end_date=date.fromisoformat(trip_config['end_date']),
            budget=trip_config['budget'],
            travel_style=trip_config.get('travel_style', 'comfort'),
            interests=trip_config.get('interests', []),
            number_of_travelers=trip_config.get('number_of_travelers', 1)
        )
        
        results.append({
            'name': trip_config['name'],
            'plan': trip_plan
        })
    
    return results
```

## Customization

### Creating Custom Agents

```python
from travel_agents.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    """Custom agent extending the base agent."""
    
    def __init__(self):
        super().__init__("CustomAgent")
    
    def validate_input(self, input_data) -> bool:
        """Validate input data."""
        return isinstance(input_data, dict) and 'required_field' in input_data
    
    def process(self, input_data):
        """Process input and return output."""
        self.logger.info("Processing custom agent input")
        # Your custom logic here
        return {'result': 'custom output'}
```

### Customizing Scoring Algorithm

```python
from travel_agents.agents.destination_recommender_agent import DestinationRecommenderAgent

class CustomRecommenderAgent(DestinationRecommenderAgent):
    """Custom recommender with modified scoring."""
    
    def calculate_match_score(self, destination, preferences):
        """Override the match score calculation."""
        score = 0.0
        
        # Custom weights
        score += 50  # Base score
        
        # Custom budget calculation
        if destination.estimated_cost_per_day < preferences.budget / 10:
            score += 40
        
        # Custom interest matching
        score += 10  # Bonus for any destination
        
        return min(100, score)
```

## Best Practices

### 1. Error Handling

```python
from travel_agents.orchestrator import TravelPlanningOrchestrator

try:
    orchestrator = TravelPlanningOrchestrator()
    trip_plan = orchestrator.plan_trip(...)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2. Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get logger for your code
logger = logging.getLogger(__name__)
```

### 3. Performance Optimization

```python
# Cache results if planning multiple trips
from functools import lru_cache

@lru_cache(maxsize=128)
def get_destination_info(destination_name):
    orchestrator = TravelPlanningOrchestrator()
    # Get info
    return orchestrator.destination_recommender
```

### 4. Input Validation

```python
from datetime import date
from travel_agents.models.travel_plan import TravelPreferences

def validate_trip_input(destinations, start_date, end_date, budget):
    """Validate trip input parameters."""
    
    if not destinations or len(destinations) == 0:
        raise ValueError("At least one destination required")
    
    if end_date <= start_date:
        raise ValueError("End date must be after start date")
    
    if budget <= 0:
        raise ValueError("Budget must be positive")
    
    if (end_date - start_date).days < 2:
        raise ValueError("Trip duration must be at least 2 days")
    
    return True
```

## Troubleshooting

### Google API Key Issues

```python
import os

# Check if API key is set
if 'GOOGLE_MAPS_API_KEY' not in os.environ:
    print("Warning: GOOGLE_MAPS_API_KEY not set")
    print("Using fallback/mock data")

# Or set it programmatically
os.environ['GOOGLE_MAPS_API_KEY'] = 'your-key'
```

### Handling Missing Destinations

```python
from travel_agents.agents.destination_recommender_agent import DestinationRecommenderAgent

agent = DestinationRecommenderAgent()

# Check if destination exists in database
if destination_name not in [d.name for d in agent.destinations]:
    print(f"Warning: {destination_name} not in database")
    print("Using closest match or generic recommendations")
```

### Memory Usage

```python
# For large trip plans, use generators
def process_large_trips(trips_list):
    for trip in trips_list:
        trip_plan = orchestrator.plan_trip(**trip)
        yield trip_plan
        # Process and clear memory
```

### Debugging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed output
orchestrator = TravelPlanningOrchestrator(use_google_api=False)
trip_plan = orchestrator.plan_trip(...)

# Check specific components
print("Destination recommendations:", len(trip_plan['destination_recommendations']))
print("Itinerary days:", len(trip_plan['itinerary']['daily_plans']))
print("Budget recommendations:", len(trip_plan['budget_breakdown']['recommendations']))
```

## Examples File

See `examples/` directory for complete working examples:
- `basic_usage.py` - Simple trip planning
- `advanced_usage.py` - Complex scenarios
- `batch_processing.py` - Multiple trips
- `api_server.py` - REST API implementation

---

For more information, see the [README.md](../README.md) and [ARCHITECTURE.md](ARCHITECTURE.md).
