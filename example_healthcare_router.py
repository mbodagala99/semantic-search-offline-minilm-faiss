#!/usr/bin/env python3
"""
Example usage of Healthcare Query Router

This script demonstrates how to use the healthcare query routing system
for intelligent data source selection based on user queries.
"""

import json
from index_router import HealthcareQueryRouter, HealthcareQueryAnalyzer
from embedding_generator import EmbeddingGenerator


def example_basic_routing():
    """Example of basic query routing."""
    
    print("🏥 Basic Healthcare Query Routing Example")
    print("=" * 45)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    
    # Example queries
    queries = [
        "Show me fraud detection reports for Q3 2024",
        "Generate provider network analysis",
        "show me data"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 25)
        
        # Route the query
        result = query_router.route_healthcare_query(query)
        
        # Display results
        analysis = result["routing_analysis"]
        print(f"Confidence: {analysis['confidence_score']:.3f}")
        print(f"Status: {analysis['routing_status']}")
        
        if analysis["routing_status"] == "HIGH_CONFIDENCE":
            print(f"Data Source: {analysis['primary_data_source']}")
            print(f"Recommendation: {result['routing_recommendation']}")
        else:
            print("Clarification needed - query too generic")


def example_query_improvement():
    """Example of query improvement suggestions."""
    
    print(f"\n🔧 Query Improvement Example")
    print("=" * 30)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    # Generic query that needs improvement
    generic_query = "claims"
    
    print(f"Original Query: '{generic_query}'")
    
    # Get improvement recommendations
    recommendations = query_analyzer.get_query_recommendations(generic_query)
    rec_data = recommendations["query_recommendations"]
    
    print(f"Confidence Score: {rec_data['confidence_score']:.3f}")
    print(f"Complexity Level: {rec_data['complexity_analysis']['complexity_level']}")
    
    if rec_data["improvement_suggestions"]:
        print("Improvement Suggestions:")
        for suggestion in rec_data["improvement_suggestions"]:
            print(f"  - {suggestion}")
    
    # Show sample improved queries
    print("\nSample Improved Queries:")
    improved_queries = [
        "Show me claims payment reconciliation for Q3 2024",
        "Generate claims processing analysis for last month",
        "Create claims fraud detection report for 2024"
    ]
    
    for improved_query in improved_queries:
        print(f"\nImproved: '{improved_query}'")
        result = query_router.route_healthcare_query(improved_query)
        analysis = result["routing_analysis"]
        print(f"  Confidence: {analysis['confidence_score']:.3f}")
        print(f"  Status: {analysis['routing_status']}")


def example_system_statistics():
    """Example of system statistics."""
    
    print(f"\n📊 System Statistics Example")
    print("=" * 30)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    
    # Get statistics
    stats = query_router.get_routing_statistics()
    
    print("Routing System Configuration:")
    system_info = stats["routing_system_info"]
    for key, value in system_info.items():
        print(f"  {key}: {value}")
    
    if "index_statistics" in stats:
        print("\nIndex Information:")
        index_stats = stats["index_statistics"]
        for key, value in index_stats.items():
            print(f"  {key}: {value}")


def example_interactive_routing():
    """Example of interactive query routing."""
    
    print(f"\n🔄 Interactive Routing Example")
    print("=" * 35)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    # Simulate user interaction
    user_queries = [
        "show me data",  # Generic query
        "fraud detection",  # Partial query
        "Show me fraud detection reports for Q3 2024"  # Specific query
    ]
    
    for i, query in enumerate(user_queries, 1):
        print(f"\nStep {i}: User Query: '{query}'")
        
        # Route the query
        result = query_router.route_healthcare_query(query)
        analysis = result["routing_analysis"]
        
        print(f"System Response:")
        print(f"  Confidence: {analysis['confidence_score']:.3f}")
        print(f"  Status: {analysis['routing_status']}")
        
        if analysis["routing_status"] == "REQUIRES_CLARIFICATION":
            print("  Action: Requesting clarification from user")
            clarification = result["clarification_request"]
            print(f"  Message: {clarification['message']}")
            print("  Available domains:")
            for domain in clarification["available_healthcare_domains"]:
                print(f"    - {domain}")
        else:
            print("  Action: Routing to appropriate data source")
            print(f"  Data Source: {analysis['primary_data_source']}")
            print(f"  Recommendation: {result['routing_recommendation']}")


def main():
    """Main example function."""
    
    print("🏥 Healthcare Query Router - Usage Examples")
    print("=" * 50)
    
    try:
        # Run examples
        example_basic_routing()
        example_query_improvement()
        example_system_statistics()
        example_interactive_routing()
        
        print(f"\n✅ All Examples Completed Successfully!")
        print("\nThe healthcare query router is ready for use.")
        print("You can now route healthcare queries intelligently!")
        
    except Exception as e:
        print(f"\n❌ Example Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
