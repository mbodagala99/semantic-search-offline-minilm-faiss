# Healthcare Query Router - Intelligent Data Source Routing

## Overview

The Healthcare Query Router is an intelligent system that automatically routes healthcare data queries to the most appropriate data sources using semantic similarity search with confidence-based decision making. It implements a simple two-level confidence approach with a 0.5 threshold for routing decisions.

## Key Features

- **Intelligent Query Routing**: Automatically identifies the best data source for healthcare queries
- **Confidence-Based Decisions**: Uses semantic similarity scores to make routing decisions
- **Query Clarification**: Provides helpful guidance when queries are too generic
- **Professional Architecture**: Clean, well-structured code with appropriate class and method names
- **Comprehensive Testing**: Full test suite with various query scenarios

## Architecture

### Core Classes

#### `HealthcareQueryRouter`
The main router class that handles query routing decisions.

**Key Methods:**
- `route_healthcare_query(user_query: str) -> Dict[str, Any]`: Routes a query to appropriate data source
- `_calculate_confidence_score(search_results: List[Dict[str, Any]]) -> float`: Calculates confidence from search results
- `_create_high_confidence_routing_response()`: Creates response for high confidence matches
- `_create_clarification_request_response()`: Creates clarification request for low confidence matches
- `get_routing_statistics() -> Dict[str, Any]`: Returns system statistics

#### `HealthcareQueryAnalyzer`
Analyzes healthcare queries to provide insights and recommendations.

**Key Methods:**
- `analyze_query_complexity(user_query: str) -> Dict[str, Any]`: Analyzes query complexity
- `get_query_recommendations(user_query: str) -> Dict[str, Any]`: Provides improvement suggestions

## Confidence Levels

### High Confidence (≥ 0.5)
- **Status**: `HIGH_CONFIDENCE`
- **Action**: Direct routing to appropriate data source
- **Response**: Includes data source, index path, and recommendation

### Low Confidence (< 0.5)
- **Status**: `REQUIRES_CLARIFICATION`
- **Action**: Request clarification from user
- **Response**: Includes available domains, required details, and sample queries

## Usage Examples

### Basic Query Routing

```python
from index_router import HealthcareQueryRouter
from embedding_generator import EmbeddingGenerator

# Initialize the system
embedding_gen = EmbeddingGenerator()
query_router = HealthcareQueryRouter(embedding_gen)

# Route a query
result = query_router.route_healthcare_query("Show me fraud detection reports for Q3 2024")

# Check the result
analysis = result["routing_analysis"]
print(f"Confidence: {analysis['confidence_score']}")
print(f"Status: {analysis['routing_status']}")

if analysis["routing_status"] == "HIGH_CONFIDENCE":
    print(f"Data Source: {analysis['primary_data_source']}")
    print(f"Recommendation: {result['routing_recommendation']}")
else:
    print("Clarification needed")
```

### Query Improvement

```python
from index_router import HealthcareQueryAnalyzer

# Initialize analyzer
query_analyzer = HealthcareQueryAnalyzer(query_router)

# Get improvement recommendations
recommendations = query_analyzer.get_query_recommendations("claims")
rec_data = recommendations["query_recommendations"]

print(f"Complexity Level: {rec_data['complexity_analysis']['complexity_level']}")
for suggestion in rec_data["improvement_suggestions"]:
    print(f"- {suggestion}")
```

## Response Formats

### High Confidence Response

```json
{
  "user_query": "Show me fraud detection reports for Q3 2024",
  "routing_analysis": {
    "confidence_score": 0.646,
    "routing_status": "HIGH_CONFIDENCE",
    "primary_data_source": "healthcare_claims_index",
    "index_file_path": "indexes/healthcare_semantic_index.faiss",
    "matching_capabilities": ["fraud detection and investigation..."]
  },
  "routing_recommendation": "Proceed with healthcare_claims_index for your analysis"
}
```

### Low Confidence Response

```json
{
  "user_query": "show me data",
  "routing_analysis": {
    "confidence_score": 0.275,
    "routing_status": "REQUIRES_CLARIFICATION",
    "reason": "Query too generic - confidence below 0.5 threshold"
  },
  "clarification_request": {
    "message": "Your query needs more specific details to find the right data source",
    "available_healthcare_domains": [
      "Claims Processing and Payment Reconciliation",
      "Provider Network Management",
      "Fraud Detection and Investigation",
      "Financial Reporting and Analytics"
    ],
    "required_query_details": [
      "Specific domain (claims, providers, fraud, etc.)",
      "Time period (date range, quarter, etc.)",
      "Type of analysis or report needed"
    ],
    "sample_healthcare_queries": [
      "Show me fraud detection reports for Q3 2024",
      "Generate provider network adequacy analysis for cardiology",
      "Create claims payment reconciliation report for last month"
    ]
  }
}
```

## Available Healthcare Domains

1. **Claims Processing and Payment Reconciliation**
2. **Provider Network Management**
3. **Fraud Detection and Investigation**
4. **Financial Reporting and Analytics**

## Testing

### Run Test Suite
```bash
source venv/bin/activate
python test_healthcare_router.py
```

### Run Examples
```bash
source venv/bin/activate
python example_healthcare_router.py
```

## System Statistics

The router provides comprehensive statistics about the system:

```python
stats = query_router.get_routing_statistics()
print(stats)
```

**Sample Output:**
```json
{
  "routing_system_info": {
    "confidence_threshold": 0.5,
    "available_domains_count": 4,
    "routing_decision_levels": 2
  },
  "index_statistics": {
    "total_embeddings": 32,
    "dimensions": 384,
    "source_files": ["providers_index_mapping_expanded.json", "claims_index_mapping_expanded.json"],
    "index_ntotal": 32,
    "source_breakdown": {
      "healthcare_providers_index": 16,
      "healthcare_claims_index": 16
    }
  }
}
```

## Query Complexity Analysis

The system analyzes query complexity based on:

- **Word Count**: Number of words in the query
- **Timeframe Presence**: Whether the query includes time references
- **Domain Specification**: Whether the query specifies a healthcare domain
- **Analysis Type**: Whether the query specifies the type of analysis needed

**Complexity Levels:**
- **HIGH**: Score ≥ 3 (comprehensive queries)
- **MEDIUM**: Score = 2 (moderately specific queries)
- **LOW**: Score < 2 (generic queries)

## Best Practices

### For High Confidence Routing
- Include specific healthcare domain (claims, providers, fraud, etc.)
- Specify time periods (quarter, month, year, date range)
- Mention the type of analysis or report needed
- Use descriptive terms related to healthcare operations

### For Query Improvement
- Start with domain-specific terms
- Add temporal context
- Specify analysis requirements
- Use healthcare industry terminology

## Dependencies

- `embedding_generator.py`: Core embedding and search functionality
- `sentence-transformers`: For semantic similarity search
- `faiss-cpu`: For efficient vector similarity search
- `numpy`: For numerical operations

## File Structure

```
├── index_router.py                 # Main router implementation
├── test_healthcare_router.py      # Comprehensive test suite
├── example_healthcare_router.py   # Usage examples
├── embedding_generator.py         # Core embedding functionality
└── indexes/
    ├── healthcare_semantic_index.faiss
    ├── healthcare_semantic_index.json
    └── healthcare_semantic_index_registry.json
```

## Future Enhancements

The current implementation provides a solid foundation for future enhancements:

1. **Dynamic Thresholds**: Adjust confidence thresholds based on query complexity
2. **Partial Match Utilization**: Better leverage of low-confidence matches
3. **Context Awareness**: Consider user history and preferences
4. **Multi-Level Routing**: Support for multiple data sources
5. **Learning Capabilities**: Improve routing based on user feedback

## Performance

- **Query Processing**: Fast semantic similarity search using FAISS
- **Memory Efficiency**: Consolidated index approach reduces memory usage
- **Scalability**: Easy to add new healthcare domains and data sources
- **Accuracy**: Conservative 0.5 threshold ensures high-quality routing decisions

The Healthcare Query Router provides a robust, professional solution for intelligent healthcare data query routing with clear separation of concerns and comprehensive testing capabilities.
