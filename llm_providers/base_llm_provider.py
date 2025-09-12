#!/usr/bin/env python3
"""
Base LLM Provider - Abstract Interface

This module defines the abstract base class for all LLM providers,
ensuring a consistent interface for plug-and-play LLM integration.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM provider"""
    content: str
    success: bool
    error_message: Optional[str] = None
    usage_stats: Optional[Dict[str, Any]] = None
    model_name: Optional[str] = None
    processing_time_ms: Optional[float] = None


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    This ensures all LLM providers implement the same interface,
    enabling easy switching between different providers.
    """
    
    def __init__(self, api_key: str, model_name: str, **kwargs):
        """
        Initialize the LLM provider.
        
        Args:
            api_key: API key for the LLM service
            model_name: Name of the model to use
            **kwargs: Additional provider-specific parameters
        """
        self.api_key = api_key
        self.model_name = model_name
        self.config = kwargs
        
    @abstractmethod
    def generate_dsl_query(
        self, 
        user_query: str, 
        index_info: Dict[str, Any], 
        schema_info: Dict[str, Any],
        dsl_type: str = "sql"
    ) -> LLMResponse:
        """
        Generate DSL query from user query and index information.
        
        Args:
            user_query: Original user query
            index_info: Information about the identified index
            schema_info: Schema information for the data source
            dsl_type: Type of DSL to generate (sql, graphql, elasticsearch, etc.)
            
        Returns:
            LLMResponse containing the generated DSL query
        """
        pass
    
    @abstractmethod
    def generate_query_explanation(
        self, 
        dsl_query: str, 
        user_query: str
    ) -> LLMResponse:
        """
        Generate explanation of the DSL query.
        
        Args:
            dsl_query: The generated DSL query
            user_query: Original user query
            
        Returns:
            LLMResponse containing the explanation
        """
        pass
    
    @abstractmethod
    def validate_query_safety(
        self, 
        dsl_query: str
    ) -> LLMResponse:
        """
        Validate that the DSL query is safe to execute.
        
        Args:
            dsl_query: The DSL query to validate
            
        Returns:
            LLMResponse indicating if query is safe
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the LLM provider is available and configured.
        
        Returns:
            True if provider is available, False otherwise
        """
        pass
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about the LLM provider.
        
        Returns:
            Dictionary containing provider information
        """
        return {
            "provider_name": self.__class__.__name__,
            "model_name": self.model_name,
            "is_available": self.is_available(),
            "config": self.config
        }
    
    def _create_error_response(
        self, 
        error_message: str, 
        processing_time_ms: float = 0.0
    ) -> LLMResponse:
        """
        Create a standardized error response.
        
        Args:
            error_message: Error message
            processing_time_ms: Processing time in milliseconds
            
        Returns:
            LLMResponse with error information
        """
        return LLMResponse(
            content="",
            success=False,
            error_message=error_message,
            processing_time_ms=processing_time_ms,
            model_name=self.model_name
        )
    
    def _create_success_response(
        self, 
        content: str, 
        usage_stats: Optional[Dict[str, Any]] = None,
        processing_time_ms: float = 0.0
    ) -> LLMResponse:
        """
        Create a standardized success response.
        
        Args:
            content: Generated content
            usage_stats: Usage statistics
            processing_time_ms: Processing time in milliseconds
            
        Returns:
            LLMResponse with success information
        """
        return LLMResponse(
            content=content,
            success=True,
            usage_stats=usage_stats,
            processing_time_ms=processing_time_ms,
            model_name=self.model_name
        )
