#!/usr/bin/env python3
"""
Comprehensive Test script for Healthcare Query Router

This script tests the intelligent query routing capabilities
for healthcare data queries using semantic similarity search
with 120 comprehensive healthcare queries.
"""

import json
import csv
from datetime import datetime
from index_router import HealthcareQueryRouter, HealthcareQueryAnalyzer
from embedding_generator import EmbeddingGenerator


def test_healthcare_query_routing(query_router=None, save_results=True):
    """Test the healthcare query routing system with comprehensive healthcare queries."""
    
    if query_router is None:
        print("🏥 Healthcare Query Router - Comprehensive Test Suite")
        print("=" * 60)
        
        # Initialize the system
        embedding_gen = EmbeddingGenerator()
        query_router = HealthcareQueryRouter(embedding_gen)
        query_analyzer = HealthcareQueryAnalyzer(query_router)
    else:
        query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    # Comprehensive test queries
    test_queries = [
        {"query": "Show me all claims submitted between January 1, 2022 and March 31, 2022", "description": "Claims query with specific date range"},
        {"query": "Get the top 10 providers with the highest claim amounts in 2023", "description": "Provider ranking query with timeframe"},
        {"query": "List all pharmacy claims for diabetic patients after July 2021", "description": "Pharmacy claims with patient condition filter"},
        {"query": "Which providers had more than 500 claims in 2022?", "description": "Provider volume analysis query"},
        {"query": "Show outpatient claims for members over the age of 65 in Texas for 2021", "description": "Complex claims query with multiple filters"},
        {"query": "Retrieve claims rejected due to eligibility issues in 2023", "description": "Claims rejection analysis query"},
        {"query": "Show total paid amount by provider for Q4 of 2022", "description": "Provider payment summary query"},
        {"query": "Find all providers in Florida with average claim cost greater than $2,000", "description": "Provider cost analysis with location filter"},
        {"query": "Show ER claims filed in August 2021 by Blue Cross members", "description": "Emergency room claims with payer filter"},
        {"query": "Get total number of claims per member between 2020 and 2022", "description": "Member claims summary query"},
        {"query": "Show claims denied due to lack of prior authorization in first half of 2023", "description": "Claims denial analysis with authorization filter"},
        {"query": "Get the total paid amount for behavioral health services in 2022", "description": "Behavioral health payment analysis"},
        {"query": "List providers specializing in cardiology with more than 10,000 claims in 2021", "description": "Specialty provider volume analysis"},
        {"query": "Show member demographics for claim IDs 10001 through 10100", "description": "Member demographics query with claim ID range"},
        {"query": "Find monthly trend of dental claims in 2022", "description": "Dental claims trend analysis"},
        {"query": "Show average allowed amount for MRI procedures in 2021", "description": "Procedure cost analysis query"},
        {"query": "Which members had claims exceeding $50,000 in 2022?", "description": "High-cost member identification query"},
        {"query": "Find duplicate claims submitted between June and September 2021", "description": "Duplicate claims detection query"},
        {"query": "Get proportion of denied claims by provider specialty for 2022", "description": "Provider specialty denial analysis"},
        {"query": "Retrieve inpatient admission claims for children under 12 in 2020", "description": "Pediatric inpatient claims query"},
        {"query": "Get all maternity claims processed in 2021 and the total payment", "description": "Maternity claims and payment analysis"},
        {"query": "Show claims over $100,000 for oncology services in 2022", "description": "High-cost oncology claims query"},
        {"query": "List providers with highest claim denial rates in 2021", "description": "Provider denial rate analysis"},
        {"query": "Retrieve pharmacy data for insulin prescriptions in 2023", "description": "Pharmacy prescription analysis"},
        {"query": "Show count of claims filed per county in California for 2021", "description": "Geographic claims distribution analysis"},
        {"query": "Which providers submitted paper claims in January 2022?", "description": "Provider submission method analysis"},
        {"query": "Show claims pending for more than 60 days as of today", "description": "Pending claims analysis"},
        {"query": "Compare paid vs billed amounts across all claims in 2022", "description": "Claims payment comparison analysis"},
        {"query": "Show top 50 most expensive claims in 2023 to date", "description": "High-cost claims ranking query"},
        {"query": "Get list of providers with license numbers but missing NPI", "description": "Provider credentialing data quality query"},
        {"query": "Retrieve chiropractic claims in New York for 2020", "description": "Specialty claims with location filter"},
        {"query": "Show claims denied due to coordination of benefits between 2021–2022", "description": "Coordination of benefits denial analysis"},
        {"query": "Which procedure codes had highest denial rates in 2021?", "description": "Procedure code denial analysis"},
        {"query": "Get member claims summary with total billed and paid amounts for 2022", "description": "Member claims financial summary"},
        {"query": "Show claims for emergency transport services in 2021", "description": "Emergency transport claims analysis"},
        {"query": "Identify fraudulent claim patterns from Feb–Apr 2022", "description": "Fraud detection analysis query"},
        {"query": "Show outpatient surgery claims between July–Dec 2021", "description": "Outpatient surgery claims analysis"},
        {"query": "List members with more than 20 claims in a single month", "description": "High-utilization member identification"},
        {"query": "Find high-cost claims for premature newborns in 2020", "description": "Neonatal high-cost claims analysis"},
        {"query": "Show all claims for procedure code 99213 during Jan 2023", "description": "Specific procedure code claims query"},
        {"query": "Get all Tier-1 provider claims for PPO plan members in 2022", "description": "Provider tier and plan type analysis"},
        {"query": "Show denied claims due to missing documentation between Jan–Mar 2021", "description": "Documentation-related denial analysis"},
        {"query": "Get monthly pharmacy spend trends from 2019–2022", "description": "Pharmacy spending trend analysis"},
        {"query": "Show orthopedic provider claims in Illinois in Q3 2021", "description": "Specialty provider claims with location and time filter"},
        {"query": "List top 5 facilities by total inpatient costs in 2022", "description": "Facility cost ranking analysis"},
        {"query": "Retrieve claims of members with multiple chronic conditions in 2021", "description": "Chronic condition member claims analysis"},
        {"query": "Find member IDs with denied claims due to invalid diagnosis code", "description": "Diagnosis code validation analysis"},
        {"query": "Which facilities submitted claims with DRG code 470 in 2022?", "description": "DRG code facility analysis"},
        {"query": "Show telehealth claims in Q1 2022 compared to Q1 2021", "description": "Telehealth claims comparison analysis"},
        {"query": "Get total spend per member over lifetime claims", "description": "Lifetime member spending analysis"},
        {"query": "List all paid claims for HMO plan members in 2021", "description": "HMO plan claims analysis"},
        {"query": "Retrieve claims with partial payments issued in 2022", "description": "Partial payment claims analysis"},
        {"query": "Show total denied amount for provider ID 20045 in 2021", "description": "Specific provider denial analysis"},
        {"query": "Find trend in maternity-related claims from 2018 to 2022", "description": "Maternity claims trend analysis"},
        {"query": "Show claims denied by system error in July 2021", "description": "System error denial analysis"},
        {"query": "List providers who filed zero claims in 2022", "description": "Inactive provider identification"},
        {"query": "Show average turnaround time for claim payments between 2020–2022", "description": "Claims processing time analysis"},
        {"query": "Get all out-of-network claims for 2022", "description": "Out-of-network claims analysis"},
        {"query": "Show member claims split by gender in 2021", "description": "Gender-based claims analysis"},
        {"query": "Calculate readmission rates from claims data in 2020", "description": "Readmission rate calculation"},
        {"query": "Show rejected claims due to invalid subscriber ID in 2022", "description": "Subscriber ID validation analysis"},
        {"query": "List states with highest per-member claim costs in 2021", "description": "State-level cost analysis"},
        {"query": "Retrieve hospice claims between Jan 2020 and Jun 2021", "description": "Hospice claims analysis"},
        {"query": "Show procedure codes billed by provider ID 10123 during 2022", "description": "Provider procedure mix analysis"},
        {"query": "Get all mental health provider claims for adolescents in 2022", "description": "Mental health adolescent claims analysis"},
        {"query": "List all inpatient claims where stay exceeded 30 days", "description": "Long-stay inpatient claims analysis"},
        {"query": "Find duplicate member claims between Jan–Mar 2023", "description": "Duplicate member claims detection"},
        {"query": "Show all anesthesia-related claims in Q4 2020", "description": "Anesthesia claims analysis"},
        {"query": "Get breakdown of denied claims by payer type in 2021", "description": "Payer type denial analysis"},
        {"query": "Which providers exceeded $10M total claims in 2022?", "description": "High-volume provider identification"},
        {"query": "Show claims submitted with invalid CPT codes in 2021", "description": "CPT code validation analysis"},
        {"query": "Get all oncology-related claims filed after diagnosis", "description": "Oncology claims post-diagnosis analysis"},
        {"query": "Retrieve data on claims that required retroactive adjustment in 2022", "description": "Retroactive adjustment claims analysis"},
        {"query": "Show distribution of paid amounts for ER services in 2021", "description": "ER service payment distribution analysis"},
        {"query": "Find claim records tagged as high dollar outliers in 2020", "description": "High-dollar outlier claims analysis"},
        {"query": "List average payment lag time for orthopedic claims in 2022", "description": "Orthopedic claims payment timing analysis"},
        {"query": "Show member IDs with outstanding claim balances in 2023", "description": "Outstanding balance member identification"},
        {"query": "Retrieve procedure mix for provider ID 50089 during 2021", "description": "Specific provider procedure mix analysis"},
        {"query": "Show denied claims because service was not covered in 2021", "description": "Coverage-related denial analysis"},
        {"query": "Get claim amounts submitted through clearinghouse X in 2022", "description": "Clearinghouse submission analysis"},
        {"query": "List claims from rural providers in Kentucky for 2020", "description": "Rural provider claims analysis"},
        {"query": "Show claim payments broken down by funding arrangement in 2021", "description": "Funding arrangement payment analysis"},
        {"query": "Retrieve fraudulent claim flags in March 2022", "description": "Fraud flag analysis"},
        {"query": "Find most common procedures denied in Florida 2022", "description": "State-specific procedure denial analysis"},
        {"query": "Show specialty mix of providers with highest reimbursements in 2022", "description": "High-reimbursement provider specialty analysis"},
        {"query": "Get monthly summary of capitation vs fee-for-service claims", "description": "Payment model comparison analysis"},
        {"query": "Retrieve all outpatient claims over $25,000 from 2021", "description": "High-cost outpatient claims analysis"},
        {"query": "Show dental claim activity by provider network in 2020", "description": "Dental network activity analysis"},
        {"query": "List facilities with DRG code 291 in 2021", "description": "Specific DRG facility analysis"},
        {"query": "Get neonatal intensive care claims in 2021 and 2022", "description": "NICU claims analysis"},
        {"query": "Show providers filing highest number of appeals in 2022", "description": "Provider appeals analysis"},
        {"query": "Retrieve denied claims due to pre-existing condition clause", "description": "Pre-existing condition denial analysis"},
        {"query": "Show differences between billed and allowed amounts for 2022", "description": "Billed vs allowed amount analysis"},
        {"query": "Find claims for procedures conducted on weekends only", "description": "Weekend procedure claims analysis"},
        {"query": "Generate provider ranking by claim amounts in Texas, 2021", "description": "State-specific provider ranking analysis"},
        {"query": "Show pharmacy claims for controlled substances in 2022", "description": "Controlled substance pharmacy analysis"},
        {"query": "List inpatient claims associated with COVID-19 in 2020", "description": "COVID-19 inpatient claims analysis"},
        {"query": "Show all duplicate claim pairs across 2021", "description": "Comprehensive duplicate claims analysis"},
        {"query": "Retrieve members with more than $100K total annual claims", "description": "High-cost member identification"},
        {"query": "Find denial rate trends for cardiology specialty in 2020–2022", "description": "Specialty denial trend analysis"},
        {"query": "Show providers credentialed in 2020 but no claims filed", "description": "Inactive credentialed provider analysis"},
        {"query": "Get ER claim counts per member", "description": "ER utilization per member analysis"},
        {"query": "Show high-dollar transplant claims in 2022", "description": "Transplant claims analysis"},
        {"query": "Retrieve transitional care claims after hospital discharge", "description": "Transitional care claims analysis"},
        {"query": "Which counties in Texas had most ER claims in 2022?", "description": "County-level ER claims analysis"},
        {"query": "Show rejected claims for unlisted procedure codes", "description": "Unlisted procedure code analysis"},
        {"query": "Find trends in provider submission methods (EDI vs paper)", "description": "Submission method trend analysis"},
        {"query": "Compare member liabilities vs payer liabilities in 2021", "description": "Liability comparison analysis"},
        {"query": "Show lab claim volumes monthly across 2022", "description": "Lab claims volume trend analysis"},
        {"query": "Get longest length of stay claims with details", "description": "Longest stay claims analysis"},
        {"query": "Which providers submitted claims only during holiday weeks?", "description": "Holiday-only provider analysis"},
        {"query": "Show providers who had 100% claim acceptance rate in 2021", "description": "Perfect acceptance rate provider analysis"},
        {"query": "Find NPI mismatches in 2022 claim submissions", "description": "NPI validation analysis"},
        {"query": "Retrieve rolling 12-month claim costs for oncology", "description": "Rolling oncology cost analysis"},
        {"query": "Show inpatient claims trends vs outpatient claims trends in 2022", "description": "Inpatient vs outpatient trend comparison"},
        {"query": "Get percentage of denied ER claims in 2021", "description": "ER denial rate analysis"},
        {"query": "List all claims tied to catastrophic coverage in 2020", "description": "Catastrophic coverage claims analysis"},
        {"query": "Show pharmacy claims with brand vs generic splits by month", "description": "Brand vs generic pharmacy analysis"},
        {"query": "Retrieve anomaly in claims for provider ID 99999 in 2021", "description": "Provider anomaly detection analysis"},
        {"query": "Show behavioral health claims per member between 2020–2022", "description": "Behavioral health per-member analysis"}
    ]
    
    print(f"\n🔍 Testing {len(test_queries)} Comprehensive Healthcare Queries:")
    print("-" * 60)
    
    # Initialize results tracking
    results = []
    high_confidence_count = 0
    low_confidence_count = 0
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        description = test_case["description"]
        
        print(f"\n{i:3d}. {description}")
        print(f"     Query: '{query}'")
        print("-" * 50)
        
        # Route the query
        routing_result = query_router.route_healthcare_query(query)
        
        # Analyze the result
        analysis = routing_result["routing_analysis"]
        confidence_score = analysis["confidence_score"]
        routing_status = analysis["routing_status"]
        
        print(f"     Confidence: {confidence_score:.3f}")
        print(f"     Status: {routing_status}")
        
        # Count results
        if routing_status == "HIGH_CONFIDENCE":
            high_confidence_count += 1
            print(f"     ✅ High Confidence Match")
            print(f"     Data Source: {analysis['primary_data_source']}")
            print(f"     Recommendation: {routing_result['routing_recommendation']}")
        else:
            low_confidence_count += 1
            print(f"     ⚠️  Requires Clarification")
            clarification = routing_result["clarification_request"]
            print(f"     Message: {clarification['message']}")
            print(f"     Available Domains: {len(clarification['available_healthcare_domains'])}")
        
        # Get query recommendations
        recommendations = query_analyzer.get_query_recommendations(query)
        improvement_suggestions = recommendations["query_recommendations"]["improvement_suggestions"]
        
        if improvement_suggestions:
            print(f"     Improvement Suggestions: {len(improvement_suggestions)}")
            for suggestion in improvement_suggestions:
                print(f"     - {suggestion}")
        
        # Store result for output file
        result_entry = {
            "test_number": i,
            "query": query,
            "description": description,
            "confidence_score": confidence_score,
            "routing_status": routing_status,
            "primary_data_source": analysis.get('primary_data_source', 'N/A'),
            "recommendation": routing_result.get('routing_recommendation', 'N/A'),
            "improvement_suggestions_count": len(improvement_suggestions),
            "improvement_suggestions": "; ".join(improvement_suggestions) if improvement_suggestions else "None"
        }
        results.append(result_entry)
    
    # Summary
    print(f"\n📊 Comprehensive Test Results Summary:")
    print("-" * 40)
    print(f"   Total Queries Tested: {len(test_queries)}")
    print(f"   High Confidence Matches: {high_confidence_count}")
    print(f"   Low Confidence (Clarification): {low_confidence_count}")
    print(f"   Success Rate: {(high_confidence_count / len(test_queries)) * 100:.1f}%")
    
    result_data = {
        "total_queries": len(test_queries),
        "high_confidence_matches": high_confidence_count,
        "low_confidence_clarification": low_confidence_count,
        "success_rate": (high_confidence_count / len(test_queries)) * 100,
        "results": results
    }
    
    if save_results:
        # Generate output files
        json_filename, csv_filename, report_filename = generate_test_output_file(result_data)
        print(f"\n📁 Test Output Files Generated:")
        print(f"   JSON Results: {json_filename}")
        print(f"   CSV Results: {csv_filename}")
        print(f"   Summary Report: {report_filename}")
    
    return result_data


def generate_test_output_file(test_results):
    """Generate comprehensive test output files."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate JSON output file
    json_filename = f"healthcare_router_test_results_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)
    
    # Generate CSV output file
    csv_filename = f"healthcare_router_test_results_{timestamp}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        if test_results["results"]:
            fieldnames = test_results["results"][0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_results["results"])
    
    # Generate summary report
    report_filename = f"healthcare_router_test_summary_{timestamp}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("Healthcare Query Router - Comprehensive Test Results\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Queries Tested: {test_results['total_queries']}\n")
        f.write(f"High Confidence Matches: {test_results['high_confidence']}\n")
        f.write(f"Low Confidence (Clarification): {test_results['low_confidence']}\n")
        f.write(f"Success Rate: {test_results['success_rate']:.1f}%\n\n")
        
        f.write("Detailed Results:\n")
        f.write("-" * 30 + "\n")
        for result in test_results["results"]:
            f.write(f"\nTest {result['test_number']:3d}: {result['description']}\n")
            f.write(f"Query: {result['query']}\n")
            f.write(f"Confidence: {result['confidence_score']:.3f}\n")
            f.write(f"Status: {result['routing_status']}\n")
            if result['routing_status'] == 'HIGH_CONFIDENCE':
                f.write(f"Data Source: {result['primary_data_source']}\n")
                f.write(f"Recommendation: {result['recommendation']}\n")
            else:
                f.write(f"Improvement Suggestions: {result['improvement_suggestions']}\n")
    
    print(f"\n📁 Test Output Files Generated:")
    print(f"   JSON Results: {json_filename}")
    print(f"   CSV Results: {csv_filename}")
    print(f"   Summary Report: {report_filename}")
    
    return json_filename, csv_filename, report_filename


def main():
    """Main test function."""
    
    try:
        # Run comprehensive tests
        test_results = test_healthcare_query_routing()
        
        # Generate output files
        json_file, csv_file, report_file = generate_test_output_file(test_results)
        
        print(f"\n🎉 Comprehensive Tests Completed Successfully!")
        print(f"   Overall Success Rate: {test_results['success_rate']:.1f}%")
        print(f"   Output files generated for detailed analysis")
        
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
