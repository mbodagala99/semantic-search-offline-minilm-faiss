#!/usr/bin/env python3
"""
OpenSearch Query Executor
Minimalistic component for executing LLM-generated DSL queries against OpenSearch
"""

import json
import requests
from typing import Dict, Any, Optional, List
from opensearch_server_resolver import OpenSearchServerResolver
from config_reader import config

class OpenSearchQueryExecutor:
    """Minimalistic OpenSearch query executor"""
    
    def __init__(self):
        self.server_resolver = OpenSearchServerResolver()
        self.session = requests.Session()
        self.session.timeout = 30
    
    def execute_query(self, dsl_query: Dict[str, Any], index_name: str) -> Dict[str, Any]:
        """
        Execute DSL query against specified OpenSearch index
        
        Args:
            dsl_query: OpenSearch DSL query dictionary
            index_name: Target index name
            
        Returns:
            Query results with metadata
        """
        try:
            # Get OpenSearch configuration
            opensearch_config = self.server_resolver.resolve_complete_config(index_name)
            
            # Build request URL
            url = f"{opensearch_config['cluster_url']}/{index_name}/_search"
            
            # Execute query
            response = self.session.post(
                url,
                json=dsl_query,
                headers={'Content-Type': 'application/json'},
                auth=self._get_auth(opensearch_config)
            )
            
            # Handle response
            if response.status_code == 200:
                result = response.json()
                return self._format_success_response(result, index_name, dsl_query)
            else:
                return self._format_error_response(response, index_name, dsl_query)
                
        except Exception as e:
            return self._format_exception_response(str(e), index_name, dsl_query)
    
    def _get_auth(self, opensearch_config: Dict[str, Any]) -> Optional[tuple]:
        """Get authentication tuple if needed"""
        auth_config = opensearch_config.get('authentication', {})
        if auth_config.get('type') == 'basic':
            return (auth_config.get('username', ''), auth_config.get('password', ''))
        return None
    
    def _format_success_response(self, result: Dict[str, Any], index_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Format successful query response"""
        hits = result.get('hits', {})
        total_hits = hits.get('total', {})
        
        return {
            'success': True,
            'index_name': index_name,
            'total_hits': total_hits.get('value', 0) if isinstance(total_hits, dict) else total_hits,
            'max_score': hits.get('max_score', 0),
            'documents': hits.get('hits', []),
            'query_executed': query,
            'execution_time_ms': result.get('took', 0),
            'shards_info': result.get('_shards', {})
        }
    
    def _format_error_response(self, response: requests.Response, index_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Format error response"""
        try:
            error_detail = response.json()
        except:
            error_detail = {'error': response.text}
        
        return {
            'success': False,
            'index_name': index_name,
            'error': f"HTTP {response.status_code}: {response.reason}",
            'error_detail': error_detail,
            'query_executed': query
        }
    
    def _format_exception_response(self, error_message: str, index_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Format exception response"""
        return {
            'success': False,
            'index_name': index_name,
            'error': f"Execution failed: {error_message}",
            'query_executed': query
        }
    
    def get_index_info(self, index_name: str) -> Dict[str, Any]:
        """Get basic index information"""
        try:
            opensearch_config = self.server_resolver.resolve_complete_config(index_name)
            url = f"{opensearch_config['cluster_url']}/{index_name}"
            
            response = self.session.get(
                url,
                auth=self._get_auth(opensearch_config)
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"Failed to get index info: {response.status_code}"}
                
        except Exception as e:
            return {'error': f"Exception getting index info: {str(e)}"}
    
    def health_check(self) -> Dict[str, Any]:
        """Check OpenSearch cluster health"""
        try:
            # Use first available server for health check
            opensearch_config = self.server_resolver.resolve_complete_config('healthcare_claims_index')
            url = f"{opensearch_config['cluster_url']}/_cluster/health"
            
            response = self.session.get(
                url,
                auth=self._get_auth(opensearch_config)
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"Health check failed: {response.status_code}"}
                
        except Exception as e:
            return {'error': f"Health check exception: {str(e)}"}

class QueryExecutorFactory:
    """Factory for creating query executor instances"""
    
    @staticmethod
    def create_executor() -> OpenSearchQueryExecutor:
        """Create and return a new query executor instance"""
        return OpenSearchQueryExecutor()

# Example usage and testing
if __name__ == "__main__":
    # Test the executor
    executor = QueryExecutorFactory.create_executor()
    
    # Health check
    print("🔍 Checking OpenSearch health...")
    health = executor.health_check()
    print(f"Cluster Status: {health.get('status', 'unknown')}")
    
    # Test query
    print("\n🧪 Testing sample query...")
    test_query = {
        "query": {
            "match_all": {}
        },
        "size": 2
    }
    
    result = executor.execute_query(test_query, "healthcare_claims_index")
    
    if result['success']:
        print(f"✅ Query successful: {result['total_hits']} total hits")
        print(f"📊 Execution time: {result['execution_time_ms']}ms")
        print(f"📄 Sample documents: {len(result['documents'])}")
    else:
        print(f"❌ Query failed: {result['error']}")
