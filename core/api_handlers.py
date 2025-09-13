#!/usr/bin/env python3
"""
Production-Ready API Handlers for Healthcare Search
Clean, modular API handlers that use pre-initialized components
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from .initialization import get_components, health_check

logger = logging.getLogger(__name__)


# Pydantic models for API requests/responses
class SearchRequest(BaseModel):
    """Request model for search API"""
    query: str = Field(..., description="Search query string", min_length=1, max_length=1000)
    index_name: Optional[str] = Field(None, description="Specific index to search (optional)")
    max_results: int = Field(10, description="Maximum number of results to return", ge=1, le=100)
    include_metadata: bool = Field(True, description="Include metadata in response")
    
    class Config:
        schema_extra = {
            "example": {
                "query": "Find cardiology providers in New York",
                "index_name": "healthcare_providers_index",
                "max_results": 10,
                "include_metadata": True
            }
        }


class SearchResponse(BaseModel):
    """Response model for search API"""
    success: bool
    query: str
    results: List[Dict[str, Any]]
    total_hits: int
    execution_time_ms: float
    index_used: str
    routing_info: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for health check API"""
    status: str
    timestamp: str
    components: Dict[str, Any]
    detailed_checks: Dict[str, Any]


class SearchService:
    """
    Production-ready search service that uses pre-initialized components.
    This class provides clean, stateless methods for search operations.
    """
    
    def __init__(self):
        self._components = None
    
    def _get_components(self):
        """Get initialized components, with lazy loading if needed"""
        if self._components is None:
            self._components = get_components()
        return self._components
    
    async def search_healthcare_data(
        self, 
        query: str, 
        index_name: Optional[str] = None,
        max_results: int = 10,
        include_metadata: bool = True
    ) -> SearchResponse:
        """
        Search healthcare data using semantic search and OpenSearch.
        
        Args:
            query: Search query string
            index_name: Optional specific index to search
            max_results: Maximum number of results to return
            include_metadata: Whether to include metadata in response
            
        Returns:
            SearchResponse with search results and metadata
        """
        start_time = datetime.now()
        
        try:
            components = self._get_components()
            
            # Step 1: Route the query to determine the best index
            routing_result = None
            if not index_name and components.query_processor:
                try:
                    routing_result = components.query_processor.route_healthcare_query(query)
                    logger.debug(f"Routing result: {routing_result}")
                    
                    # Extract index name from routing result
                    if isinstance(routing_result, dict):
                        if "routing_analysis" in routing_result:
                            index_name = routing_result["routing_analysis"].get("primary_data_source")
                        elif "primary_data_source" in routing_result:
                            index_name = routing_result["primary_data_source"]
                    
                    # Default to claims index if routing failed or returned invalid index
                    if not index_name or index_name == "N/A":
                        index_name = "healthcare_claims_index"
                        
                except Exception as e:
                    logger.warning(f"Query routing failed: {e}")
                    index_name = "healthcare_claims_index"
            
            # Use default index if none specified
            if not index_name:
                index_name = "healthcare_claims_index"
            
            # Step 2: Generate OpenSearch DSL query
            dsl_query = None
            if components.dsl_generator:
                try:
                    dsl_query = components.dsl_generator.generate_dsl_query(query, index_name)
                    logger.debug(f"Generated DSL query: {dsl_query}")
                except Exception as e:
                    logger.error(f"DSL generation failed: {e}")
                    raise RuntimeError(f"Failed to generate search query: {e}")
            
            # Step 3: Execute query against OpenSearch
            search_results = None
            if components.query_executor_factory and dsl_query:
                try:
                    executor = components.query_executor_factory.create_executor()
                    search_results = executor.execute_query(dsl_query, index_name)
                    logger.debug(f"Search executed successfully, found {search_results.get('total_hits', 0)} results")
                except Exception as e:
                    logger.error(f"OpenSearch query execution failed: {e}")
                    raise RuntimeError(f"Failed to execute search: {e}")
            
            # Step 4: Format response
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            response_data = {
                "success": True,
                "query": query,
                "results": search_results.get("documents", [])[:max_results] if search_results else [],
                "total_hits": search_results.get("total_hits", 0) if search_results else 0,
                "execution_time_ms": execution_time,
                "index_used": index_name,
                "routing_info": routing_result if include_metadata else None,
                "error": None,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Search completed successfully: {query[:50]}... -> {response_data['total_hits']} results")
            return SearchResponse(**response_data)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            error_msg = f"Search failed: {str(e)}"
            logger.error(error_msg)
            
            return SearchResponse(
                success=False,
                query=query,
                results=[],
                total_hits=0,
                execution_time_ms=execution_time,
                index_used=index_name or "unknown",
                routing_info=None,
                error=error_msg,
                timestamp=datetime.now().isoformat()
            )
    
    async def get_health_status(self) -> HealthResponse:
        """
        Get comprehensive health status of all components.
        
        Returns:
            HealthResponse with detailed health information
        """
        try:
            health_data = health_check()
            
            return HealthResponse(
                status=health_data["overall_status"],
                timestamp=health_data["timestamp"],
                components=health_data["components"],
                detailed_checks=health_data["detailed_checks"]
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return HealthResponse(
                status="unhealthy",
                timestamp=datetime.now().isoformat(),
                components={"is_initialized": False},
                detailed_checks={"error": str(e)}
            )
    
    async def get_available_indexes(self) -> Dict[str, Any]:
        """
        Get list of available indexes and their metadata.
        
        Returns:
            Dictionary with available indexes information
        """
        try:
            components = self._get_components()
            
            if components.embedding_generator:
                stats = components.embedding_generator.get_consolidated_index_statistics()
                return {
                    "success": True,
                    "indexes": stats,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "Embedding generator not available",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get available indexes: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# Global service instance
_search_service = None


def get_search_service() -> SearchService:
    """
    Get the global search service instance.
    Creates a new instance if none exists.
    
    Returns:
        SearchService: Global search service instance
    """
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service


# Convenience functions for direct use
async def search_healthcare_data(
    query: str, 
    index_name: Optional[str] = None,
    max_results: int = 10,
    include_metadata: bool = True
) -> SearchResponse:
    """Convenience function for healthcare data search"""
    service = get_search_service()
    return await service.search_healthcare_data(query, index_name, max_results, include_metadata)


async def get_health_status() -> HealthResponse:
    """Convenience function for health check"""
    service = get_search_service()
    return await service.get_health_status()


async def get_available_indexes() -> Dict[str, Any]:
    """Convenience function for getting available indexes"""
    service = get_search_service()
    return await service.get_available_indexes()
