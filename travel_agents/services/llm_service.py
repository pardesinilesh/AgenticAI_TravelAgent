"""LLM Service for intelligent reasoning and decision-making."""
import os
import json
from typing import Dict, List, Any, Optional
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM-based reasoning and intelligence."""

    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        """
        Initialize LLM service.
        
        Args:
            model: OpenAI model to use
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set. LLM reasoning disabled.")
            self.enabled = False
            return
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.enabled = True
        logger.info(f"LLM Service initialized with model: {model}")

    def reason_about_destinations(
        self,
        preferences: Dict[str, Any],
        destinations: List[str],
        context: str = ""
    ) -> str:
        """
        Use LLM to reason about best destinations.
        
        Args:
            preferences: User preferences dictionary
            destinations: List of candidate destinations
            context: Additional context
            
        Returns:
            LLM reasoning and recommendations
        """
        if not self.enabled:
            return ""
        
        prompt = f"""
        You are an expert travel advisor. Based on the following user preferences and candidate destinations,
        provide thoughtful reasoning about which destinations would be best matches.
        
        User Preferences:
        - Travel Style: {preferences.get('travel_style', 'comfort')}
        - Budget: ${preferences.get('budget', 0)}
        - Trip Duration: {preferences.get('duration_days', 7)} days
        - Interests: {', '.join(preferences.get('interests', []))}
        - Number of Travelers: {preferences.get('number_of_travelers', 1)}
        
        Candidate Destinations: {', '.join(destinations)}
        
        Additional Context: {context}
        
        Please provide:
        1. Top 3 destination recommendations with reasoning
        2. Why each destination matches their profile
        3. Any concerns or considerations
        4. Hidden gems or alternatives they might not have considered
        
        Format your response as JSON with keys: top_picks, reasoning, concerns, alternatives
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            reasoning = response.choices[0].message.content
            logger.info("Destination reasoning completed via LLM")
            return reasoning
            
        except Exception as e:
            logger.error(f"Error in LLM reasoning: {str(e)}")
            return ""

    def generate_itinerary_description(
        self,
        destination: str,
        preferences: Dict[str, Any],
        days: int
    ) -> str:
        """
        Generate creative itinerary description.
        
        Args:
            destination: Destination name
            preferences: User preferences
            days: Number of days
            
        Returns:
            Creative itinerary description
        """
        if not self.enabled:
            return ""
        
        prompt = f"""
        Create a compelling {days}-day itinerary description for {destination}
        tailored to someone who enjoys: {', '.join(preferences.get('interests', []))}
        
        Travel style: {preferences.get('travel_style', 'comfort')}
        
        Generate a narrative that:
        1. Captures the essence of the destination
        2. Highlights experiences matching their interests
        3. Includes local tips and hidden gems
        4. Is inspiring and actionable
        
        Keep it concise (150-200 words).
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=300
            )
            
            description = response.choices[0].message.content
            return description
            
        except Exception as e:
            logger.error(f"Error generating itinerary description: {str(e)}")
            return ""

    def optimize_budget_reasoning(
        self,
        budget_breakdown: Dict[str, float],
        exceeded: bool
    ) -> List[str]:
        """
        Use LLM to generate intelligent budget optimization recommendations.
        
        Args:
            budget_breakdown: Current budget breakdown
            exceeded: Whether budget is exceeded
            
        Returns:
            List of intelligent recommendations
        """
        if not self.enabled:
            return []
        
        status = "EXCEEDED" if exceeded else "WITHIN"
        
        prompt = f"""
        As a travel budget expert, provide detailed optimization recommendations
        for the following trip budget (Status: {status}):
        
        Budget Breakdown:
        {json.dumps(budget_breakdown, indent=2)}
        
        Generate 5-7 specific, actionable recommendations that:
        1. Consider the travel style implications
        2. Include creative money-saving ideas
        3. Suggest tactical adjustments
        4. Highlight where to splurge vs save
        
        Format as a numbered list.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            recommendations_text = response.choices[0].message.content
            # Split recommendations into list
            recommendations = [
                line.strip() for line in recommendations_text.split('\n') 
                if line.strip() and not line.strip().startswith('#')
            ]
            
            logger.info("Budget optimization recommendations generated via LLM")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in budget optimization: {str(e)}")
            return []

    def evaluate_trip_satisfaction(
        self,
        trip_plan: Dict[str, Any],
        user_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate overall trip satisfaction using LLM analysis.
        
        Args:
            trip_plan: Complete trip plan
            user_feedback: Optional user feedback
            
        Returns:
            Evaluation dictionary with score and insights
        """
        if not self.enabled:
            return {"score": 0.5, "insights": []}
        
        prompt = f"""
        Analyze this trip plan for overall satisfaction and improvement potential:
        
        Trip Summary:
        - Duration: {trip_plan.get('summary', {}).get('trip_duration', 'N/A')}
        - Destinations: {trip_plan.get('summary', {}).get('destinations', 'N/A')}
        - Travel Style: {trip_plan.get('summary', {}).get('travel_style', 'N/A')}
        - Budget Status: {trip_plan.get('summary', {}).get('budget_status', 'N/A')}
        
        {f'User Feedback: {user_feedback}' if user_feedback else ''}
        
        Provide:
        1. Overall satisfaction score (0-10)
        2. Key strengths of the plan
        3. Potential improvements
        4. Risk factors
        
        Format as JSON with keys: score, strengths, improvements, risks
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=600
            )
            
            evaluation_text = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                evaluation = json.loads(evaluation_text)
            except json.JSONDecodeError:
                evaluation = {"analysis": evaluation_text}
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating trip satisfaction: {str(e)}")
            return {"score": 0.5, "insights": []}

    def generate_travel_tips(
        self,
        destinations: List[str],
        preferences: Dict[str, Any]
    ) -> str:
        """
        Generate personalized travel tips for the trip.
        
        Args:
            destinations: List of destinations
            preferences: User preferences
            
        Returns:
            Travel tips and advice
        """
        if not self.enabled:
            return ""
        
        prompt = f"""
        Generate personalized travel tips for someone visiting:
        {', '.join(destinations)}
        
        User Profile:
        - Travel Style: {preferences.get('travel_style', 'comfort')}
        - Interests: {', '.join(preferences.get('interests', []))}
        - Travel Duration: {preferences.get('duration_days', 7)} days
        - Budget: {preferences.get('budget', 0)}
        
        Include tips about:
        1. Getting around efficiently
        2. Staying safe and healthy
        3. Cultural considerations
        4. Money-saving hacks
        5. Best times to visit attractions
        6. Local dining recommendations
        
        Keep it practical and actionable (200-300 words).
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            tips = response.choices[0].message.content
            return tips
            
        except Exception as e:
            logger.error(f"Error generating travel tips: {str(e)}")
            return ""

    def should_revise_plan(
        self,
        current_plan: Dict[str, Any],
        feedback_score: float,
        user_concerns: List[str]
    ) -> Dict[str, Any]:
        """
        Autonomously determine if plan should be revised.
        
        Args:
            current_plan: Current trip plan
            feedback_score: User satisfaction score (0-1)
            user_concerns: List of user concerns
            
        Returns:
            Dictionary with revision_needed and suggested_changes
        """
        if not self.enabled:
            return {"revision_needed": False, "reason": "LLM disabled"}
        
        prompt = f"""
        Autonomously evaluate if this trip plan should be revised:
        
        User Satisfaction Score: {feedback_score}/1.0
        User Concerns: {', '.join(user_concerns) if user_concerns else 'None'}
        
        Current Plan Summary:
        - Destinations: {current_plan.get('summary', {}).get('destinations', 'N/A')}
        - Duration: {current_plan.get('summary', {}).get('trip_duration', 'N/A')}
        - Budget Status: {current_plan.get('summary', {}).get('budget_status', 'N/A')}
        
        Determine:
        1. Should the plan be revised? (yes/no)
        2. If yes, what specific changes are recommended?
        3. What's the reasoning?
        4. Priority level (low/medium/high)
        
        Be objective and practical. Format as JSON with keys: 
        revision_needed (bool), changes (list), reasoning (str), priority (str)
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=500
            )
            
            evaluation_text = response.choices[0].message.content
            
            try:
                evaluation = json.loads(evaluation_text)
            except json.JSONDecodeError:
                evaluation = {
                    "revision_needed": feedback_score < 0.6,
                    "reasoning": evaluation_text
                }
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating plan revision: {str(e)}")
            return {"revision_needed": False, "reason": "Error occurred"}
