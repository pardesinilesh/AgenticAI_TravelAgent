"""Base agent class for travel planning."""
from abc import ABC, abstractmethod
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for travel planning agents."""

    def __init__(self, name: str):
        """Initialize base agent."""
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Process input data and return output.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Processed output
        """
        pass

    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if input is valid
        """
        pass

    def run(self, input_data: Any) -> Any:
        """
        Run the agent with input data.
        
        Args:
            input_data: Input data
            
        Returns:
            Processed output
        """
        self.logger.info(f"Running {self.name} agent with input")
        
        if not self.validate_input(input_data):
            raise ValueError(f"Invalid input for {self.name} agent")
        
        result = self.process(input_data)
        self.logger.info(f"{self.name} agent completed successfully")
        return result
