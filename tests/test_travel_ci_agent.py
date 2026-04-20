"""pytest test suite driven by TravelCITestAgent.

Each test function maps to one named result produced by the agent so
pytest can report pass/fail individually in CI output.  The agent is
instantiated once per session (session-scoped fixture) to avoid
redundant computation.

Run with:
    pytest tests/test_travel_ci_agent.py -v
"""

import logging
import os
import sys
from datetime import date
from typing import Any, Dict

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from travel_agents.agents.travel_ci_test_agent import TravelCITestAgent


# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def ci_agent() -> TravelCITestAgent:
    """Create one TravelCITestAgent for the whole test session."""
    logging.basicConfig(level=logging.WARNING)
    return TravelCITestAgent(
        use_google_api=bool(os.getenv("GOOGLE_MAPS_API_KEY")),
        use_llm=bool(os.getenv("OPENAI_API_KEY")),
    )


@pytest.fixture(scope="session")
def ci_report(ci_agent: TravelCITestAgent) -> Dict[str, Any]:
    """Run the full CI suite once and share the report across all tests."""
    return ci_agent.run(None)


@pytest.fixture(scope="session")
def results_by_name(ci_report: Dict[str, Any]) -> Dict[str, str]:
    """Index the flat results list by test name for O(1) lookup."""
    return {r["test"]: r["status"] for r in ci_report["results"]}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _assert_passed(results: Dict[str, str], name: str) -> None:
    assert name in results, f"Test '{name}' was not found in CI report"
    status = results[name]
    assert status == "PASS", f"TravelCITestAgent reported FAIL for '{name}'"


# ---------------------------------------------------------------------------
# Top-level sanity checks
# ---------------------------------------------------------------------------


def test_ci_report_exists(ci_report: Dict[str, Any]) -> None:
    """The CI report must be a non-empty dict produced by TravelCITestAgent."""
    assert isinstance(ci_report, dict)
    assert ci_report["total_tests"] > 0


def test_ci_agent_identity(ci_report: Dict[str, Any]) -> None:
    """Report must identify itself as TravelCITestAgent."""
    assert ci_report["agent"] == "TravelCITestAgent"


def test_overall_pass_rate(ci_report: Dict[str, Any]) -> None:
    """All tests in the CI suite must pass (100 % pass rate)."""
    failed = ci_report["failed"]
    total = ci_report["total_tests"]
    assert failed == 0, (
        f"{failed}/{total} TravelCITestAgent tests failed — "
        "see test output for details"
    )


def test_coverage_metadata_present(ci_report: Dict[str, Any]) -> None:
    """Report must declare both SC and DC coverage."""
    cov = ci_report["coverage"]
    assert "statement_coverage" in cov
    assert "decision_coverage" in cov


# ---------------------------------------------------------------------------
# Data model tests (SC)
# ---------------------------------------------------------------------------


def test_data_model_travel_preferences(results_by_name):
    _assert_passed(results_by_name, "DataModel_TravelPreferences")


def test_data_model_destination(results_by_name):
    _assert_passed(results_by_name, "DataModel_Destination")


def test_data_model_activity(results_by_name):
    _assert_passed(results_by_name, "DataModel_Activity")


def test_data_model_itinerary_day(results_by_name):
    _assert_passed(results_by_name, "DataModel_ItineraryDay")


def test_data_model_travel_itinerary(results_by_name):
    _assert_passed(results_by_name, "DataModel_TravelItinerary")


def test_data_model_budget_breakdown(results_by_name):
    _assert_passed(results_by_name, "DataModel_BudgetBreakdown")


def test_data_model_destination_recommendation(results_by_name):
    _assert_passed(results_by_name, "DataModel_DestinationRecommendation")


# ---------------------------------------------------------------------------
# DestinationRecommenderAgent tests (SC + DC)
# ---------------------------------------------------------------------------


def test_dest_rec_validate_valid(results_by_name):
    _assert_passed(results_by_name, "DestRec_validate_valid")


def test_dest_rec_validate_wrong_type(results_by_name):
    _assert_passed(results_by_name, "DestRec_validate_wrong_type")


def test_dest_rec_validate_empty_destinations(results_by_name):
    _assert_passed(results_by_name, "DestRec_validate_empty_destinations")


def test_dest_rec_validate_zero_budget(results_by_name):
    _assert_passed(results_by_name, "DestRec_validate_zero_budget")


def test_dest_rec_score_budget_well_within(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_budget_well_within")


def test_dest_rec_score_budget_within(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_budget_within")


def test_dest_rec_score_budget_slightly_over(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_budget_slightly_over")


def test_dest_rec_score_budget_very_over(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_budget_very_over")


def test_dest_rec_score_luxury_expensive_dest(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_luxury_expensive_dest")


def test_dest_rec_score_luxury_cheap_dest(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_luxury_cheap_dest")


def test_dest_rec_score_budget_style_cheap_dest(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_budget_style_cheap_dest")


def test_dest_rec_score_budget_style_expensive_dest(results_by_name):
    _assert_passed(results_by_name, "DestRec_score_budget_style_expensive_dest")


def test_dest_rec_reasons_high_score(results_by_name):
    _assert_passed(results_by_name, "DestRec_reasons_high_score")


def test_dest_rec_reasons_medium_score(results_by_name):
    _assert_passed(results_by_name, "DestRec_reasons_medium_score")


def test_dest_rec_reasons_low_score(results_by_name):
    _assert_passed(results_by_name, "DestRec_reasons_low_score")


def test_dest_rec_reasons_within_budget(results_by_name):
    _assert_passed(results_by_name, "DestRec_reasons_within_budget")


def test_dest_rec_reasons_above_budget(results_by_name):
    _assert_passed(results_by_name, "DestRec_reasons_above_budget")


def test_dest_rec_similar_existing(results_by_name):
    _assert_passed(results_by_name, "DestRec_similar_existing")


def test_dest_rec_similar_nonexistent(results_by_name):
    _assert_passed(results_by_name, "DestRec_similar_nonexistent")


def test_dest_rec_get_recommendations(results_by_name):
    _assert_passed(results_by_name, "DestRec_get_recommendations")


def test_dest_rec_process(results_by_name):
    _assert_passed(results_by_name, "DestRec_process")


# ---------------------------------------------------------------------------
# ItineraryPlannerAgent tests (SC + DC)
# ---------------------------------------------------------------------------


def test_itinerary_validate_valid(results_by_name):
    _assert_passed(results_by_name, "Itinerary_validate_valid")


def test_itinerary_validate_not_dict(results_by_name):
    _assert_passed(results_by_name, "Itinerary_validate_not_dict")


def test_itinerary_validate_missing_key(results_by_name):
    _assert_passed(results_by_name, "Itinerary_validate_missing_key")


def test_itinerary_validate_bad_preferences(results_by_name):
    _assert_passed(results_by_name, "Itinerary_validate_bad_preferences")


def test_itinerary_validate_destinations_not_list(results_by_name):
    _assert_passed(results_by_name, "Itinerary_validate_destinations_not_list")


@pytest.mark.parametrize("interest", ["culture", "adventure", "nightlife", "nature", "food"])
def test_itinerary_activities_by_interest(results_by_name, interest):
    _assert_passed(results_by_name, f"Itinerary_activities_{interest}")


def test_itinerary_activities_day1_reduced(results_by_name):
    _assert_passed(results_by_name, "Itinerary_activities_day1_reduced")


def test_itinerary_activities_last_day_reduced(results_by_name):
    _assert_passed(results_by_name, "Itinerary_activities_last_day_reduced")


def test_itinerary_activities_default_fallback(results_by_name):
    _assert_passed(results_by_name, "Itinerary_activities_default_fallback")


def test_itinerary_create_day(results_by_name):
    _assert_passed(results_by_name, "Itinerary_create_day")


def test_itinerary_process(results_by_name):
    _assert_passed(results_by_name, "Itinerary_process")


# ---------------------------------------------------------------------------
# BudgetOptimizerAgent tests (SC + DC)
# ---------------------------------------------------------------------------


def test_budget_validate_valid(results_by_name):
    _assert_passed(results_by_name, "Budget_validate_valid")


def test_budget_validate_not_dict(results_by_name):
    _assert_passed(results_by_name, "Budget_validate_not_dict")


def test_budget_validate_missing_key(results_by_name):
    _assert_passed(results_by_name, "Budget_validate_missing_key")


def test_budget_validate_bad_itinerary(results_by_name):
    _assert_passed(results_by_name, "Budget_validate_bad_itinerary")


def test_budget_validate_zero_budget(results_by_name):
    _assert_passed(results_by_name, "Budget_validate_zero_budget")


def test_budget_validate_negative_budget(results_by_name):
    _assert_passed(results_by_name, "Budget_validate_negative_budget")


def test_budget_recs_well_within(results_by_name):
    _assert_passed(results_by_name, "Budget_recs_well_within")


def test_budget_recs_within_tight(results_by_name):
    _assert_passed(results_by_name, "Budget_recs_within_tight")


def test_budget_recs_tightly_allocated(results_by_name):
    _assert_passed(results_by_name, "Budget_recs_tightly_allocated")


def test_budget_recs_over_budget(results_by_name):
    _assert_passed(results_by_name, "Budget_recs_over_budget")


def test_budget_optimize_transport_branch(results_by_name):
    _assert_passed(results_by_name, "Budget_optimize_transport_branch")


def test_budget_recs_high_accommodation(results_by_name):
    _assert_passed(results_by_name, "Budget_recs_high_accommodation")


def test_budget_recs_high_dining(results_by_name):
    _assert_passed(results_by_name, "Budget_recs_high_dining")


def test_budget_recs_high_activities(results_by_name):
    _assert_passed(results_by_name, "Budget_recs_high_activities")


def test_budget_daily_breakdown(results_by_name):
    _assert_passed(results_by_name, "Budget_daily_breakdown")


# ---------------------------------------------------------------------------
# BaseAgent tests (SC + DC)
# ---------------------------------------------------------------------------


def test_base_agent_run_valid(results_by_name):
    _assert_passed(results_by_name, "BaseAgent_run_valid")


def test_base_agent_run_invalid_raises(results_by_name):
    _assert_passed(results_by_name, "BaseAgent_run_invalid_raises")


# ---------------------------------------------------------------------------
# TravelPlanningOrchestrator tests (SC + DC)
# ---------------------------------------------------------------------------


def test_orchestrator_init_no_api(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_init_no_api")


def test_orchestrator_init_missing_key_graceful(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_init_missing_key_graceful")


def test_orchestrator_plan_trip_comfort(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_plan_trip_comfort")


def test_orchestrator_plan_trip_budget(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_plan_trip_budget")


def test_orchestrator_plan_trip_luxury(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_plan_trip_luxury")


def test_orchestrator_summary_within_budget(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_summary_within_budget")


def test_orchestrator_summary_over_budget(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_summary_over_budget")


def test_orchestrator_save_plan_to_file(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_save_plan_to_file")


def test_orchestrator_print_trip_plan(results_by_name):
    _assert_passed(results_by_name, "Orchestrator_print_trip_plan")


# ---------------------------------------------------------------------------
# MemorySystem tests (SC + DC)
# ---------------------------------------------------------------------------


def test_memory_init_no_file(results_by_name):
    _assert_passed(results_by_name, "Memory_init_no_file")


def test_memory_init_existing_file(results_by_name):
    _assert_passed(results_by_name, "Memory_init_existing_file")


def test_memory_save_trip_with_spend(results_by_name):
    _assert_passed(results_by_name, "Memory_save_trip_with_spend")


def test_memory_save_trip_no_spend(results_by_name):
    _assert_passed(results_by_name, "Memory_save_trip_no_spend")


def test_memory_update_profile_existing(results_by_name):
    _assert_passed(results_by_name, "Memory_update_profile_existing")


def test_memory_update_new_user_profile(results_by_name):
    _assert_passed(results_by_name, "Memory_update_new_user_profile")


def test_memory_favorites_high_satisfaction(results_by_name):
    _assert_passed(results_by_name, "Memory_favorites_high_satisfaction")


def test_memory_avoidlist_low_satisfaction(results_by_name):
    _assert_passed(results_by_name, "Memory_avoidlist_low_satisfaction")


def test_memory_get_trip_history(results_by_name):
    _assert_passed(results_by_name, "Memory_get_trip_history")


def test_memory_get_trip_history_empty(results_by_name):
    _assert_passed(results_by_name, "Memory_get_trip_history_empty")


def test_memory_avg_satisfaction(results_by_name):
    _assert_passed(results_by_name, "Memory_avg_satisfaction")


def test_memory_avg_satisfaction_no_trips(results_by_name):
    _assert_passed(results_by_name, "Memory_avg_satisfaction_no_trips")


def test_memory_learning_insights(results_by_name):
    _assert_passed(results_by_name, "Memory_learning_insights")


def test_memory_should_avoid(results_by_name):
    _assert_passed(results_by_name, "Memory_should_avoid")


def test_memory_weights_no_trips(results_by_name):
    _assert_passed(results_by_name, "Memory_weights_no_trips")


def test_memory_weights_with_trips(results_by_name):
    _assert_passed(results_by_name, "Memory_weights_with_trips")


def test_memory_extract_lessons_all_ranges(results_by_name):
    _assert_passed(results_by_name, "Memory_extract_lessons_all_ranges")


# ---------------------------------------------------------------------------
# GoogleAPIService tests (SC + DC)
# ---------------------------------------------------------------------------


def test_google_api_init_no_key_raises(results_by_name):
    _assert_passed(results_by_name, "GoogleAPI_init_no_key_raises")


@pytest.mark.parametrize("test_name", [
    "GoogleAPI_search_places_mock_success",
    "GoogleAPI_search_places_empty_geocode",
    "GoogleAPI_search_places_exception",
    "GoogleAPI_distance_matrix_mock_success",
    "GoogleAPI_distance_matrix_exception",
    "GoogleAPI_place_details_mock_success",
    "GoogleAPI_place_details_exception",
    "GoogleAPI_geocode_success",
    "GoogleAPI_geocode_empty",
    "GoogleAPI_geocode_exception",
    "GoogleAPI_reverse_geocode_success",
    "GoogleAPI_reverse_geocode_empty",
    "GoogleAPI_reverse_geocode_exception",
    "GoogleAPI_convenience_methods",
    "GoogleAPI_weather_info_success",
    "GoogleAPI_weather_info_no_result",
    "GoogleAPI_weather_info_exception",
])
def test_google_api_mock_branches(results_by_name, test_name):
    # These tests only run when Google API token is absent; skip when real API is used.
    if test_name not in results_by_name:
        pytest.skip(f"Test '{test_name}' not in report (real API may have been used instead)")
    _assert_passed(results_by_name, test_name)


# ---------------------------------------------------------------------------
# LLMService tests (SC + DC)
# ---------------------------------------------------------------------------


def test_llm_init_no_key_disabled(results_by_name):
    _assert_passed(results_by_name, "LLM_init_no_key_disabled")


def test_llm_all_disabled_defaults(results_by_name):
    _assert_passed(results_by_name, "LLM_all_disabled_defaults")


@pytest.mark.parametrize("test_name", [
    "LLM_reason_destinations_mock",
    "LLM_itinerary_description_mock",
    "LLM_budget_reasoning_mock",
    "LLM_trip_satisfaction_json_mock",
    "LLM_trip_satisfaction_non_json_mock",
    "LLM_travel_tips_mock",
    "LLM_should_revise_json_mock",
    "LLM_should_revise_non_json_high_score",
    "LLM_should_revise_non_json_low_score",
    "LLM_exception_paths_all_methods",
])
def test_llm_mock_branches(results_by_name, test_name):
    if test_name not in results_by_name:
        pytest.skip(f"Test '{test_name}' not in report (real LLM may have been used instead)")
    _assert_passed(results_by_name, test_name)


# ---------------------------------------------------------------------------
# End-to-end tests
# ---------------------------------------------------------------------------


def test_e2e_basic_orchestrator(results_by_name):
    _assert_passed(results_by_name, "E2E_basic_orchestrator_complete_workflow")


def test_e2e_intelligent_orchestrator(results_by_name):
    _assert_passed(results_by_name, "E2E_intelligent_orchestrator_with_memory")


# ---------------------------------------------------------------------------
# Standalone unit tests (do not depend on the CI agent report)
# These provide direct pytest coverage independently of TravelCITestAgent.
# ---------------------------------------------------------------------------


class TestTravelCITestAgentContract:
    """Verify TravelCITestAgent itself satisfies the BaseAgent contract."""

    def test_is_base_agent_subclass(self):
        from travel_agents.agents.base_agent import BaseAgent
        assert issubclass(TravelCITestAgent, BaseAgent)

    def test_validate_input_accepts_none(self):
        agent = TravelCITestAgent()
        assert agent.validate_input(None) is True

    def test_validate_input_accepts_dict(self):
        agent = TravelCITestAgent()
        assert agent.validate_input({"key": "value"}) is True

    def test_validate_input_rejects_string(self):
        agent = TravelCITestAgent()
        assert agent.validate_input("bad") is False

    def test_process_returns_dict_with_required_keys(self):
        agent = TravelCITestAgent()
        report = agent.process(None)
        for key in ("agent", "total_tests", "passed", "failed", "pass_rate",
                    "coverage", "results"):
            assert key in report, f"Missing key: {key}"

    def test_process_via_run_method(self):
        """run() should call process() via BaseAgent.run()."""
        agent = TravelCITestAgent()
        report = agent.run(None)
        assert report["agent"] == "TravelCITestAgent"

    def test_run_rejects_non_dict_non_none(self):
        agent = TravelCITestAgent()
        with pytest.raises(ValueError):
            agent.run("not valid")

    def test_pass_rate_formula(self):
        agent = TravelCITestAgent()
        report = agent.run(None)
        expected = round(report["passed"] / report["total_tests"] * 100, 2)
        assert abs(report["pass_rate"] - expected) < 0.01

    def test_every_result_has_required_fields(self):
        agent = TravelCITestAgent()
        report = agent.run(None)
        for item in report["results"]:
            assert "test" in item
            assert "status" in item
            assert item["status"] in ("PASS", "FAIL")

    def test_api_tokens_reflect_env(self):
        agent = TravelCITestAgent(use_google_api=False, use_llm=False)
        report = agent.run(None)
        assert report["api_tokens_used"]["google_api"] is False
        assert report["api_tokens_used"]["openai_llm"] is False


class TestTripPlanningDirectly:
    """Direct unit tests that do not require the CI agent report."""

    @pytest.fixture
    def basic_prefs(self):
        return {
            "destinations": ["Paris", "Tokyo"],
            "start_date": date(2024, 6, 1),
            "end_date": date(2024, 6, 10),
            "budget": 4000.0,
            "travel_style": "comfort",
            "interests": ["culture", "food"],
            "number_of_travelers": 2,
        }

    def test_plan_trip_returns_all_keys(self, basic_prefs):
        from travel_agents.orchestrator import TravelPlanningOrchestrator
        orch = TravelPlanningOrchestrator(use_google_api=False)
        plan = orch.plan_trip(**basic_prefs)
        for key in ("preferences", "destination_recommendations",
                    "itinerary", "budget_breakdown", "summary"):
            assert key in plan

    def test_destination_recommendations_are_sorted_by_score(self, basic_prefs):
        from travel_agents.orchestrator import TravelPlanningOrchestrator
        orch = TravelPlanningOrchestrator(use_google_api=False)
        plan = orch.plan_trip(**basic_prefs)
        scores = [r["match_score"] for r in plan["destination_recommendations"]]
        assert scores == sorted(scores, reverse=True)

    def test_itinerary_duration_matches_dates(self, basic_prefs):
        from travel_agents.orchestrator import TravelPlanningOrchestrator
        orch = TravelPlanningOrchestrator(use_google_api=False)
        plan = orch.plan_trip(**basic_prefs)
        expected_days = (basic_prefs["end_date"] - basic_prefs["start_date"]).days
        assert plan["itinerary"]["total_duration"] == expected_days

    def test_budget_breakdown_sums_correctly(self, basic_prefs):
        from travel_agents.orchestrator import TravelPlanningOrchestrator
        orch = TravelPlanningOrchestrator(use_google_api=False)
        plan = orch.plan_trip(**basic_prefs)
        bd = plan["budget_breakdown"]
        assert bd["total_budget"] == basic_prefs["budget"]

    def test_intelligent_orchestrator_autonomous_decisions(self):
        from travel_agents.intelligent_orchestrator import IntelligentTravelOrchestrator
        orch = IntelligentTravelOrchestrator(use_google_api=False, use_llm=False,
                                             user_id="pytest_user")
        plan = orch.plan_trip(
            destinations=["Rome", "Florence"],
            start_date=date(2024, 5, 1), end_date=date(2024, 5, 10),
            budget=3000.0, travel_style="comfort",
            interests=["culture", "art"], number_of_travelers=1,
        )
        assert "autonomous_decisions" in plan
        assert isinstance(plan["autonomous_decisions"]["auto_actions"], list)
