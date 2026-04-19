"""Budget Optimizer Agent for travel planning."""
from typing import List
from travel_agents.agents.base_agent import BaseAgent
from travel_agents.models.travel_plan import TravelItinerary, BudgetBreakdown
from travel_agents.services.google_api_service import GoogleAPIService
import logging

logger = logging.getLogger(__name__)


class BudgetOptimizerAgent(BaseAgent):
    """Agent for optimizing travel budget and providing cost recommendations."""

    def __init__(self, google_api_service: GoogleAPIService = None):
        """Initialize budget optimizer agent."""
        super().__init__("BudgetOptimizer")
        self.google_api_service = google_api_service

    def validate_input(self, input_data) -> bool:
        """Validate budget optimization input."""
        if not isinstance(input_data, dict):
            return False
        
        required_keys = ['itinerary', 'total_budget']
        if not all(key in input_data for key in required_keys):
            return False
        
        if not isinstance(input_data['itinerary'], TravelItinerary):
            return False
        
        if not isinstance(input_data['total_budget'], (int, float)) or input_data['total_budget'] <= 0:
            return False
        
        return True

    def analyze_budget(
        self,
        itinerary: TravelItinerary,
        total_budget: float
    ) -> BudgetBreakdown:
        """
        Analyze and break down the travel budget.
        
        Args:
            itinerary: Travel itinerary
            total_budget: Total available budget
            
        Returns:
            Budget breakdown analysis
        """
        estimated_total = itinerary.total_estimated_cost
        
        # Allocate budget based on percentages
        transportation = itinerary.transportation_cost
        accommodation = itinerary.accommodation_cost
        activities = itinerary.activities_cost
        dining = itinerary.dining_cost
        
        # Emergency buffer (10% of total budget)
        emergency_buffer = total_budget * 0.1
        
        # Calculate remaining buffer after estimated costs
        allocated_budget = transportation + accommodation + activities + dining
        remaining_buffer = total_budget - allocated_budget - emergency_buffer
        
        recommendations = self._generate_recommendations(
            total_budget,
            allocated_budget,
            remaining_buffer,
            itinerary
        )
        
        breakdown = BudgetBreakdown(
            total_budget=total_budget,
            transportation=transportation,
            accommodation=accommodation,
            activities=activities,
            dining=dining,
            emergency_buffer=emergency_buffer,
            remaining_buffer=max(0, remaining_buffer),
            recommendations=recommendations
        )
        
        return breakdown

    def _generate_recommendations(
        self,
        total_budget: float,
        allocated_budget: float,
        remaining_buffer: float,
        itinerary: TravelItinerary
    ) -> List[str]:
        """Generate budget optimization recommendations."""
        recommendations = []
        
        # Check if within budget
        if allocated_budget <= total_budget:
            if remaining_buffer > total_budget * 0.15:
                recommendations.append(
                    f"✓ Well within budget! You have ${remaining_buffer:.2f} extra to spend on experiences."
                )
                recommendations.append(
                    "Consider upgrading accommodation or trying premium dining experiences."
                )
            elif remaining_buffer > 0:
                recommendations.append(
                    f"✓ Within budget with ${remaining_buffer:.2f} flexibility for emergencies."
                )
            else:
                recommendations.append(
                    "✓ Budget is tightly allocated. Minimal flexibility remaining."
                )
        else:
            overage = allocated_budget - total_budget
            recommendations.append(
                f"⚠ Budget exceeded by ${overage:.2f}. Consider the following:"
            )
            
            # Provide specific optimization suggestions
            recommendations.extend(self._optimize_costs(itinerary, overage))
        
        # Add general recommendations
        recommendations.append(
            f"Daily budget: ${total_budget / len(itinerary.days):.2f} per day"
        )
        
        if itinerary.accommodation_cost > total_budget * 0.5:
            recommendations.append(
                "💡 Accommodation is a large portion of budget. Consider hostels or Airbnb in cheaper areas."
            )
        
        if itinerary.dining_cost > total_budget * 0.25:
            recommendations.append(
                "💡 Dining costs are high. Try street food and local markets to save money."
            )
        
        if itinerary.activities_cost > total_budget * 0.35:
            recommendations.append(
                "💡 Activity costs are substantial. Look for free or discounted attractions."
            )
        
        return recommendations

    def _optimize_costs(self, itinerary: TravelItinerary, overage: float) -> List[str]:
        """Generate specific cost optimization suggestions."""
        suggestions = []
        
        # Transportation suggestions
        if itinerary.transportation_cost > overage * 0.5:
            savings_needed = overage * 0.3
            suggestions.append(
                f"- Use public transportation instead of taxis: Save ~${savings_needed:.2f}"
            )
            suggestions.append(
                "- Book flights in advance or consider budget airlines"
            )
        
        # Accommodation suggestions
        accommodation_reduction = overage * 0.4
        suggestions.append(
            f"- Reduce accommodation costs by ~${accommodation_reduction:.2f}:"
        )
        suggestions.append(
            "  • Stay in hostels or budget hotels in cheaper neighborhoods"
        )
        suggestions.append(
            "  • Reduce number of nights in expensive cities"
        )
        
        # Activities suggestions
        activity_reduction = overage * 0.2
        suggestions.append(
            f"- Reduce activity costs by ~${activity_reduction:.2f}:"
        )
        suggestions.append(
            "  • Look for free walking tours"
        )
        suggestions.append(
            "  • Skip some paid attractions"
        )
        
        # Dining suggestions
        dining_reduction = overage * 0.1
        suggestions.append(
            f"- Reduce dining costs by ~${dining_reduction:.2f}:"
        )
        suggestions.append(
            "  • Eat lunch/dinner at local street food vendors"
        )
        suggestions.append(
            "  • Cook some meals if accommodation allows"
        )
        
        return suggestions

    def get_daily_breakdown(self, breakdown: BudgetBreakdown, num_days: int) -> dict:
        """
        Get daily budget breakdown.
        
        Args:
            breakdown: Budget breakdown
            num_days: Number of days
            
        Returns:
            Daily breakdown dictionary
        """
        return {
            'total_daily_budget': breakdown.total_budget / num_days,
            'daily_accommodation': breakdown.accommodation / num_days,
            'daily_transport': breakdown.transportation / num_days,
            'daily_activities': breakdown.activities / num_days,
            'daily_dining': breakdown.dining / num_days,
        }

    def process(self, input_data: dict) -> BudgetBreakdown:
        """
        Process itinerary and optimize budget.
        
        Args:
            input_data: Dictionary with itinerary and total budget
            
        Returns:
            Budget breakdown with recommendations
        """
        itinerary: TravelItinerary = input_data['itinerary']
        total_budget: float = input_data['total_budget']
        
        self.logger.info(f"Analyzing budget: ${total_budget} for {itinerary.total_duration} days")
        
        breakdown = self.analyze_budget(itinerary, total_budget)
        
        self.logger.info(f"Budget analysis complete. Remaining buffer: ${breakdown.remaining_buffer:.2f}")
        
        return breakdown
