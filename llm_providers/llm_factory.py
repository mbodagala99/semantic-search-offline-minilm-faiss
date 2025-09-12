#!/usr/bin/env python3
"""
LLM Factory - Provider Selection and Management

This module provides a factory pattern for creating and managing LLM providers,
enabling easy switching between different LLM services.
"""

from typing import Dict, Any, Optional
from .base_llm_provider import BaseLLMProvider
from .gemini_provider import GeminiProvider


class LLMFactory:
    """
    Factory class for creating LLM providers.
    
    Provides a unified interface for creating different LLM providers
    based on configuration.
    """
    
    # Registry of available providers
    _providers = {
        'gemini': GeminiProvider,
        # Future providers can be added here
        # 'openai': OpenAIProvider,
        # 'anthropic': AnthropicProvider,
    }
    
    @classmethod
    def create_provider(
        self, 
        provider_name: str, 
        api_key: str, 
        model_name: str = None,
        **kwargs
    ) -> BaseLLMProvider:
        """
        Create an LLM provider instance.
        
        Args:
            provider_name: Name of the provider ('gemini', 'openai', etc.)
            api_key: API key for the provider
            model_name: Model name (optional, uses provider default)
            **kwargs: Additional provider-specific parameters
            
        Returns:
            LLM provider instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider_name = provider_name.lower()
        
        if provider_name not in self._providers:
            available = ', '.join(self._providers.keys())
            raise ValueError(f"Unsupported provider '{provider_name}'. Available: {available}")
        
        provider_class = self._providers[provider_name]
        
        # Set default model name if not provided
        if model_name is None:
            model_name = self._get_default_model(provider_name)
        
        return provider_class(api_key=api_key, model_name=model_name, **kwargs)
    
    @classmethod
    def get_available_providers(self) -> list:
        """
        Get list of available LLM providers.
        
        Returns:
            List of provider names
        """
        return list(self._providers.keys())
    
    @classmethod
    def register_provider(self, name: str, provider_class: type):
        """
        Register a new LLM provider.
        
        Args:
            name: Provider name
            provider_class: Provider class that extends BaseLLMProvider
        """
        if not issubclass(provider_class, BaseLLMProvider):
            raise ValueError("Provider class must extend BaseLLMProvider")
        
        self._providers[name.lower()] = provider_class
    
    @classmethod
    def _get_default_model(self, provider_name: str) -> str:
        """
        Get default model name for a provider.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            Default model name
        """
        defaults = {
            'gemini': 'gemini-1.5-pro',
            'openai': 'gpt-4',
            'anthropic': 'claude-3-sonnet-20240229'
        }
        
        return defaults.get(provider_name.lower(), 'default')
    
    @classmethod
    def create_from_config(self, config: Dict[str, Any]) -> BaseLLMProvider:
        """
        Create LLM provider from configuration dictionary.
        
        Args:
            config: Configuration dictionary containing:
                - provider: Provider name
                - api_key: API key
                - model: Model name (optional)
                - Additional provider-specific parameters
                
        Returns:
            LLM provider instance
        """
        provider_name = config.get('provider')
        if not provider_name:
            raise ValueError("Configuration must include 'provider' field")
        
        api_key = config.get('api_key')
        if not api_key:
            raise ValueError("Configuration must include 'api_key' field")
        
        model_name = config.get('model')
        
        # Extract additional parameters
        provider_kwargs = {k: v for k, v in config.items() 
                          if k not in ['provider', 'api_key', 'model']}
        
        return self.create_provider(
            provider_name=provider_name,
            api_key=api_key,
            model_name=model_name,
            **provider_kwargs
        )
    
    @classmethod
    def test_provider(self, provider: BaseLLMProvider) -> Dict[str, Any]:
        """
        Test an LLM provider to ensure it's working.
        
        Args:
            provider: LLM provider instance to test
            
        Returns:
            Test results dictionary
        """
        test_results = {
            'provider_name': provider.__class__.__name__,
            'is_available': False,
            'test_query_success': False,
            'error_message': None,
            'response_time_ms': 0
        }
        
        try:
            # Test availability
            test_results['is_available'] = provider.is_available()
            
            if test_results['is_available']:
                # Test with a simple query
                import time
                start_time = time.time()
                
                test_response = provider.generate_dsl_query(
                    user_query="test query",
                    index_info={'index_name': 'test', 'data_source': 'test'},
                    schema_info={'tables': ['test_table']},
                    dsl_type='sql'
                )
                
                test_results['response_time_ms'] = (time.time() - start_time) * 1000
                test_results['test_query_success'] = test_response.success
                
                if not test_response.success:
                    test_results['error_message'] = test_response.error_message
                    
        except Exception as e:
            test_results['error_message'] = str(e)
        
        return test_results
