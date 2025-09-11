#!/usr/bin/env python3
"""
Enhance providers index mapping with generic versions of test queries
"""

import json

def create_generic_provider_queries():
    """Create generic versions of the provider-related test queries."""
    
    # Generic provider queries based on test results
    generic_provider_queries = {
        "provider_credentialing_analysis": {
            "category": "Provider Credentialing and Compliance Analysis",
            "description": "Comprehensive analysis of provider credentialing status, compliance verification, and credentialing data quality including missing information and validation issues.",
            "scenarios": [
                "Analyze provider credentialing status and compliance verification",
                "Track provider license numbers and NPI validation issues",
                "Monitor provider credentialing data quality and completeness",
                "Identify providers with missing or incomplete credentialing information",
                "Analyze provider credentialing compliance by specialty and location",
                "Track provider credentialing renewal requirements and deadlines",
                "Monitor provider credentialing data accuracy and validation",
                "Analyze provider credentialing patterns by organization and network"
            ],
            "natural_language_prompts": [
                "Get list of providers with license numbers but missing NPI",
                "Show me providers with incomplete credentialing information",
                "Find providers with credentialing data quality issues",
                "Generate a report of provider credentialing compliance status",
                "Show me providers with missing or invalid credentialing data",
                "Find providers with credentialing validation problems",
                "Analyze provider credentialing completeness by specialty",
                "Show me providers with credentialing data accuracy issues"
            ]
        },
        
        "provider_cost_analysis": {
            "category": "Provider Cost and Financial Performance Analysis",
            "description": "Comprehensive analysis of provider cost patterns, financial performance, and billing behavior including cost thresholds and financial metrics.",
            "scenarios": [
                "Analyze provider cost patterns and financial performance metrics",
                "Track provider average claim costs and cost thresholds",
                "Monitor provider cost analysis by geographic location",
                "Identify providers with high-cost patterns and outliers",
                "Analyze provider cost trends and financial performance",
                "Track provider cost analysis by specialty and service type",
                "Monitor provider cost patterns by payer type and coverage",
                "Analyze provider cost analysis by patient demographics and volume"
            ],
            "natural_language_prompts": [
                "Find all providers with average claim cost greater than specific amounts",
                "Show me provider cost analysis by geographic location",
                "Generate a report of provider cost patterns and trends",
                "Find providers with high-cost patterns and outliers",
                "Show me provider cost analysis by specialty and service",
                "Analyze provider cost trends and financial performance",
                "Find provider cost patterns by payer type and coverage",
                "Show me provider cost analysis by patient demographics"
            ]
        },
        
        "provider_network_analysis": {
            "category": "Provider Network Management and Analysis",
            "description": "Comprehensive analysis of provider network performance, network adequacy, and network optimization including coverage analysis and network metrics.",
            "scenarios": [
                "Analyze provider network coverage and adequacy by specialty",
                "Track provider network performance metrics and quality indicators",
                "Monitor provider network utilization patterns and capacity",
                "Identify provider network gaps and coverage issues",
                "Analyze provider network optimization opportunities",
                "Track provider network compliance and regulatory requirements",
                "Monitor provider network expansion and strategic planning",
                "Analyze provider network performance by geographic region"
            ],
            "natural_language_prompts": [
                "Show me provider network coverage gaps by specialty and location",
                "Find provider network adequacy analysis and metrics",
                "Generate a report of provider network performance indicators",
                "Show me provider network utilization patterns and capacity",
                "Find provider network gaps and coverage issues",
                "Analyze provider network optimization opportunities",
                "Show me provider network compliance and regulatory status",
                "Find provider network expansion and strategic planning needs"
            ]
        },
        
        "provider_performance_metrics": {
            "category": "Provider Performance Metrics and Quality Analysis",
            "description": "Comprehensive analysis of provider performance metrics, quality indicators, and outcome measures including ranking and benchmarking analysis.",
            "scenarios": [
                "Analyze provider performance metrics and quality indicators",
                "Track provider performance ranking and benchmarking analysis",
                "Monitor provider performance by specialty and service type",
                "Identify top performing providers by various metrics",
                "Analyze provider performance trends and improvement opportunities",
                "Track provider performance by patient demographics and outcomes",
                "Monitor provider performance by payer type and coverage",
                "Analyze provider performance by geographic region and access"
            ],
            "natural_language_prompts": [
                "Show me provider performance metrics and quality indicators",
                "Find top performing providers by various performance metrics",
                "Generate a report of provider performance ranking and benchmarking",
                "Show me provider performance by specialty and service type",
                "Analyze provider performance trends and improvement opportunities",
                "Find provider performance by patient demographics and outcomes",
                "Show me provider performance by payer type and coverage",
                "Generate a report of provider performance by geographic region"
            ]
        },
        
        "provider_specialty_analysis": {
            "category": "Provider Specialty and Service Analysis",
            "description": "Comprehensive analysis of provider specialties, service offerings, and specialty-specific performance including specialty distribution and analysis.",
            "scenarios": [
                "Analyze provider specialty distribution and coverage",
                "Track provider specialty performance and quality metrics",
                "Monitor provider specialty utilization patterns and trends",
                "Identify provider specialty gaps and coverage needs",
                "Analyze provider specialty trends and market analysis",
                "Track provider specialty compliance and regulatory requirements",
                "Monitor provider specialty expansion and recruitment needs",
                "Analyze provider specialty performance by geographic region"
            ],
            "natural_language_prompts": [
                "Show me provider specialty distribution and coverage analysis",
                "Find provider specialty performance and quality metrics",
                "Generate a report of provider specialty utilization patterns",
                "Show me provider specialty gaps and coverage needs",
                "Analyze provider specialty trends and market analysis",
                "Find provider specialty compliance and regulatory status",
                "Show me provider specialty expansion and recruitment needs",
                "Generate a report of provider specialty performance by region"
            ]
        },
        
        "provider_geographic_analysis": {
            "category": "Provider Geographic Distribution and Analysis",
            "description": "Comprehensive analysis of provider geographic distribution, location-based performance, and geographic coverage including rural and urban analysis.",
            "scenarios": [
                "Analyze provider geographic distribution and coverage",
                "Track provider location-based performance and metrics",
                "Monitor provider geographic coverage gaps and needs",
                "Identify provider geographic distribution patterns and trends",
                "Analyze provider geographic performance by specialty and service",
                "Track provider geographic compliance and regulatory requirements",
                "Monitor provider geographic expansion and strategic planning",
                "Analyze provider geographic performance by patient demographics"
            ],
            "natural_language_prompts": [
                "Show me provider geographic distribution and coverage analysis",
                "Find provider location-based performance and metrics",
                "Generate a report of provider geographic coverage gaps",
                "Show me provider geographic distribution patterns and trends",
                "Analyze provider geographic performance by specialty",
                "Find provider geographic compliance and regulatory status",
                "Show me provider geographic expansion and planning needs",
                "Generate a report of provider geographic performance by demographics"
            ]
        },
        
        "provider_utilization_analysis": {
            "category": "Provider Utilization and Capacity Analysis",
            "description": "Comprehensive analysis of provider utilization patterns, capacity management, and utilization trends including volume analysis and capacity planning.",
            "scenarios": [
                "Analyze provider utilization patterns and capacity management",
                "Track provider utilization trends and volume analysis",
                "Monitor provider capacity constraints and utilization rates",
                "Identify provider utilization optimization opportunities",
                "Analyze provider utilization by specialty and service type",
                "Track provider utilization by patient demographics and volume",
                "Monitor provider utilization by payer type and coverage",
                "Analyze provider utilization by geographic region and access"
            ],
            "natural_language_prompts": [
                "Show me provider utilization patterns and capacity management",
                "Find provider utilization trends and volume analysis",
                "Generate a report of provider capacity constraints and rates",
                "Show me provider utilization optimization opportunities",
                "Analyze provider utilization by specialty and service",
                "Find provider utilization by patient demographics and volume",
                "Show me provider utilization by payer type and coverage",
                "Generate a report of provider utilization by geographic region"
            ]
        },
        
        "provider_quality_analysis": {
            "category": "Provider Quality Metrics and Outcome Analysis",
            "description": "Comprehensive analysis of provider quality metrics, outcome measures, and quality indicators including quality ranking and improvement analysis.",
            "scenarios": [
                "Analyze provider quality metrics and outcome measures",
                "Track provider quality ranking and benchmarking analysis",
                "Monitor provider quality improvement opportunities and trends",
                "Identify top quality providers by various quality metrics",
                "Analyze provider quality trends and performance indicators",
                "Track provider quality by specialty and service type",
                "Monitor provider quality by patient demographics and outcomes",
                "Analyze provider quality by geographic region and access"
            ],
            "natural_language_prompts": [
                "Show me provider quality metrics and outcome measures",
                "Find top quality providers by various quality metrics",
                "Generate a report of provider quality ranking and benchmarking",
                "Show me provider quality improvement opportunities and trends",
                "Analyze provider quality trends and performance indicators",
                "Find provider quality by specialty and service type",
                "Show me provider quality by patient demographics and outcomes",
                "Generate a report of provider quality by geographic region"
            ]
        }
    }
    
    return generic_provider_queries

def enhance_providers_index():
    """Enhance the providers index mapping file with new use cases."""
    
    # Load current providers index
    with open('data/opensearch/providers_index_mapping_expanded.json', 'r') as f:
        providers_index = json.load(f)
    
    # Get new use cases
    new_use_cases = create_generic_provider_queries()
    
    # Add new use cases to existing ones
    for use_case_key, use_case_data in new_use_cases.items():
        providers_index['_meta']['use_cases'].append(use_case_data)
    
    # Add new report categories
    new_reports = {
        "report_type": "Comprehensive Provider Analysis Reports",
        "description": "Advanced provider analysis reports covering credentialing, cost analysis, network management, performance metrics, specialty analysis, geographic distribution, utilization patterns, and quality metrics.",
        "report_categories": [
            {
                "category": "Provider Credentialing and Compliance Reports",
                "description": "Detailed analysis of provider credentialing status, compliance verification, and credentialing data quality.",
                "sample_prompts": [
                    "Get list of providers with license numbers but missing NPI",
                    "Show me providers with incomplete credentialing information",
                    "Find providers with credentialing data quality issues",
                    "Generate a report of provider credentialing compliance status",
                    "Show me providers with missing or invalid credentialing data"
                ],
                "filters": [
                    "Credentialing status: complete, incomplete, expired, missing",
                    "Data quality: valid, invalid, missing, incomplete",
                    "Provider type: individual, group, facility, network",
                    "Specialty: specific medical specialties",
                    "Geographic region: state, county, city, zip code"
                ]
            },
            {
                "category": "Provider Cost and Financial Performance Reports",
                "description": "Comprehensive analysis of provider cost patterns, financial performance, and billing behavior.",
                "sample_prompts": [
                    "Find all providers with average claim cost greater than specific amounts",
                    "Show me provider cost analysis by geographic location",
                    "Generate a report of provider cost patterns and trends",
                    "Find providers with high-cost patterns and outliers",
                    "Show me provider cost analysis by specialty and service"
                ],
                "filters": [
                    "Cost thresholds: specific dollar amounts and ranges",
                    "Geographic location: state, county, city, rural/urban",
                    "Provider specialty: specific medical specialties",
                    "Time period: specific date ranges and periods",
                    "Payer type: commercial, Medicare, Medicaid, self-pay"
                ]
            },
            {
                "category": "Provider Network Management Reports",
                "description": "Detailed analysis of provider network performance, network adequacy, and network optimization.",
                "sample_prompts": [
                    "Show me provider network coverage gaps by specialty and location",
                    "Find provider network adequacy analysis and metrics",
                    "Generate a report of provider network performance indicators",
                    "Show me provider network utilization patterns and capacity",
                    "Find provider network gaps and coverage issues"
                ],
                "filters": [
                    "Network type: HMO, PPO, EPO, POS, Medicare, Medicaid",
                    "Specialty coverage: specific medical specialties",
                    "Geographic region: state, county, city, rural/urban",
                    "Network adequacy: adequate, inadequate, gaps",
                    "Performance metrics: quality, access, cost, satisfaction"
                ]
            },
            {
                "category": "Provider Performance Metrics Reports",
                "description": "Comprehensive analysis of provider performance metrics, quality indicators, and outcome measures.",
                "sample_prompts": [
                    "Show me provider performance metrics and quality indicators",
                    "Find top performing providers by various performance metrics",
                    "Generate a report of provider performance ranking and benchmarking",
                    "Show me provider performance by specialty and service type",
                    "Analyze provider performance trends and improvement opportunities"
                ],
                "filters": [
                    "Performance metrics: quality, efficiency, cost, satisfaction",
                    "Provider ranking: top 10, top 50, top 100, bottom performers",
                    "Specialty: specific medical specialties",
                    "Time period: specific date ranges and periods",
                    "Benchmarking: industry standards, peer comparison"
                ]
            },
            {
                "category": "Provider Specialty and Service Reports",
                "description": "Detailed analysis of provider specialties, service offerings, and specialty-specific performance.",
                "sample_prompts": [
                    "Show me provider specialty distribution and coverage analysis",
                    "Find provider specialty performance and quality metrics",
                    "Generate a report of provider specialty utilization patterns",
                    "Show me provider specialty gaps and coverage needs",
                    "Analyze provider specialty trends and market analysis"
                ],
                "filters": [
                    "Specialty type: primary care, specialty care, subspecialty",
                    "Service offerings: specific services and procedures",
                    "Geographic region: state, county, city, rural/urban",
                    "Market analysis: competition, demand, supply",
                    "Performance metrics: quality, access, cost, satisfaction"
                ]
            },
            {
                "category": "Provider Geographic Distribution Reports",
                "description": "Comprehensive analysis of provider geographic distribution, location-based performance, and geographic coverage.",
                "sample_prompts": [
                    "Show me provider geographic distribution and coverage analysis",
                    "Find provider location-based performance and metrics",
                    "Generate a report of provider geographic coverage gaps",
                    "Show me provider geographic distribution patterns and trends",
                    "Analyze provider geographic performance by specialty"
                ],
                "filters": [
                    "Geographic region: state, county, city, zip code",
                    "Rural/Urban classification: rural, urban, metropolitan",
                    "Provider type: individual, group, facility, network",
                    "Specialty: specific medical specialties",
                    "Performance metrics: quality, access, cost, satisfaction"
                ]
            }
        ]
    }
    
    # Add new reports to existing ones
    providers_index['_meta']['reports_generated'].append(new_reports)
    
    # Save enhanced providers index
    with open('data/opensearch/providers_index_mapping_expanded.json', 'w') as f:
        json.dump(providers_index, f, indent=2)
    
    print("✅ Enhanced providers index mapping with new use cases and reports")
    print(f"   Added {len(new_use_cases)} new use cases")
    print(f"   Added 1 new comprehensive report category with 6 subcategories")

if __name__ == "__main__":
    enhance_providers_index()
