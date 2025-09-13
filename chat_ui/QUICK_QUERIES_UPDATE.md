# Quick Queries Update - 15 Real Test Queries

## Overview
Updated the Quick Queries section with 15 real test queries selected from the comprehensive test files used for healthcare search testing.

## Query Categories

### Claims Queries (5 queries)
1. **Claims by Date Range**: "Show me all claims submitted between January 1, 2022 and March 31, 2022"
2. **Denied Claims by Provider**: "Find denied claims for provider ID 12345 in 2021"
3. **High-Cost Claims 2023**: "Find high-cost claims over $50,000 submitted in 2023"
4. **Claims by Procedure Code**: "Find claims with procedure code 99213 and their status"

### Provider Queries (4 queries)
5. **Cardiology Providers in CA**: "Find all cardiology providers in California"
6. **High-Rated Providers**: "Find providers with quality ratings above 4.0"
7. **Telehealth Providers**: "Find providers with telehealth capabilities"

### Member Queries (4 queries)
8. **Diabetic Members in CA**: "Find all members with diabetes in California"
9. **Medicare Members 65+**: "Find members aged 65 and older with Medicare plans"
10. **High-Risk Members**: "Get members with risk scores above 2.0"
11. **Inactive Members**: "Find members who haven't used services in 12 months"

### Procedure Queries (4 queries)
12. **Prior Auth Procedures**: "Find all procedures that require prior authorization"
13. **High RVU Procedures**: "Show procedures with RVU greater than 5.0"
14. **High-Cost Procedures**: "Show procedures with high allowed amounts over $1000"
15. **Cardiology Procedures**: "Get procedures in the cardiology specialty"

## Benefits of Updated Queries

### Real-World Relevance
- All queries are based on actual healthcare data scenarios
- Cover common healthcare analytics use cases
- Include specific technical terms (RVU, NPI, procedure codes)

### Comprehensive Coverage
- **Claims**: Date ranges, provider-specific, cost analysis, procedure codes
- **Providers**: Specialty, location, quality ratings, capabilities
- **Members**: Demographics, risk stratification, utilization patterns
- **Procedures**: Authorization requirements, cost analysis, specialty focus

### Testing Value
- Queries are proven to work with the healthcare search system
- Cover different confidence levels and routing scenarios
- Include both simple and complex query patterns

## Technical Details

### Query Sources
- **Claims**: From `claims_queries_001.json` (30 total queries)
- **Providers**: From `providers_queries_002.json` (30 total queries)  
- **Members**: From `members_queries_003.json` (40 total queries)
- **Procedures**: From `procedures_queries_004.json` (50 total queries)

### Selection Criteria
- Chose queries that represent common healthcare analytics needs
- Balanced across all four healthcare data categories
- Selected queries with clear, descriptive labels
- Included both simple and complex query patterns

### UI Integration
- All queries work with existing radio button selection system
- Compatible with the "Use Selected" and "Clear" functionality
- Properly formatted for the scrollable Quick Queries section
- Optimized spacing for better text visibility

## Usage
Users can now select from 15 real-world healthcare queries that demonstrate the full capabilities of the healthcare search assistant, covering claims analysis, provider management, member insights, and procedure research.
