# Quick Start - Intelligent Travel Agents

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your keys:
GOOGLE_MAPS_API_KEY=your_key_here
OPENAI_API_KEY=your_openai_key_here
```

### 3. Run Demo
```bash
python travel_agents/intelligent_orchestrator.py
```

This will generate:
- An intelligent trip plan with all 5 components
- `intelligent_trip_plan.json` with complete output
- Console output showing AI reasoning at each step

---

## Basic Usage

### Simple Trip Planning with AI

```python
from travel_agents.intelligent_orchestrator import IntelligentTravelOrchestrator
from datetime import date

# Create orchestrator (user_id for personalization)
orchestrator = IntelligentTravelOrchestrator(
    use_google_api=False,
    use_llm=True,  # Enable AI reasoning
    user_id="john_doe"
)

# Plan trip
trip_plan = orchestrator.plan_trip(
    destinations=["Paris", "London", "Amsterdam"],
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 14),
    budget=4000,
    travel_style="comfort",
    interests=["culture", "food", "museums"],
    number_of_travelers=2
)

# See the results
orchestrator.print_trip_plan(trip_plan)

# Save to file
orchestrator.save_plan_to_file(trip_plan, "my_trip.json")
```

### Output Includes:
- ✅ AI-powered destination recommendations
- ✅ Predicted satisfaction score
- ✅ Autonomous decisions made
- ✅ Personalized suggestions
- ✅ Travel tips from LLM

---

## Advanced: Learning from Trips

```python
# After trip is completed
orchestrator.record_trip_completion(
    trip_id="paris_london_2024",
    trip_plan=trip_plan,
    satisfaction_score=9.0,
    feedback="Excellent! Paris was amazing, perfect pace.",
    actual_spend=3850
)

# System automatically:
#   ✓ Saves trip to memory (user_memory.json)
#   ✓ Updates user profile
#   ✓ Adjusts personalization weights
#   ✓ Extracts lessons learned

# Next trip will be MORE personalized!
trip_plan_2 = orchestrator.plan_trip(...)
# Now system understands what works for this user
```

---

## 5 Components Explained

### 1. LLM Integration

```python
from travel_agents.services.llm_service import LLMService

llm = LLMService()

# LLM reasons about destinations
insights = llm.reason_about_destinations(
    preferences={'budget': 5000, 'style': 'comfort'},
    destinations=['Paris', 'Tokyo']
)
```

**What it does:**
- Contextual reasoning about destination fit
- Creative itinerary descriptions
- Intelligent budget optimization
- Travel tips and advice

### 2. Machine Learning Personalization

```python
from travel_agents.services.personalization_engine import PersonalizationEngine

peng = PersonalizationEngine()

# Predict satisfaction for a plan
score, suggestions = peng.predict_satisfaction("john_doe", trip_plan)
# Returns: (8.5, ['Consider more budget for dining', ...])

# Learn from feedback
peng.learn_from_feedback("john_doe", 9.0, {
    'budget_respected': True,
    'style_matched': True
})
```

**What it does:**
- Adapts weights (budget, style, interests)
- Predicts trip satisfaction
- Recommends adjustments
- Improves with each trip

### 3. Memory & Context System

```python
from travel_agents.services.memory_system import MemorySystem

memory = MemorySystem()

# Get user profile
profile = memory.get_user_profile("john_doe")
# Returns: total_trips, preferences, favorites, avoided destinations

# Get trip history
history = memory.get_trip_history("john_doe")

# Check if should avoid destination
if memory.should_avoid_destination("john_doe", "Las Vegas"):
    print("User didn't like Vegas - avoid for recommendations")
```

**What it does:**
- Stores user history and preferences
- Tracks satisfaction scores
- Learns avoided destinations
- Extracts lessons from trips

### 4. Multi-Step Reasoning Chains

Orchestrator implements 5+ step reasoning:

```
Step 1: Generate 10 base recommendations (algorithm)
  ↓
Step 2: Use LLM to analyze all 10 (context-aware)
  ↓
Step 3: Re-score with personalized weights (ML)
  ↓
Step 4: Filter based on memory (history)
  ↓
Step 5: Rank with intelligent factors (synthesis)
  ↓
Return top 5 recommendations
```

Each step builds on previous, creating robust decisions.

### 5. Autonomous Decision-Making

System makes decisions without asking:

```python
# Autonomous checks:
- "Should we suggest alternatives for variety?" → AUTO DECIDED
- "Is itinerary pace too aggressive?" → AUTO FLAGGED
- "Should we revise budget?" → AUTO DETECTED
- "What did we learn from this trip?" → AUTO EXTRACTED
```

---

## Common Workflows

### Workflow 1: Plan Your First Trip

```python
orchestrator = IntelligentTravelOrchestrator(
    user_id="new_user"
)

# System uses defaults (no history yet)
plan_1 = orchestrator.plan_trip(
    destinations=["Paris", "Amsterdam"],
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 10),
    budget=3000,
    travel_style="comfort",
    interests=["culture", "food"],
    number_of_travelers=1
)

orchestrator.print_trip_plan(plan_1)
```

### Workflow 2: Learn & Improve (2nd Trip)

```python
# User completes trip 1
orchestrator.record_trip_completion(
    trip_id="trip_001",
    trip_plan=plan_1,
    satisfaction_score=8.0,
    feedback="Great! But too much in 9 days."
)

# System now KNOWS:
# - User enjoys this travel style
# - Prefers slower pace
# - Good budget allocation

# Plan trip 2 with improvements
plan_2 = orchestrator.plan_trip(
    destinations=["Tokyo", "Kyoto"],
    start_date=date(2024, 9, 1),
    end_date=date(2024, 9, 14),
    budget=3500,
    travel_style="comfort",
    interests=["culture", "food", "nature"],
    number_of_travelers=1
)

# Output will be MORE personalized
# Pace will be slower based on memory
# Weights will be adjusted (learned from feedback)
```

### Workflow 3: Group Travel

```python
# Planning for a group
# System creates separate profile per user_id
orchestrator = IntelligentTravelOrchestrator(user_id="shared_trip_123")

plan = orchestrator.plan_trip(
    destinations=["Barcelona", "Madrid"],
    start_date=date(2024, 7, 1),
    end_date=date(2024, 7, 7),
    budget=5000,  # Per person
    travel_style="adventure",
    interests=["nightlife", "beaches", "food"],
    number_of_travelers=4
)

# Recommends group-friendly activities
# Balances individual/group interests
```

---

## Comparison: Old vs New

### Old System (Rule-Based)
```
Input → Algorithm 1 → Algorithm 2 → Algorithm 3 → Static Output
```
- Always same results for same input
- No learning
- No context awareness
- Limited reasoning

### New System (Intelligent Agents)
```
Input → LLM → ML → Memory → Reasoning Chains → Autonomous Decisions → Output
                                                       ↓
                                                    Learning Loop
                                                       ↓
                                                   Next Trip Better
```
- Improves with each trip
- Context-aware reasoning
- Personalized to user
- Self-improving system

---

## Troubleshooting

### "OpenAI API Error"
```python
# Run without LLM (still works!)
orchestrator = IntelligentTravelOrchestrator(
    use_llm=False  # Falls back to regular reasoning
)
```

### "Google API Key Not Found"
```python
# Run without Google API (uses mock data)
orchestrator = IntelligentTravelOrchestrator(
    use_google_api=False
)
```

### "No learning happening?"
```python
# Make sure to record trip completion:
orchestrator.record_trip_completion(
    trip_id=trip_id,
    trip_plan=trip_plan,
    satisfaction_score=8.0
)

# Check user profile:
profile = orchestrator.memory_system.get_user_profile(user_id)
print(f"Total trips: {profile.total_trips}")
```

---

## Files Overview

| File | Purpose |
|------|---------|
| `intelligent_orchestrator.py` | Main coordinator with all 5 components |
| `agents/intelligent_agents.py` | Enhanced agents with reasoning |
| `services/llm_service.py` | LLM integration |
| `services/personalization_engine.py` | ML adaptive learning |
| `services/memory_system.py` | User history & context |
| `docs/INTELLIGENT_AGENTS_GUIDE.md` | Comprehensive guide (this file depth) |

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Set up API keys (.env file)
3. ✅ Run demo: `python travel_agents/intelligent_orchestrator.py`
4. ✅ Try basic usage with your preferences
5. ✅ Record trip completion and see learning
6. ✅ Plan second trip and see improvements

---

## Support

For detailed documentation, see:
- **INTELLIGENT_AGENTS_GUIDE.md** - Technical deep dive
- **API_REFERENCE.md** - API documentation
- **USAGE_GUIDE.md** - More examples
- **ARCHITECTURE.md** - System architecture

---

**Ready to see AI agents in action? Let's go! 🚀**
