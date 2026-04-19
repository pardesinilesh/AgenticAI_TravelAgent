# Travel Planning Agent System

## Architecture Overview

This is a comprehensive travel planning system that uses multiple autonomous agents to provide destination recommendations, create detailed itineraries, and optimize budgets.

### System Architecture

The system is built on a multi-agent orchestration pattern with the following components:

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface                               │
│                   (CLI / API / Web)                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Travel Planning Orchestrator                        │
│                  (orchestrator.py)                              │
└─┬─────────────────────────────────────────────────────┬──────┬─┘
  │                                                      │      │
  ▼                                                      ▼      ▼
┌─────────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ Destination Recommender │  │ Itinerary Planner    │  │ Budget Optimizer     │
│ Agent                   │  │ Agent                │  │ Agent                │
│                         │  │                      │  │                      │
│ • Scoring Algorithm     │  │ • Daily Activities   │  │ • Cost Analysis      │
│ • Preference Matching   │  │ • Route Planning     │  │ • Budget Breakdown   │
│ • Recommendations       │  │ • Transport Schedule │  │ • Recommendations    │
└──────────┬──────────────┘  └──────────┬───────────┘  └──────────┬───────────┘
           │                            │                         │
           └────────────────┬───────────┴────────────┬────────────┘
                            │                        │
                            ▼                        ▼
                   ┌────────────────────┐    ┌──────────────────┐
                   │ Data Models        │    │ Google API       │
                   │                    │    │ Service          │
                   │ • TravelPref...    │    │                  │
                   │ • Destination      │    │ • Places API     │
                   │ • Itinerary        │    │ • Distance API   │
                   │ • Budget           │    │ • Geocoding      │
                   └────────────────────┘    └──────────────────┘
```

## 3 Core Agents

### 1. **Destination Recommender Agent**
- **Purpose**: Analyze user preferences and recommend suitable destinations
- **Input**: Travel preferences (dates, budget, interests, style)
- **Output**: Ranked list of destination recommendations with match scores
- **Algorithm**: 
  - Budget compatibility (40%)
  - Travel style matching (30%)
  - Interest alignment (30%)

### 2. **Itinerary Planner Agent**
- **Purpose**: Create detailed day-by-day travel itinerary
- **Input**: Preferred destinations and travel preferences
- **Output**: Complete itinerary with daily activities, accommodations, costs
- **Features**:
  - Distributes destinations across trip duration
  - Creates context-aware activities
  - Includes transportation and accommodation

### 3. **Budget Optimizer Agent**
- **Purpose**: Analyze and optimize travel budget
- **Input**: Total itinerary and available budget
- **Output**: Budget breakdown and optimization recommendations
- **Features**:
  - Cost allocation across categories
  - Budget variance analysis
  - Cost-saving suggestions

## Data Flow

```
┌─────────────────────────┐
│  User Input             │
│  - Destinations         │
│  - Dates                │
│  - Budget               │
│  - Interests            │
│  - Travel Style         │
└────────────┬────────────┘
             │
             ▼
    ┌────────────────────┐
    │ Create User        │
    │ Preferences Object │
    └────────┬───────────┘
             │
             ▼
    ┌─────────────────────────────────┐
    │ Destination Recommender Agent   │
    │ ✓ Returns top 5 recommendations │
    └────────┬───────────────────────┘
             │
             ▼
    ┌─────────────────────────────────┐
    │ User Selects Top 3 Destinations │
    └────────┬───────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────┐
    │ Itinerary Planner Agent              │
    │ ✓ Returns detailed day-by-day travel │
    └────────┬─────────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────┐
    │ Budget Optimizer Agent               │
    │ ✓ Returns budget breakdown & suggestions│
    └────────┬─────────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────┐
    │ Complete Trip Plan (JSON)            │
    │ - Preferences                        │
    │ - Recommendations                    │
    │ - Itinerary                          │
    │ - Budget Analysis                    │
    └──────────────────────────────────────┘
```

## Project Structure

```
AgenticAL_Travelling_Assitance/
├── travel_agents/
│   ├── __init__.py
│   ├── orchestrator.py              # Main orchestration engine
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Abstract base class
│   │   ├── destination_recommender_agent.py
│   │   ├── itinerary_planner_agent.py
│   │   └── budget_optimizer_agent.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── travel_plan.py           # Data models
│   ├── services/
│   │   ├── __init__.py
│   │   └── google_api_service.py    # Google API integration
│   ├── utils/
│   │   └── __init__.py
│   └── utils/
├── docs/
│   ├── ARCHITECTURE.md              # This file
│   ├── API_REFERENCE.md
│   ├── USAGE_GUIDE.md
│   └── diagrams/
│       ├── architecture.puml
│       ├── sequence.puml
│       └── classes.puml
├── requirements.txt
├── .env.example
└── README.md
```

## Technology Stack

- **Language**: Python 3.8+
- **Dependencies**:
  - `googlemaps`: Google Maps API client
  - `requests`: HTTP library for API calls
  - `python-dotenv`: Environment variable management
- **APIs**:
  - Google Maps API (Places, Distance Matrix, Geocoding)

## Key Design Patterns

### 1. **Agent Pattern**
- Each agent is independent and focuses on a specific domain
- Follows Single Responsibility Principle
- Easy to extend with new agents

### 2. **Orchestrator Pattern**
- Coordinates between multiple agents
- Manages data flow
- Handles error cases

### 3. **Data Model Pattern**
- Strongly typed data models using dataclasses
- Clear separation of concerns
- Easy serialization to JSON

### 4. **Strategy Pattern**
- Different recommendation algorithms
- Budget optimization strategies
- Extensible for new strategies

## Integration Points

### Google Maps API
The system integrates with Google Maps API for:
- **Places API**: Search attractions, restaurants, hotels
- **Distance Matrix API**: Calculate travel times and distances
- **Geocoding API**: Convert addresses to coordinates

### Environment Configuration
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## Error Handling

The system implements comprehensive error handling:
- Input validation at the agent level
- Graceful degradation if Google API is unavailable
- Fallback to mock data for demonstration
- Detailed logging for debugging

## Future Enhancements

1. **Machine Learning Integration**
   - Personalized recommendations based on user history
   - Price prediction models
   - Popularity trends analysis

2. **Real-time Data**
   - Live flight prices
   - Weather forecasts
   - Currency conversion

3. **User Profiles**
   - Save and manage multiple itineraries
   - Learn from past trips
   - Collaborative planning

4. **Additional Agents**
   - Transport Booking Agent
   - Accommodation Agent
   - Travel Insurance Agent
   - Visa Requirements Agent

## Performance Considerations

- **Caching**: Cache destination database and API responses
- **Async Operations**: Use async calls for API requests
- **Pagination**: Handle large result sets from Google API
- **Rate Limiting**: Implement rate limiting for API calls

## Security Considerations

- Store API keys in environment variables (never in code)
- Validate all user inputs
- Use HTTPS for all API calls
- Implement request signing if needed
