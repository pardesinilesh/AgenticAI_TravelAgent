# Travel Planning Test Scenarios

This document describes the test scenarios used to validate the travel planning system with live data and user-requested destinations.

## Scenario 1: Family History & Fun (test_different_example.py)
- Destinations: Rome, Athens, Istanbul
- Dates: July 10–24, 2026
- Budget: $5000
- Style: family
- Interests: history, fun
- Travelers: 4
- **Validation:**
  - All days assigned to requested cities
  - Hotels in correct cities
  - Budget not exceeded

## Scenario 2: Hotel Location Accuracy (test_location_accuracy.py)
- Destinations: Berlin, Prague, Vienna
- Dates: August 1–10, 2026
- Budget: $3000
- Style: comfort
- Interests: art, architecture
- Travelers: 2
- **Validation:**
  - Each day’s hotel is in the correct city
  - No days assigned to cities outside the requested list

## How to Run
- Use `run_tests.sh` to execute all tests.
- All tests are in the `testing/` folder.

## Adding More Scenarios
- Add new test files in `testing/` following the above pattern.
- Document each scenario here for traceability.
