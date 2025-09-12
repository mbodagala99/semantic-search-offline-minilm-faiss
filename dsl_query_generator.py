#!/usr/bin/env python3
"""
DSL Query Generator - LLM Integration for Healthcare Queries

This module provides DSL query generation using LLM integration,
converting user queries into executable DSL queries based on
identified healthcare data sources.
"""

import json
from typing import Dict, Any, Optional, List
from llm_providers import LLMFactory, BaseLLMProvider
from config_reader import config


class DSLQueryGenerator:
    """
    DSL Query Generator using LLM integration.
    
    Converts user queries into executable DSL queries based on
    identified healthcare data sources and schemas.
    """
    
    def __init__(self):
        """Initialize the DSL query generator."""
        self.llm_provider = None
        self.is_enabled = config.is_llm_enabled()
        
        if self.is_enabled:
            self._initialize_llm_provider()
    
    def _initialize_llm_provider(self):
        """Initialize the LLM provider from configuration."""
        try:
            llm_config = config.get_llm_config()
            
            if not llm_config['api_key'] or llm_config['api_key'] == 'your_gemini_api_key_here':
                print("⚠️  LLM API key not configured. LLM integration disabled.")
                self.is_enabled = False
                return
            
            self.llm_provider = LLMFactory.create_from_config(llm_config)
            
            # Test the provider
            if not self.llm_provider.is_available():
                print("⚠️  LLM provider not available. LLM integration disabled.")
                self.is_enabled = False
                return
            
            print(f"✅ LLM provider initialized: {llm_config['provider']} ({llm_config['model']})")
            
        except Exception as e:
            print(f"⚠️  Failed to initialize LLM provider: {e}")
            self.is_enabled = False
    
    def generate_dsl_query(
        self, 
        user_query: str, 
        routing_result: Dict[str, Any],
        dsl_type: str = "sql"
    ) -> Dict[str, Any]:
        """
        Generate DSL query from user query and routing result.
        
        Args:
            user_query: Original user query
            routing_result: Result from healthcare query router
            dsl_type: Type of DSL to generate (sql, graphql, elasticsearch, etc.)
            
        Returns:
            Dictionary containing DSL query and metadata
        """
        if not self.is_enabled or not self.llm_provider:
            return self._create_fallback_response(user_query, routing_result)
        
        try:
            # Extract routing information
            routing_analysis = routing_result.get('routing_analysis', {})
            index_info = self._extract_index_info(routing_analysis)
            schema_info = self._get_schema_info(index_info)
            
            # Generate DSL query using LLM
            llm_response = self.llm_provider.generate_dsl_query(
                user_query=user_query,
                index_info=index_info,
                schema_info=schema_info,
                dsl_type=dsl_type
            )
            
            if llm_response.success:
                # Parse structured response
                structured_data = llm_response.content
                
                # Extract OpenSearch DSL from structured response
                opensearch_dsl = structured_data.get('opensearch_dsl', {})
                index_name = structured_data.get('index_name', index_info.get('index_name', 'unknown'))
                query_type = structured_data.get('query_type', 'search')
                
                # Validate query safety
                safety_response = self.llm_provider.validate_query_safety(json.dumps(opensearch_dsl))
                
                return {
                    "dsl_query": opensearch_dsl,
                    "dsl_type": "opensearch",
                    "index_name": index_name,
                    "query_type": query_type,
                    "is_safe": safety_response.success,
                    "safety_issues": safety_response.error_message if not safety_response.success else None,
                    "explanation": self._generate_explanation(user_query, json.dumps(opensearch_dsl)),
                    "metadata": {
                        "provider": self.llm_provider.__class__.__name__,
                        "model": llm_response.model_name,
                        "processing_time_ms": llm_response.processing_time_ms,
                        "usage_stats": llm_response.usage_stats
                    },
                    "index_info": index_info,
                    "success": True,
                    "structured_response": structured_data
                }
            else:
                return self._create_error_response(
                    user_query, 
                    f"LLM generation failed: {llm_response.error_message}"
                )
                
        except Exception as e:
            return self._create_error_response(user_query, f"DSL generation error: {str(e)}")
    
    def _extract_index_info(self, routing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract index information from routing analysis."""
        return {
            "index_name": routing_analysis.get('primary_data_source', 'unknown'),
            "confidence_score": routing_analysis.get('confidence_score', 0.0),
            "routing_status": routing_analysis.get('routing_status', 'unknown'),
            "data_source": routing_analysis.get('primary_data_source', 'unknown')
        }
    
    def _get_schema_info(self, index_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get schema information for the identified index.
        
        This would typically connect to your actual data source
        to get real schema information. For now, we'll use mock data.
        """
        index_name = index_info.get('index_name', 'unknown')
        
        # Mock schema information - in production, this would be dynamic
        schemas = {
            'healthcare_claims_index': {
                'tables': ['claims', 'payments', 'adjustments'],
                'fields': {
                    'claims': ['claim_id', 'patient_id', 'provider_id', 'procedure_code', 'amount', 'status', 'date'],
                    'payments': ['payment_id', 'claim_id', 'amount', 'payment_date', 'method'],
                    'adjustments': ['adjustment_id', 'claim_id', 'amount', 'reason', 'date']
                },
                'relationships': [
                    'claims.claim_id = payments.claim_id',
                    'claims.claim_id = adjustments.claim_id'
                ]
            },
            'healthcare_providers_index': {
                'tables': ['providers', 'specialties', 'credentials'],
                'fields': {
                    'providers': ['provider_id', 'name', 'npi', 'specialty_id', 'active'],
                    'specialties': ['specialty_id', 'name', 'description'],
                    'credentials': ['credential_id', 'provider_id', 'type', 'expiry_date']
                },
                'relationships': [
                    'providers.specialty_id = specialties.specialty_id',
                    'providers.provider_id = credentials.provider_id'
                ]
            },
            'healthcare_members_index': {
                'tables': ['members', 'enrollments', 'benefits'],
                'fields': {
                    'members': ['member_id', 'first_name', 'last_name', 'dob', 'ssn', 'active'],
                    'enrollments': ['enrollment_id', 'member_id', 'plan_id', 'start_date', 'end_date'],
                    'benefits': ['benefit_id', 'plan_id', 'benefit_type', 'coverage_level']
                },
                'relationships': [
                    'members.member_id = enrollments.member_id',
                    'enrollments.plan_id = benefits.plan_id'
                ]
            },
            'healthcare_procedures_index': {
                'tables': ['procedures', 'codes', 'pricing'],
                'fields': {
                    'procedures': ['procedure_id', 'code', 'description', 'category'],
                    'codes': ['code_id', 'code', 'type', 'description'],
                    'pricing': ['pricing_id', 'procedure_id', 'amount', 'effective_date']
                },
                'relationships': [
                    'procedures.code = codes.code',
                    'procedures.procedure_id = pricing.procedure_id'
                ]
            }
        }
        
        return schemas.get(index_name, {
            'tables': ['unknown_table'],
            'fields': {'unknown_table': ['id', 'name']},
            'relationships': []
        })
    
    def _generate_explanation(self, user_query: str, dsl_query: str) -> str:
        """Generate explanation of the DSL query."""
        if not self.is_enabled or not self.llm_provider:
            return f"Generated {dsl_query.split()[0].upper()} query for: {user_query}"
        
        try:
            response = self.llm_provider.generate_query_explanation(dsl_query, user_query)
            return response.content if response.success else f"Generated {dsl_query.split()[0].upper()} query for: {user_query}"
        except Exception:
            return f"Generated {dsl_query.split()[0].upper()} query for: {user_query}"
    
    def _create_fallback_response(self, user_query: str, routing_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback response when LLM is not available."""
        routing_analysis = routing_result.get('routing_analysis', {})
        index_name = routing_analysis.get('primary_data_source', 'unknown')
        
        # Simple fallback query generation
        fallback_data = self._generate_fallback_query(user_query, index_name)
        
        return {
            "dsl_query": fallback_data["opensearch_dsl"],
            "dsl_type": "opensearch",
            "index_name": fallback_data["index_name"],
            "query_type": fallback_data["query_type"],
            "is_safe": True,
            "safety_issues": None,
            "explanation": f"Fallback OpenSearch DSL query generated for: {user_query}",
            "metadata": {
                "provider": "fallback",
                "model": "none",
                "processing_time_ms": 0,
                "usage_stats": None
            },
            "index_info": self._extract_index_info(routing_analysis),
            "success": True,
            "fallback": True,
            "structured_response": fallback_data
        }
    
    def _generate_fallback_query(self, user_query: str, index_name: str) -> Dict[str, Any]:
        """Generate a simple fallback OpenSearch DSL query when LLM is not available."""
        # Simple keyword-based query generation
        query_lower = user_query.lower()
        
        # Base OpenSearch DSL structure
        base_dsl = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            },
            "size": 100,
            "sort": [
                {
                    "date": {
                        "order": "desc"
                    }
                }
            ]
        }
        
        # Add specific filters based on query content
        if 'denied' in query_lower or 'rejected' in query_lower:
            base_dsl["query"]["bool"]["filter"].append({
                "term": {
                    "status": "denied"
                }
            })
        elif 'approved' in query_lower or 'paid' in query_lower:
            base_dsl["query"]["bool"]["filter"].append({
                "term": {
                    "status": "approved"
                }
            })
        
        if 'last month' in query_lower or 'recent' in query_lower:
            base_dsl["query"]["bool"]["filter"].append({
                "range": {
                    "date": {
                        "gte": "now-1M"
                    }
                }
            })
        
        # Add text search if specific terms are mentioned
        if 'claims' in query_lower:
            base_dsl["query"]["bool"]["must"].append({
                "match": {
                    "claim_type": "healthcare"
                }
            })
        elif 'provider' in query_lower:
            base_dsl["query"]["bool"]["must"].append({
                "match": {
                    "provider_type": "healthcare"
                }
            })
        
        return {
            "index_name": index_name,
            "query_type": "search",
            "opensearch_dsl": base_dsl
        }
    
    def _create_error_response(self, user_query: str, error_message: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            "dsl_query": "",
            "dsl_type": "sql",
            "is_safe": False,
            "safety_issues": error_message,
            "explanation": f"Error generating query for: {user_query}",
            "metadata": {
                "provider": "error",
                "model": "none",
                "processing_time_ms": 0,
                "usage_stats": None
            },
            "index_info": {},
            "success": False,
            "error": error_message
        }
    
    def is_available(self) -> bool:
        """Check if DSL query generator is available."""
        return self.is_enabled and self.llm_provider is not None
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the LLM provider."""
        if not self.llm_provider:
            return {"available": False, "provider": "none"}
        
        return {
            "available": True,
            "provider_info": self.llm_provider.get_provider_info()
        }
