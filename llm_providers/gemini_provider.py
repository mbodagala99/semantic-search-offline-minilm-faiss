#!/usr/bin/env python3
"""
Google Gemini LLM Provider

This module implements the Google Gemini LLM provider for DSL query generation.
"""

import time
import json
from typing import Dict, Any, Optional
import google.generativeai as genai
from .base_llm_provider import BaseLLMProvider, LLMResponse


class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini LLM provider implementation.
    
    Provides DSL query generation using Google's Gemini API.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro", **kwargs):
        """
        Initialize the Gemini provider.
        
        Args:
            api_key: Google AI API key
            model_name: Gemini model name (default: gemini-1.5-pro)
            **kwargs: Additional parameters
        """
        super().__init__(api_key, model_name, **kwargs)
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Default parameters
        self.temperature = kwargs.get('temperature', 0.1)
        self.max_tokens = kwargs.get('max_tokens', 1000)
        self.top_p = kwargs.get('top_p', 0.8)
        self.top_k = kwargs.get('top_k', 40)
    
    def generate_dsl_query(
        self, 
        user_query: str, 
        index_info: Dict[str, Any], 
        schema_info: Dict[str, Any],
        dsl_type: str = "opensearch"
    ) -> LLMResponse:
        """
        Generate DSL query using Google Gemini.
        
        Args:
            user_query: Original user query
            index_info: Information about the identified index
            schema_info: Schema information for the data source
            dsl_type: Type of DSL to generate
            
        Returns:
            LLMResponse containing the generated DSL query
        """
        start_time = time.time()
        
        try:
            # Create the structured prompt for OpenSearch DSL generation
            prompt = self._create_structured_opensearch_prompt(
                user_query, index_info, schema_info
            )
            
            # Try up to 3 times to get a valid JSON response
            max_retries = 3
            structured_response = None
            
            for attempt in range(max_retries):
                try:
                    # Generate response using Gemini
                    response = self.model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=self.temperature,
                            max_output_tokens=self.max_tokens,
                            top_p=self.top_p,
                            top_k=self.top_k
                        )
                    )
                    
                    # Parse and validate the structured JSON response
                    structured_response = self._parse_structured_response(response.text)
                    break  # Success, exit retry loop
                    
                except ValueError as e:
                    if attempt < max_retries - 1:
                        # Add retry instruction to prompt for next attempt
                        prompt += f"\n\n⚠️ RETRY {attempt + 2}: Previous response was invalid. {str(e)}. RESPOND WITH ONLY VALID JSON:"
                        continue
                    else:
                        # Final attempt failed
                        raise e
            
            processing_time = (time.time() - start_time) * 1000
            
            # Create usage stats
            usage_stats = {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response.text.split()),
                "total_tokens": len(prompt.split()) + len(response.text.split()),
                "retry_attempts": attempt + 1
            }
            
            return self._create_success_response(
                content=structured_response,
                usage_stats=usage_stats,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return self._create_error_response(
                f"Gemini API error: {str(e)}",
                processing_time
            )
    
    def generate_query_explanation(
        self, 
        dsl_query: str, 
        user_query: str
    ) -> LLMResponse:
        """
        Generate explanation of the DSL query using Gemini.
        
        Args:
            dsl_query: The generated DSL query
            user_query: Original user query
            
        Returns:
            LLMResponse containing the explanation
        """
        start_time = time.time()
        
        try:
            prompt = f"""
            Explain the following {dsl_query.split()[0].upper()} query in simple terms:
            
            Original User Query: {user_query}
            Generated Query: {dsl_query}
            
            Please provide:
            1. What this query does
            2. What data it will retrieve
            3. Any important considerations
            """
            
            response = self.model.generate_content(prompt)
            processing_time = (time.time() - start_time) * 1000
            
            return self._create_success_response(
                content=response.text,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return self._create_error_response(
                f"Gemini explanation error: {str(e)}",
                processing_time
            )
    
    def validate_query_safety(
        self, 
        dsl_query: str
    ) -> LLMResponse:
        """
        Validate DSL query safety using Gemini.
        
        Args:
            dsl_query: The DSL query to validate
            
        Returns:
            LLMResponse indicating if query is safe
        """
        start_time = time.time()
        
        try:
            prompt = f"""
            Analyze the following query for safety and security issues:
            
            Query: {dsl_query}
            
            Check for:
            1. SQL injection vulnerabilities
            2. Unauthorized data access
            3. Performance issues (e.g., SELECT *)
            4. Sensitive data exposure
            5. Malicious operations
            
            Respond with JSON:
            {{
                "is_safe": true/false,
                "issues": ["list of issues if any"],
                "recommendations": ["list of recommendations"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            processing_time = (time.time() - start_time) * 1000
            
            # Parse JSON response
            try:
                safety_data = json.loads(response.text)
                is_safe = safety_data.get("is_safe", False)
                
                if is_safe:
                    return self._create_success_response(
                        content="Query is safe to execute",
                        processing_time_ms=processing_time
                    )
                else:
                    issues = safety_data.get("issues", [])
                    return self._create_error_response(
                        f"Query safety issues: {', '.join(issues)}",
                        processing_time
                    )
            except json.JSONDecodeError:
                return self._create_error_response(
                    "Could not parse safety validation response",
                    processing_time
                )
                
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return self._create_error_response(
                f"Gemini safety validation error: {str(e)}",
                processing_time
            )
    
    def is_available(self) -> bool:
        """
        Check if Gemini provider is available.
        
        Returns:
            True if available, False otherwise
        """
        try:
            # Test with a simple request
            test_response = self.model.generate_content("Test")
            return test_response is not None
        except Exception:
            return False
    
    def _create_structured_opensearch_prompt(
        self, 
        user_query: str, 
        index_info: Dict[str, Any], 
        schema_info: Dict[str, Any]
    ) -> str:
        """
        Create a structured prompt for OpenSearch DSL generation.
        
        Args:
            user_query: Original user query
            index_info: Index information
            schema_info: Schema information
            
        Returns:
            Formatted prompt string with strict JSON requirements
        """
        return f"""
🚨 CRITICAL INSTRUCTION: RESPOND WITH ONLY VALID JSON - NO OTHER TEXT 🚨

You are an OpenSearch DSL expert. Your response must be ONLY a valid JSON object.

❌ DO NOT INCLUDE:
- Explanations
- Headers like "Here is the query:"
- Markdown formatting
- Code blocks
- Any text before or after JSON
- Comments or descriptions

✅ ONLY INCLUDE:
- Valid JSON object starting with {{ and ending with }}

User Query: {user_query}

Index: {index_info.get('index_name', 'healthcare_claims_index')}
Schema: {json.dumps(schema_info, indent=2)}

REQUIRED FORMAT - RESPOND WITH ONLY THIS JSON STRUCTURE:
{{
  "index_name": "{index_info.get('index_name', 'healthcare_claims_index')}",
  "query_type": "search",
  "opensearch_dsl": {{
    "query": {{
      "bool": {{
        "must": [
          {{
            "match": {{
              "field_name": "search_term"
            }}
          }}
        ],
        "filter": [
          {{
            "range": {{
              "date_field": {{
                "gte": "2024-01-01"
              }}
            }}
          }}
        ]
      }}
    }},
    "size": 100,
    "sort": [
      {{
        "date_field": {{
          "order": "desc"
        }}
      }}
    ]
  }}
}}

INSTRUCTIONS:
1. Replace field_name with actual schema fields
2. Replace search_term with query-relevant terms
3. Replace date_field with appropriate date fields
4. Use proper OpenSearch DSL syntax
5. Add filters based on user query
6. Set size limit (max 1000)
7. Add sorting when relevant

🚨 FINAL WARNING: RESPOND WITH ONLY THE JSON OBJECT - NO OTHER TEXT 🚨

JSON RESPONSE:
"""
    
    def _parse_structured_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse and validate structured JSON response from Gemini with multiple extraction strategies.
        
        Args:
            response_text: Raw response from Gemini
            
        Returns:
            Parsed and validated structured response
            
        Raises:
            ValueError: If response is not valid JSON or missing required fields
        """
        # Try multiple extraction strategies
        extraction_strategies = [
            self._extract_json_direct,
            self._extract_json_with_cleaning,
            self._extract_json_with_regex,
            self._extract_json_with_boundaries
        ]
        
        for strategy in extraction_strategies:
            try:
                cleaned_response = strategy(response_text)
                if cleaned_response:
                    structured_data = json.loads(cleaned_response)
                    
                    # Validate required fields
                    if self._validate_structured_data(structured_data):
                        return structured_data
                        
            except (json.JSONDecodeError, ValueError) as e:
                continue
        
        # If all strategies fail, raise error with original response for debugging
        raise ValueError(f"Could not extract valid JSON from response: {response_text[:200]}...")
    
    def _extract_json_direct(self, response_text: str) -> str:
        """Try to parse JSON directly without cleaning."""
        return response_text.strip()
    
    def _extract_json_with_cleaning(self, response_text: str) -> str:
        """Extract JSON with basic cleaning."""
        return self._clean_response_text(response_text)
    
    def _extract_json_with_regex(self, response_text: str) -> str:
        """Extract JSON using regex patterns."""
        import re
        
        # Find JSON object boundaries using regex
        json_pattern = r'\{.*\}'
        matches = re.findall(json_pattern, response_text, re.DOTALL)
        
        if matches:
            # Return the longest match (most likely to be complete)
            return max(matches, key=len)
        
        return ""
    
    def _extract_json_with_boundaries(self, response_text: str) -> str:
        """Extract JSON by finding object boundaries."""
        # Find first { and last }
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            return response_text[start_idx:end_idx + 1]
        
        return ""
    
    def _validate_structured_data(self, data: Dict[str, Any]) -> bool:
        """Validate that structured data has required fields and structure."""
        try:
            # Check required fields
            required_fields = ['index_name', 'query_type', 'opensearch_dsl']
            for field in required_fields:
                if field not in data:
                    return False
            
            # Validate OpenSearch DSL structure
            dsl = data['opensearch_dsl']
            if not isinstance(dsl, dict) or 'query' not in dsl:
                return False
            
            return True
        except Exception:
            return False
    
    def _clean_response_text(self, response_text: str) -> str:
        """
        Clean response text to extract JSON with aggressive cleaning.
        
        Args:
            response_text: Raw response from Gemini
            
        Returns:
            Cleaned JSON string
        """
        # Remove any leading/trailing whitespace
        cleaned = response_text.strip()
        
        # Remove common prefixes that LLMs add
        prefixes_to_remove = [
            "Here is the OpenSearch DSL query:",
            "Here's the OpenSearch DSL query:",
            "The OpenSearch DSL query is:",
            "OpenSearch DSL Query:",
            "Here is the query:",
            "Here's the query:",
            "The query is:",
            "Query:",
            "Response:",
            "Answer:",
            "Result:",
            "```json",
            "```",
            "JSON:",
            "json:"
        ]
        
        for prefix in prefixes_to_remove:
            if cleaned.lower().startswith(prefix.lower()):
                cleaned = cleaned[len(prefix):].strip()
        
        # Remove markdown code blocks
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        # Remove any text before the first {
        start_idx = cleaned.find('{')
        if start_idx > 0:
            cleaned = cleaned[start_idx:]
        
        # Remove any text after the last }
        end_idx = cleaned.rfind('}')
        if end_idx != -1 and end_idx < len(cleaned) - 1:
            cleaned = cleaned[:end_idx + 1]
        
        return cleaned.strip()
