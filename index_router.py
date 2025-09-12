#!/usr/bin/env python3
"""
Healthcare Index Router - Intelligent Query Routing System

This module provides intelligent routing capabilities for healthcare data queries
using semantic similarity search with confidence-based decision making.

"""

import json
import os
from typing import Dict, List, Any, Optional
from embedding_generator import EmbeddingGenerator
from config_reader import config
from classifiers import ClassifierFactory


class HealthcareQueryRouter:
    """
    Intelligent router for healthcare data queries using semantic similarity.
    
    Routes user queries to appropriate healthcare data indexes based on
    confidence scores from semantic similarity search.
    """
    
    def __init__(self, embedding_generator: EmbeddingGenerator):
        """
        Initialize the healthcare query router.
        
        Args:
            embedding_generator: Instance of EmbeddingGenerator for semantic search
        """
        self.embedding_generator = embedding_generator
        # Use configuration for thresholds
        self.confidence_threshold = config.get_default_threshold()
        self.minimum_threshold = config.get_minimum_threshold()
        self.available_domains = [
            "Claims Processing and Payment Reconciliation",
            "Provider Network Management", 
            "Fraud Detection and Investigation",
            "Financial Reporting and Analytics"
        ]
        
        # Initialize healthcare classifier
        self.classifier = self._initialize_classifier()
    
    def _initialize_classifier(self):
        """Initialize the healthcare classifier"""
        try:
            classifier_config = {
                'model_name': config.get_bart_model(),
                'confidence_threshold': config.get_classifier_threshold(),
                'device': config.get_classifier_device(),
                'voting_strategy': config.get_voting_strategy(),
                'bart_weight': config.get_bart_weight(),
                'keyword_weight': config.get_keyword_weight(),
                'min_confidence_threshold': config.get_min_confidence_threshold()
            }
            return ClassifierFactory.create_classifier(
                config.get_classifier_type(),
                classifier_config
            )
        except Exception as e:
            print(f"Warning: Could not initialize classifier: {e}")
            return None
    
    def route_healthcare_query(self, user_query: str) -> Dict[str, Any]:
        """
        Route a healthcare query to the most appropriate data source.
        
        Args:
            user_query: The user's query string
            
        Returns:
            Dictionary containing routing analysis and recommendations
        """
        try:
            # Step 1: Classify as healthcare/non-healthcare
            if self.classifier and self.classifier.is_available():
                classification_result = self.classifier.classify(user_query)
                
                # If not healthcare, reject early
                if not self.classifier.should_route_to_healthcare(classification_result):
                    return {
                        "query": user_query,
                        "routing_status": "REJECTED_NON_HEALTHCARE",
                        "confidence_score": classification_result.confidence,
                        "primary_data_source": "N/A",
                        "classification_info": {
                            "is_healthcare": classification_result.is_healthcare,
                            "model_name": classification_result.model_name,
                            "processing_time_ms": classification_result.processing_time_ms
                        },
                        "message": "Query appears to be non-healthcare related. Please provide a healthcare-specific query."
                    }
            
            # Step 2: If healthcare, proceed with existing similarity search
            return self._perform_similarity_search(user_query)
                
        except Exception as e:
            return self._create_error_response(user_query, str(e))
    
    def _create_error_response(self, user_query: str, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "query": user_query,
            "routing_status": "ERROR",
            "confidence_score": 0.0,
            "primary_data_source": "N/A",
            "message": f"Error processing query: {error_message}"
        }
    
    def _perform_similarity_search(self, user_query: str) -> Dict[str, Any]:
        """Perform semantic similarity search for healthcare queries"""
        # Search the consolidated healthcare index
        search_results = self.embedding_generator.search_consolidated_index(
            user_query, 
            top_k=5
        )
        
        # Calculate confidence score from best match
        confidence_score = self._calculate_confidence_score(search_results)
        
        # Make routing decision based on confidence threshold
        if confidence_score >= self.confidence_threshold:
            return self._create_high_confidence_routing_response(
                user_query, confidence_score, search_results
            )
        else:
            return self._create_clarification_request_response(
                user_query, confidence_score
            )
    
    def _calculate_confidence_score(self, search_results: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score from search results.
        
        Args:
            search_results: List of search results from semantic search
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not search_results:
            return 0.0
        
        # Use the highest similarity score as confidence
        return max(result.get('similarity_score', 0.0) for result in search_results)
    
    def _create_high_confidence_routing_response(
        self, 
        user_query: str, 
        confidence_score: float, 
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create response for high confidence matches.
        
        Args:
            user_query: Original user query
            confidence_score: Calculated confidence score
            search_results: Search results from semantic search
            
        Returns:
            High confidence routing response
        """
        best_match = search_results[0]
        
        return {
            "user_query": user_query,
            "routing_analysis": {
                "confidence_score": confidence_score,
                "routing_status": "HIGH_CONFIDENCE",
                "primary_data_source": best_match.get('source_index'),
                "index_file_path": "indexes/healthcare_semantic_index.faiss",
                "matching_capabilities": [best_match.get('text', '')[:100] + "..."]
            },
            "routing_recommendation": f"Proceed with {best_match.get('source_index')} for your analysis"
        }
    
    def _create_clarification_request_response(
        self, 
        user_query: str, 
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Create clarification request for low confidence matches.
        
        Args:
            user_query: Original user query
            confidence_score: Calculated confidence score
            
        Returns:
            Clarification request response
        """
        return {
            "user_query": user_query,
            "routing_analysis": {
                "confidence_score": confidence_score,
                "routing_status": "REQUIRES_CLARIFICATION",
                "reason": "Query too generic - confidence below 0.5 threshold"
            },
            "clarification_request": {
                "message": "Your query needs more specific details to find the right data source",
                "available_healthcare_domains": self.available_domains,
                "required_query_details": [
                    "Specific domain (claims, providers, fraud, etc.)",
                    "Time period (date range, quarter, etc.)",
                    "Type of analysis or report needed"
                ],
                "sample_healthcare_queries": [
                    "Show me fraud detection reports for Q3 2024",
                    "Generate provider network adequacy analysis for cardiology",
                    "Create claims payment reconciliation report for last month",
                    "Analyze provider performance metrics for emergency services"
                ]
            }
        }
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the routing system.
        
        Returns:
            Dictionary containing routing system statistics
        """
        try:
            index_stats = self.embedding_generator.get_consolidated_index_statistics()
            return {
                "routing_system_info": {
                    "confidence_threshold": self.confidence_threshold,
                    "available_domains_count": len(self.available_domains),
                    "routing_decision_levels": 2
                },
                "index_statistics": index_stats
            }
        except Exception as e:
            return {
                "routing_system_info": {
                    "confidence_threshold": self.confidence_threshold,
                    "available_domains_count": len(self.available_domains),
                    "routing_decision_levels": 2
                },
                "error": f"Could not retrieve index statistics: {str(e)}"
            }


class HealthcareQueryAnalyzer:
    """
    Analyzer for healthcare queries to provide insights and recommendations.
    """
    
    def __init__(self, query_router: HealthcareQueryRouter):
        """
        Initialize the healthcare query analyzer.
        
        Args:
            query_router: Instance of HealthcareQueryRouter
        """
        self.query_router = query_router
    
    def analyze_query_complexity(self, user_query: str) -> Dict[str, Any]:
        """
        Analyze the complexity of a healthcare query.
        
        Args:
            user_query: The user's query string
            
        Returns:
            Dictionary containing complexity analysis
        """
        # Basic complexity indicators
        word_count = len(user_query.split())
        has_timeframe = any(word in user_query.lower() for word in ['quarter', 'month', 'year', '2024', '2023'])
        has_domain = any(domain.lower() in user_query.lower() for domain in ['claims', 'provider', 'fraud', 'financial'])
        has_analysis_type = any(word in user_query.lower() for word in ['report', 'analysis', 'metrics', 'performance'])
        
        complexity_score = 0
        if word_count > 5:
            complexity_score += 1
        if has_timeframe:
            complexity_score += 1
        if has_domain:
            complexity_score += 1
        if has_analysis_type:
            complexity_score += 1
        
        return {
            "query_complexity_analysis": {
                "word_count": word_count,
                "has_timeframe": has_timeframe,
                "has_domain_specification": has_domain,
                "has_analysis_type": has_analysis_type,
                "complexity_score": complexity_score,
                "complexity_level": self._get_complexity_level(complexity_score)
            }
        }
    
    def _get_complexity_level(self, score: int) -> str:
        """Get complexity level based on score."""
        if score >= 3:
            return "HIGH"
        elif score >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_query_recommendations(self, user_query: str) -> Dict[str, Any]:
        """
        Get recommendations for improving a healthcare query.
        
        Args:
            user_query: The user's query string
            
        Returns:
            Dictionary containing query improvement recommendations
        """
        complexity_analysis = self.analyze_query_complexity(user_query)
        routing_result = self.query_router.route_healthcare_query(user_query)
        
        recommendations = []
        
        if routing_result["routing_analysis"]["routing_status"] == "REQUIRES_CLARIFICATION":
            if not complexity_analysis["query_complexity_analysis"]["has_domain_specification"]:
                recommendations.append("Specify the healthcare domain (claims, providers, fraud, etc.)")
            if not complexity_analysis["query_complexity_analysis"]["has_timeframe"]:
                recommendations.append("Add a time period (quarter, month, year, date range)")
            if not complexity_analysis["query_complexity_analysis"]["has_analysis_type"]:
                recommendations.append("Specify the type of analysis or report needed")
        
        return {
            "query_recommendations": {
                "original_query": user_query,
                "routing_status": routing_result["routing_analysis"]["routing_status"],
                "confidence_score": routing_result["routing_analysis"]["confidence_score"],
                "improvement_suggestions": recommendations,
                "complexity_analysis": complexity_analysis["query_complexity_analysis"]
            }
        }


def main():
    """Main function to demonstrate the healthcare query routing system."""
    print("🏥 Healthcare Query Router - Intelligent Data Source Routing")
    print("=" * 60)
    
    # Initialize the embedding generator
    embedding_gen = EmbeddingGenerator()
    
    # Initialize the query router
    query_router = HealthcareQueryRouter(embedding_gen)
    
    # Initialize the query analyzer
    query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    # Test queries
    test_queries = [
        "Show me fraud detection reports for Q3 2024",
        "Generate provider network adequacy analysis for cardiology",
        "show me data",
        "claims analysis",
        "provider performance metrics for emergency services"
    ]
    
    print("\n🔍 Testing Healthcare Query Routing:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 30)
        
        # Route the query
        routing_result = query_router.route_healthcare_query(query)
        
        # Display routing analysis
        analysis = routing_result["routing_analysis"]
        print(f"   Confidence Score: {analysis['confidence_score']:.3f}")
        print(f"   Routing Status: {analysis['routing_status']}")
        
        if analysis["routing_status"] == "HIGH_CONFIDENCE":
            print(f"   Primary Data Source: {analysis['primary_data_source']}")
            print(f"   Recommendation: {routing_result['routing_recommendation']}")
        else:
            print("   Clarification Required:")
            clarification = routing_result["clarification_request"]
            print(f"   Message: {clarification['message']}")
            print(f"   Available Domains: {len(clarification['available_healthcare_domains'])}")
            print(f"   Sample Queries: {len(clarification['sample_healthcare_queries'])}")
        
        # Get query recommendations
        recommendations = query_analyzer.get_query_recommendations(query)
        if recommendations["query_recommendations"]["improvement_suggestions"]:
            print("   Improvement Suggestions:")
            for suggestion in recommendations["query_recommendations"]["improvement_suggestions"]:
                print(f"   - {suggestion}")
    
    # Display system statistics
    print("\n📊 Healthcare Query Router Statistics:")
    print("-" * 40)
    stats = query_router.get_routing_statistics()
    system_info = stats["routing_system_info"]
    print(f"   Confidence Threshold: {system_info['confidence_threshold']}")
    print(f"   Available Domains: {system_info['available_domains_count']}")
    print(f"   Routing Decision Levels: {system_info['routing_decision_levels']}")
    
    if "index_statistics" in stats:
        index_stats = stats["index_statistics"]
        print(f"   Total Embeddings: {index_stats.get('total_embeddings', 'N/A')}")
        print(f"   Index Dimensions: {index_stats.get('embedding_dimensions', 'N/A')}")
        print(f"   Source Files: {index_stats.get('source_files_count', 'N/A')}")


if __name__ == "__main__":
    main()
