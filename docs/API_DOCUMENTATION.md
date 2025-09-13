# Healthcare Search API Documentation

## Overview

The Healthcare Search API provides semantic search capabilities for healthcare data using FAISS vector indexes, OpenSearch, and LLM-powered query generation. The API is designed for production use with comprehensive error handling, health monitoring, and scalable architecture.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production deployment, implement appropriate authentication mechanisms.

## API Endpoints

### 1. Root Endpoint

**GET** `/`

Returns basic API information and status.

#### Response

```json
{
  "message": "Healthcare Search API",
  "version": "1.0.0",
  "status": "operational",
  "docs": "/docs"
}
```

#### Example

```bash
curl http://localhost:8000/
```

---

### 2. Health Check

**GET** `/health`

Returns comprehensive health status of all system components.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2025-01-13T12:00:00Z",
  "components": {
    "is_initialized": true,
    "initialization_time": "2025-01-13T11:55:00Z",
    "components": {
      "embedding_generator": true,
      "query_processor": true,
      "dsl_generator": true,
      "query_executor_factory": true,
      "config": true
    },
    "errors": []
  },
  "detailed_checks": {
    "embedding_generator": {
      "status": "healthy",
      "test_embedding_length": 768
    },
    "query_processor": {
      "status": "healthy",
      "test_result_keys": ["user_query", "routing_analysis", "analytics"]
    },
    "dsl_generator": {
      "status": "healthy",
      "test_dsl_type": "dict"
    },
    "query_executor": {
      "status": "healthy",
      "executor_type": "OpenSearchQueryExecutor"
    }
  }
}
```

#### Example

```bash
curl http://localhost:8000/health
```

---

### 3. System Status

**GET** `/status`

Returns system status and component information.

#### Response

```json
{
  "api_status": "operational",
  "components": {
    "is_initialized": true,
    "initialization_time": "2025-01-13T11:55:00Z",
    "components": {
      "embedding_generator": true,
      "query_processor": true,
      "dsl_generator": true,
      "query_executor_factory": true,
      "config": true
    },
    "errors": []
  },
  "timestamp": "2025-01-13T11:55:00Z"
}
```

#### Example

```bash
curl http://localhost:8000/status
```

---

### 4. Available Indexes

**GET** `/indexes`

Returns information about available search indexes and their metadata.

#### Response

```json
{
  "success": true,
  "indexes": {
    "created_at": "2025-01-13T10:00:00",
    "total_embeddings": 66,
    "dimensions": 768,
    "source_files": [
      "providers_index_mapping_expanded.json",
      "claims_index_mapping_expanded.json",
      "procedures_index_mapping_expanded.json",
      "members_index_mapping_expanded.json"
    ],
    "consolidated_index_path": "/path/to/healthcare_semantic_index.faiss"
  },
  "timestamp": "2025-01-13T12:00:00Z"
}
```

#### Example

```bash
curl http://localhost:8000/indexes
```

---

### 5. Search Endpoint

**POST** `/search`

Main search endpoint for healthcare data. Performs semantic search with automatic query routing.

#### Request Body

```json
{
  "query": "Find cardiology providers in New York",
  "index_name": "healthcare_providers_index",
  "max_results": 10,
  "include_metadata": true
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query string (1-1000 characters) |
| `index_name` | string | No | Auto-detected | Specific index to search |
| `max_results` | integer | No | 10 | Maximum results to return (1-100) |
| `include_metadata` | boolean | No | true | Include routing and metadata info |

#### Response

```json
{
  "success": true,
  "query": "Find cardiology providers in New York",
  "results": [
    {
      "provider_id": "PROV001",
      "provider_name": "Dr. John Smith",
      "specialties": ["Cardiology", "Internal Medicine"],
      "location": "New York, NY",
      "rating": 4.8,
      "similarity_score": 0.95
    }
  ],
  "total_hits": 25,
  "execution_time_ms": 150.5,
  "index_used": "healthcare_providers_index",
  "routing_info": {
    "user_query": "Find cardiology providers in New York",
    "routing_analysis": {
      "confidence_score": 0.875,
      "routing_status": "HIGH_CONFIDENCE",
      "primary_data_source": "healthcare_providers_index",
      "matching_capabilities": ["Provider directory management..."]
    },
    "routing_recommendation": "Proceed with healthcare_providers_index for your analysis",
    "analytics": {
      "processing_time_ms": 120.5,
      "query_count": 1,
      "classification_count": 1,
      "rejection_count": 0,
      "timestamp": "2025-01-13T12:00:00Z"
    }
  },
  "error": null,
  "timestamp": "2025-01-13T12:00:00Z"
}
```

#### Error Response

```json
{
  "success": false,
  "query": "Invalid query",
  "results": [],
  "total_hits": 0,
  "execution_time_ms": 50.0,
  "index_used": "unknown",
  "routing_info": null,
  "error": "Search failed: Invalid query format",
  "timestamp": "2025-01-13T12:00:00Z"
}
```

#### Examples

**Basic Search:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Find cardiology providers in New York"}'
```

**Search with Specific Index:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me recent claims data",
    "index_name": "healthcare_claims_index",
    "max_results": 5
  }'
```

**Search with Custom Parameters:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find providers with high patient satisfaction",
    "max_results": 20,
    "include_metadata": false
  }'
```

---

## Available Indexes

The API supports the following healthcare data indexes:

### 1. Healthcare Providers Index (`healthcare_providers_index`)

**Purpose:** Provider directory and network management

**Key Fields:**
- `provider_id`, `npi`, `provider_name`
- `specialties`, `primary_taxonomy`
- `contact_information.address.city`, `contact_information.address.state`
- `credentials`, `organization_name`

**Use Cases:**
- Provider discovery and matching
- Network adequacy analysis
- Credentialing verification
- Geographic distribution analysis

### 2. Healthcare Claims Index (`healthcare_claims_index`)

**Purpose:** Claims processing and financial analysis

**Key Fields:**
- `claim_id`, `patient.first_name`, `patient.last_name`
- `provider.name`, `payer.name`
- `service_lines.procedure_description`
- `adjustments.adjustment_reason`

**Use Cases:**
- Claims investigation and analysis
- Fraud detection patterns
- Provider billing analysis
- Financial reporting

### 3. Procedures Index (`healthcare_procedures_index`)

**Purpose:** Medical procedures and coding

**Key Fields:**
- `procedure_code`, `procedure_description`
- `category`, `specialty_requirements`
- `cost_estimates`, `duration_estimates`

**Use Cases:**
- Procedure code lookup
- Cost analysis
- Specialty requirements
- Procedure categorization

### 4. Members Index (`healthcare_members_index`)

**Purpose:** Member/patient information

**Key Fields:**
- `member_id`, `patient.first_name`, `patient.last_name`
- `demographics`, `insurance_information`
- `medical_history`, `preferences`

**Use Cases:**
- Member matching
- Demographic analysis
- Insurance verification
- Patient care coordination

---

## Query Routing

The API automatically routes queries to the most appropriate index based on:

1. **Semantic Analysis:** Uses embeddings to understand query intent
2. **Keyword Classification:** Identifies healthcare vs non-healthcare queries
3. **Confidence Scoring:** Routes based on confidence thresholds
4. **Domain Matching:** Maps queries to specific healthcare domains

### Routing Status Values

- `HIGH_CONFIDENCE`: Query routed with high confidence (>0.7)
- `REQUIRES_CLARIFICATION`: Query too generic, needs more details
- `REJECTED_NON_HEALTHCARE`: Query appears non-healthcare related

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (endpoint not found) |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Scenarios

1. **Invalid Query Format:**
   ```json
   {
     "detail": "Search failed: Query cannot be empty"
   }
   ```

2. **Component Initialization Error:**
   ```json
   {
     "detail": "Search failed: Embedding generator not available"
   }
   ```

3. **OpenSearch Connection Error:**
   ```json
   {
     "detail": "Search failed: Cannot connect to OpenSearch"
   }
   ```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider implementing:

- Request rate limiting per IP
- Query complexity limits
- Concurrent request limits

---

## Performance Considerations

### Response Times

- **Health Check:** ~50ms
- **Basic Search:** ~2-3 seconds
- **Complex Queries:** ~3-5 seconds

### Optimization Tips

1. **Use Specific Indexes:** Specify `index_name` when you know the target
2. **Limit Results:** Use `max_results` to control response size
3. **Disable Metadata:** Set `include_metadata: false` for faster responses
4. **Cache Results:** Implement client-side caching for repeated queries

---

## Monitoring and Logging

### Health Monitoring

- **Health Endpoint:** `/health` - Comprehensive component health
- **Status Endpoint:** `/status` - System status and metrics
- **Log Files:** `healthcare_search_api.log`

### Key Metrics

- Query execution time
- Component health status
- Error rates
- Search result quality

---

## SDK and Client Libraries

### Python Client Example

```python
import requests

class HealthcareSearchClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def search(self, query, index_name=None, max_results=10):
        response = requests.post(
            f"{self.base_url}/search",
            json={
                "query": query,
                "index_name": index_name,
                "max_results": max_results
            }
        )
        return response.json()
    
    def health(self):
        response = requests.get(f"{self.base_url}/health")
        return response.json()

# Usage
client = HealthcareSearchClient()
results = client.search("Find cardiology providers in New York")
print(f"Found {results['total_hits']} results")
```

### JavaScript Client Example

```javascript
class HealthcareSearchClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async search(query, options = {}) {
        const response = await fetch(`${this.baseUrl}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query,
                ...options
            })
        });
        return await response.json();
    }
    
    async health() {
        const response = await fetch(`${this.baseUrl}/health`);
        return await response.json();
    }
}

// Usage
const client = new HealthcareSearchClient();
const results = await client.search('Find cardiology providers in New York');
console.log(`Found ${results.total_hits} results`);
```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI, where you can:

- Test endpoints directly in the browser
- View request/response schemas
- Explore all available parameters
- See example requests and responses

---

## Support and Troubleshooting

### Common Issues

1. **"Components not initialized"**
   - Check if OpenSearch is running
   - Verify API key configuration
   - Check logs for initialization errors

2. **"Search returns no results"**
   - Verify OpenSearch has data
   - Check if FAISS index exists
   - Try different query terms

3. **"Slow response times"**
   - Check system resources
   - Verify OpenSearch performance
   - Consider query optimization

### Getting Help

1. Check the health endpoint: `GET /health`
2. Review logs: `tail -f healthcare_search_api.log`
3. Run tests: `python test_production_api.py`
4. Check system status: `GET /status`
