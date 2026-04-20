# Travel Planning System Testing Guide

All tests for the travel planning system are located in the `testing/` folder. This guide explains how to run the tests and interpret results.

## Quick Start

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file with a valid Google Maps API key.
3. Run all tests:
   ```bash
   bash testing/run_tests.sh
   ```

## Test Files
- `test_different_example.py`: Scenario-based test for a family trip.
- `test_location_accuracy.py`: Ensures hotel-city assignment accuracy.
- `run_tests.sh`: Shell script to run all tests.
- `TEST_SCENARIOS.md`: Documentation of all test scenarios.

## Adding New Tests
- Place all new test scripts in the `testing/` folder.
- Update `TEST_SCENARIOS.md` with a description of each new scenario.

## Notes
- All tests use live data if `use_google_api=True`.
- For best results, ensure your API key quota is sufficient.
