#!/usr/bin/env python3
"""
Enhance claims index mapping with generic versions of test queries
"""

import json
import re

def create_generic_queries():
    """Create generic versions of the test queries for claims index."""
    
    # Generic claims queries based on test results
    generic_claims_queries = {
        "claims_submission_analysis": {
            "category": "Claims Submission and Processing Analysis",
            "description": "Comprehensive analysis of claims submission patterns, processing workflows, and submission methods across different time periods and demographics.",
            "scenarios": [
                "Analyze claims submission patterns by date range and time periods",
                "Track claims processing workflows and submission methods",
                "Monitor claims submission volumes and trends over time",
                "Identify claims submission patterns by provider and specialty",
                "Analyze claims submission methods including electronic and paper submissions",
                "Track claims submission compliance and accuracy rates",
                "Monitor claims submission turnaround times and processing efficiency",
                "Analyze claims submission patterns by geographic region and payer type"
            ],
            "natural_language_prompts": [
                "Show me all claims submitted between specific date ranges",
                "Generate a report of claims submission patterns by month and quarter",
                "Find claims submitted through different methods like electronic and paper",
                "Show me claims submission trends over the last year",
                "Analyze claims submission volumes by provider and specialty",
                "Generate a report of claims submission compliance rates",
                "Show me claims submission turnaround times and processing efficiency",
                "Find claims submission patterns by geographic region and payer"
            ]
        },
        
        "provider_claims_analysis": {
            "category": "Provider Claims Volume and Performance Analysis",
            "description": "Comprehensive analysis of provider claims volume, performance metrics, and billing patterns including ranking and comparison analysis.",
            "scenarios": [
                "Analyze provider claims volume and ranking by total amounts",
                "Track provider claims performance metrics and billing patterns",
                "Monitor provider claims volume trends and capacity analysis",
                "Identify top performing providers by claims volume and amounts",
                "Analyze provider claims patterns by specialty and service type",
                "Track provider claims processing efficiency and turnaround times",
                "Monitor provider claims accuracy and error rates",
                "Analyze provider claims patterns by geographic location and payer type"
            ],
            "natural_language_prompts": [
                "Get the top providers with the highest claim amounts",
                "Show me provider claims volume analysis and ranking",
                "Find providers with the most claims submitted",
                "Generate a report of provider claims performance metrics",
                "Show me provider claims trends and capacity analysis",
                "Find top performing providers by claims volume and amounts",
                "Analyze provider claims patterns by specialty and service",
                "Show me provider claims processing efficiency and accuracy"
            ]
        },
        
        "pharmacy_claims_analysis": {
            "category": "Pharmacy Claims and Prescription Analysis",
            "description": "Comprehensive analysis of pharmacy claims, prescription patterns, and medication utilization including patient condition filtering and drug analysis.",
            "scenarios": [
                "Analyze pharmacy claims by patient condition and diagnosis",
                "Track prescription patterns and medication utilization trends",
                "Monitor pharmacy claims by drug type and therapeutic class",
                "Identify pharmacy claims patterns by patient demographics",
                "Analyze pharmacy claims by provider and pharmacy network",
                "Track pharmacy claims spending trends and cost analysis",
                "Monitor pharmacy claims compliance and formulary adherence",
                "Analyze pharmacy claims by geographic region and payer type"
            ],
            "natural_language_prompts": [
                "List all pharmacy claims for specific patient conditions",
                "Show me pharmacy claims analysis by drug type and class",
                "Find pharmacy claims patterns by patient demographics",
                "Generate a report of pharmacy claims spending trends",
                "Show me pharmacy claims by provider and network",
                "Analyze pharmacy claims compliance and formulary adherence",
                "Find pharmacy claims patterns by geographic region",
                "Show me pharmacy claims analysis by payer type and coverage"
            ]
        },
        
        "claims_denial_analysis": {
            "category": "Claims Denial and Rejection Analysis",
            "description": "Comprehensive analysis of claims denials, rejections, and adjustment patterns including reason analysis and trend monitoring.",
            "scenarios": [
                "Analyze claims denials by reason and rejection category",
                "Track claims denial trends and patterns over time",
                "Monitor claims denials by provider and specialty",
                "Identify claims denials by payer type and coverage issues",
                "Analyze claims denials by procedure and service type",
                "Track claims denial rates and improvement opportunities",
                "Monitor claims denials by geographic region and demographics",
                "Analyze claims denials by authorization and eligibility issues"
            ],
            "natural_language_prompts": [
                "Retrieve claims rejected due to eligibility issues",
                "Show me claims denied due to lack of prior authorization",
                "Find claims denials by reason and rejection category",
                "Generate a report of claims denial trends and patterns",
                "Show me claims denials by provider and specialty",
                "Analyze claims denials by payer type and coverage",
                "Find claims denials by procedure and service type",
                "Show me claims denial rates and improvement opportunities"
            ]
        },
        
        "payment_analysis": {
            "category": "Payment Processing and Financial Analysis",
            "description": "Comprehensive analysis of payment processing, financial reconciliation, and payment pattern analysis including partial payments and funding arrangements.",
            "scenarios": [
                "Analyze payment processing by provider and time period",
                "Track payment reconciliation and financial accuracy",
                "Monitor partial payments and payment adjustments",
                "Identify payment patterns by payer type and funding arrangement",
                "Analyze payment processing times and efficiency metrics",
                "Track payment amounts and financial performance analysis",
                "Monitor payment compliance and regulatory requirements",
                "Analyze payment patterns by geographic region and demographics"
            ],
            "natural_language_prompts": [
                "Show total paid amount by provider for specific time periods",
                "Retrieve claims with partial payments issued",
                "Show claim payments broken down by funding arrangement",
                "Find payment processing times and efficiency metrics",
                "Generate a report of payment amounts and financial performance",
                "Show me payment patterns by payer type and arrangement",
                "Analyze payment compliance and regulatory requirements",
                "Find payment patterns by geographic region and demographics"
            ]
        },
        
        "specialty_claims_analysis": {
            "category": "Specialty Claims and Service Analysis",
            "description": "Comprehensive analysis of specialty claims including cardiology, oncology, orthopedic, and other medical specialties with procedure and service analysis.",
            "scenarios": [
                "Analyze specialty claims by medical specialty and procedure type",
                "Track specialty claims volume and cost analysis",
                "Monitor specialty claims by provider and facility type",
                "Identify specialty claims patterns by patient demographics",
                "Analyze specialty claims by payer type and coverage level",
                "Track specialty claims trends and utilization patterns",
                "Monitor specialty claims quality metrics and outcomes",
                "Analyze specialty claims by geographic region and access"
            ],
            "natural_language_prompts": [
                "Show orthopedic provider claims in specific locations",
                "Find cardiology claims analysis and trends",
                "Generate a report of oncology claims and costs",
                "Show me specialty claims by provider and facility",
                "Analyze specialty claims patterns by patient demographics",
                "Find specialty claims by payer type and coverage",
                "Show me specialty claims trends and utilization",
                "Generate a report of specialty claims quality metrics"
            ]
        },
        
        "geographic_claims_analysis": {
            "category": "Geographic Claims Distribution and Analysis",
            "description": "Comprehensive analysis of claims distribution by geographic regions including state, county, and regional analysis with demographic considerations.",
            "scenarios": [
                "Analyze claims distribution by state and geographic region",
                "Track claims patterns by county and local area",
                "Monitor claims by rural and urban geographic classification",
                "Identify claims patterns by geographic access and availability",
                "Analyze claims by geographic demographics and population",
                "Track claims trends by geographic region and time period",
                "Monitor claims by geographic payer mix and coverage",
                "Analyze claims by geographic provider network and access"
            ],
            "natural_language_prompts": [
                "Show count of claims filed per county in specific states",
                "List claims from rural providers in specific regions",
                "Find claims patterns by geographic region and demographics",
                "Generate a report of claims by state and county",
                "Show me claims trends by geographic region and time",
                "Analyze claims by geographic payer mix and coverage",
                "Find claims by geographic provider network and access",
                "Show me claims distribution by rural and urban areas"
            ]
        },
        
        "temporal_claims_analysis": {
            "category": "Temporal Claims Trends and Time-based Analysis",
            "description": "Comprehensive analysis of claims trends over time including monthly, quarterly, and annual patterns with seasonal and cyclical analysis.",
            "scenarios": [
                "Analyze claims trends by month and quarterly periods",
                "Track claims patterns by year and annual cycles",
                "Monitor claims by seasonal patterns and holiday periods",
                "Identify claims trends by time of day and week",
                "Analyze claims by specific date ranges and periods",
                "Track claims trends by decade and long-term patterns",
                "Monitor claims by fiscal year and reporting periods",
                "Analyze claims by specific time-based criteria and filters"
            ],
            "natural_language_prompts": [
                "Find monthly trend of claims in specific years",
                "Show claims trends from specific date ranges",
                "Generate a report of claims by quarter and year",
                "Find claims patterns by seasonal and holiday periods",
                "Show me claims trends by time of day and week",
                "Analyze claims by specific date ranges and periods",
                "Find claims trends by decade and long-term patterns",
                "Show me claims by fiscal year and reporting periods"
            ]
        },
        
        "high_cost_claims_analysis": {
            "category": "High-Cost Claims and Outlier Analysis",
            "description": "Comprehensive analysis of high-cost claims, outliers, and expensive procedures including cost threshold analysis and anomaly detection.",
            "scenarios": [
                "Analyze high-cost claims above specific dollar thresholds",
                "Track expensive procedures and outlier claims",
                "Monitor high-cost claims by provider and specialty",
                "Identify high-cost claims by patient demographics",
                "Analyze high-cost claims by payer type and coverage",
                "Track high-cost claims trends and cost escalation",
                "Monitor high-cost claims by geographic region",
                "Analyze high-cost claims by procedure type and complexity"
            ],
            "natural_language_prompts": [
                "Show top most expensive claims in specific years",
                "Find claims over specific dollar amounts",
                "Generate a report of high-cost claims and outliers",
                "Show me expensive procedures and cost analysis",
                "Find high-cost claims by provider and specialty",
                "Analyze high-cost claims by patient demographics",
                "Show me high-cost claims trends and escalation",
                "Find high-cost claims by geographic region and payer"
            ]
        },
        
        "duplicate_claims_analysis": {
            "category": "Duplicate Claims Detection and Analysis",
            "description": "Comprehensive analysis of duplicate claims, potential fraud indicators, and claims integrity including detection algorithms and pattern analysis.",
            "scenarios": [
                "Detect duplicate claims and potential fraud patterns",
                "Track duplicate claims by provider and submission method",
                "Monitor duplicate claims by patient and member",
                "Identify duplicate claims by procedure and service type",
                "Analyze duplicate claims by payer and coverage type",
                "Track duplicate claims trends and detection rates",
                "Monitor duplicate claims by geographic region",
                "Analyze duplicate claims by time period and submission date"
            ],
            "natural_language_prompts": [
                "Find duplicate claims submitted between specific periods",
                "Show all duplicate claim pairs across specific years",
                "Find duplicate member claims between specific months",
                "Generate a report of duplicate claims detection",
                "Show me duplicate claims by provider and method",
                "Find duplicate claims by patient and member",
                "Analyze duplicate claims by procedure and service",
                "Show me duplicate claims trends and detection rates"
            ]
        }
    }
    
    return generic_claims_queries

def enhance_claims_index():
    """Enhance the claims index mapping file with new use cases."""
    
    # Load current claims index
    with open('data/opensearch/claims_index_mapping_expanded.json', 'r') as f:
        claims_index = json.load(f)
    
    # Get new use cases
    new_use_cases = create_generic_queries()
    
    # Add new use cases to existing ones
    for use_case_key, use_case_data in new_use_cases.items():
        claims_index['_meta']['use_cases'].append(use_case_data)
    
    # Add new report categories
    new_reports = {
        "report_type": "Comprehensive Claims Analysis Reports",
        "description": "Advanced claims analysis reports covering submission patterns, provider performance, specialty analysis, geographic distribution, temporal trends, high-cost analysis, and duplicate detection.",
        "report_categories": [
            {
                "category": "Claims Submission Pattern Analysis",
                "description": "Detailed analysis of claims submission patterns, methods, and processing workflows.",
                "sample_prompts": [
                    "Show me all claims submitted between specific date ranges",
                    "Generate a report of claims submission patterns by month and quarter",
                    "Find claims submitted through different methods like electronic and paper",
                    "Show me claims submission trends over the last year",
                    "Analyze claims submission volumes by provider and specialty"
                ],
                "filters": [
                    "Date range: specific periods, quarters, years",
                    "Submission method: electronic, paper, EDI, clearinghouse",
                    "Provider type: individual, group, facility, network",
                    "Specialty: cardiology, oncology, orthopedic, etc.",
                    "Payer type: commercial, Medicare, Medicaid, self-pay"
                ]
            },
            {
                "category": "Provider Claims Performance Analysis",
                "description": "Comprehensive provider claims performance analysis including volume, amounts, and ranking.",
                "sample_prompts": [
                    "Get the top providers with the highest claim amounts",
                    "Show me provider claims volume analysis and ranking",
                    "Find providers with the most claims submitted",
                    "Generate a report of provider claims performance metrics",
                    "Show me provider claims trends and capacity analysis"
                ],
                "filters": [
                    "Provider ranking: top 10, top 50, top 100",
                    "Time period: specific years, quarters, months",
                    "Amount thresholds: specific dollar amounts",
                    "Volume thresholds: specific claim counts",
                    "Specialty: specific medical specialties"
                ]
            },
            {
                "category": "Pharmacy Claims and Prescription Analysis",
                "description": "Detailed pharmacy claims analysis including prescription patterns and medication utilization.",
                "sample_prompts": [
                    "List all pharmacy claims for specific patient conditions",
                    "Show me pharmacy claims analysis by drug type and class",
                    "Find pharmacy claims patterns by patient demographics",
                    "Generate a report of pharmacy claims spending trends",
                    "Show me pharmacy claims by provider and network"
                ],
                "filters": [
                    "Patient condition: diabetes, hypertension, etc.",
                    "Drug type: brand, generic, controlled substances",
                    "Therapeutic class: specific medication classes",
                    "Patient demographics: age, gender, location",
                    "Time period: specific date ranges"
                ]
            },
            {
                "category": "Claims Denial and Rejection Analysis",
                "description": "Comprehensive analysis of claims denials, rejections, and adjustment patterns.",
                "sample_prompts": [
                    "Retrieve claims rejected due to eligibility issues",
                    "Show me claims denied due to lack of prior authorization",
                    "Find claims denials by reason and rejection category",
                    "Generate a report of claims denial trends and patterns",
                    "Show me claims denials by provider and specialty"
                ],
                "filters": [
                    "Denial reason: eligibility, authorization, coverage, etc.",
                    "Provider specialty: specific medical specialties",
                    "Payer type: specific insurance companies",
                    "Time period: specific date ranges",
                    "Denial rate: specific percentage thresholds"
                ]
            },
            {
                "category": "Geographic Claims Distribution Analysis",
                "description": "Detailed analysis of claims distribution by geographic regions and demographics.",
                "sample_prompts": [
                    "Show count of claims filed per county in specific states",
                    "List claims from rural providers in specific regions",
                    "Find claims patterns by geographic region and demographics",
                    "Generate a report of claims by state and county",
                    "Show me claims trends by geographic region and time"
                ],
                "filters": [
                    "Geographic region: state, county, city, zip code",
                    "Rural/Urban classification: rural, urban, metropolitan",
                    "Demographics: age, gender, income, education",
                    "Time period: specific date ranges",
                    "Provider type: rural, urban, academic, community"
                ]
            },
            {
                "category": "High-Cost Claims and Outlier Analysis",
                "description": "Comprehensive analysis of high-cost claims, outliers, and expensive procedures.",
                "sample_prompts": [
                    "Show top most expensive claims in specific years",
                    "Find claims over specific dollar amounts",
                    "Generate a report of high-cost claims and outliers",
                    "Show me expensive procedures and cost analysis",
                    "Find high-cost claims by provider and specialty"
                ],
                "filters": [
                    "Cost thresholds: $10K, $25K, $50K, $100K, $250K",
                    "Provider specialty: specific medical specialties",
                    "Procedure type: specific procedures and services",
                    "Time period: specific date ranges",
                    "Payer type: specific insurance companies"
                ]
            }
        ]
    }
    
    # Add new reports to existing ones
    claims_index['_meta']['reports_generated'].append(new_reports)
    
    # Save enhanced claims index
    with open('data/opensearch/claims_index_mapping_expanded.json', 'w') as f:
        json.dump(claims_index, f, indent=2)
    
    print("✅ Enhanced claims index mapping with new use cases and reports")
    print(f"   Added {len(new_use_cases)} new use cases")
    print(f"   Added 1 new comprehensive report category with 6 subcategories")

if __name__ == "__main__":
    enhance_claims_index()
