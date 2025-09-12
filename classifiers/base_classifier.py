"""
Base Healthcare Classifier Interface

Defines the abstract interface for all healthcare query classifiers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    """Standardized classification result"""
    is_healthcare: bool
    confidence: float
    model_name: str
    processing_time_ms: float
    raw_response: Optional[Dict[str, Any]] = None


class BaseHealthcareClassifier(ABC):
    """Abstract base class for healthcare query classification"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get('model_name', 'unknown')
        self.confidence_threshold = config.get('confidence_threshold', 0.5)
    
    @abstractmethod
    def classify(self, query: str) -> ClassificationResult:
        """Classify a query as healthcare or non-healthcare"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the classifier is available and ready"""
        pass
    
    def should_route_to_healthcare(self, result: ClassificationResult) -> bool:
        """Determine if query should be routed to healthcare system"""
        return result.is_healthcare and result.confidence >= self.confidence_threshold
