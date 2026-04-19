# Copilot Instructions for Travel Planning Agent System

## Project Overview

The Travel Planning Agent System is a sophisticated multi-agent travel planning application built with Python. It consists of three autonomous agents that work together to provide travel recommendations, create detailed itineraries, and optimize budgets.

## Project Type

- **Language**: Python 3.8+
- **Architecture**: Multi-agent orchestration pattern
- **Purpose**: Travel planning using AI agents and Google Maps integration

## Key Components

### 1. Agents (3 Core Agents)
- **Destination Recommender Agent**: Analyzes user preferences and recommends suitable destinations with match scoring
- **Itinerary Planner Agent**: Creates day-by-day travel itineraries with activities and accommodations
- **Budget Optimizer Agent**: Analyzes trip costs and provides budget optimization recommendations

### 2. Data Models
- TravelPreferences: User travel requirements
- Destination: Destination information
- Activity: Individual activities
- TravelItinerary: Complete travel plan
- BudgetBreakdown: Cost analysis

### 3. Services
- GoogleAPIService: Integration with Google Maps, Places, and Distance Matrix APIs

### 4. Orchestrator
- TravelPlanningOrchestrator: Coordinates all agents and manages data flow

## Project Structure

```
travel_agents/
├── agents/              # 3 autonomous agents
├── models/              # Data models
├── services/            # Google API integration
├── orchestrator.py      # Main coordination engine
docs/
├── ARCHITECTURE.md      # Architecture documentation
├── API_REFERENCE.md     # Complete API reference
├── USAGE_GUIDE.md       # Usage examples
├── architecture.puml    # PlantUML architecture diagram
├── sequence.puml        # PlantUML sequence diagram
├── classes.puml         # PlantUML class diagram
requirements.txt         # Python dependencies
README.md               # Project README
```

## Design Patterns Used

1. **Agent Pattern**: Each agent is independent and focuses on a specific domain
2. **Orchestrator Pattern**: Coordinates between multiple agents
3. **Data Model Pattern**: Strongly typed dataclasses for clear data flow
4. **Strategy Pattern**: Different algorithms for recommendations and optimization

## Key Features

- ✅ Intelligent destination scoring (budget, style, interests)
- ✅ Detailed daily itinerary planning
- ✅ Comprehensive budget analysis with recommendations
- ✅ Google Maps API integration (places, distances, geocoding)
- ✅ Graceful fallback to mock data without API
- ✅ JSON export functionality
- ✅ Comprehensive error handling and logging

## Dependencies

- googlemaps: Google Maps API client
- requests: HTTP library
- python-dotenv: Environment management

## Configuration

### Environment Variables
```
GOOGLE_MAPS_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

## Quick Start

```python
from travel_agents.orchestrator import TravelPlanningOrchestrator
from datetime import date

orchestrator = TravelPlanningOrchestrator(use_google_api=False)

trip_plan = orchestrator.plan_trip(
    destinations=["Paris", "London", "Amsterdam"],
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 14),
    budget=3500,
    travel_style="comfort",
    interests=["culture", "food"],
    number_of_travelers=2
)

orchestrator.print_trip_plan(trip_plan)
```

## Documentation Files

- **ARCHITECTURE.md**: Detailed system architecture with data flow diagrams
- **API_REFERENCE.md**: Complete API documentation for all classes and methods
- **USAGE_GUIDE.md**: Comprehensive usage examples and integration patterns
- **PlantUML Diagrams**: 
  - architecture.puml: Component and deployment diagram
  - sequence.puml: Interaction sequence diagram
  - classes.puml: Class structure and relationships

## Code Quality Guidelines

1. **Type Hints**: All functions use Python type hints
2. **Documentation**: Comprehensive docstrings for all public methods
3. **Error Handling**: Graceful error handling with logging
4. **Dataclasses**: Use of dataclasses for data models
5. **Logging**: Structured logging for debugging and monitoring

## Important Notes

- System works WITH or WITHOUT Google API (graceful fallback)
- All agents are independent and can be used separately
- Strong input validation at orchestrator and agent levels
- Comprehensive logging for debugging
- Extensible design for adding new agents or algorithms

## Recent Changes

- Created complete project structure with 3 agents
- Implemented destination scoring algorithm
- Built itinerary planning with activity generation
- Developed budget analysis with optimization recommendations
- Integrated Google Maps API service
- Created comprehensive documentation with PlantUML diagrams
- Added error handling and logging throughout

## Next Steps for Enhancement

1. Add machine learning for personalized recommendations
2. Implement real-time flight price tracking
3. Add weather forecasting integration
4. Create mobile app integration
5. Build REST API service layer
6. Add collaborative planning features
7. Implement caching for performance optimization

## Testing

Run the demo:
```bash
python travel_agents/orchestrator.py
```

This generates a sample trip plan and saves it to `trip_plan.json`.

---

For detailed information, see the documentation files in the docs/ directory.
