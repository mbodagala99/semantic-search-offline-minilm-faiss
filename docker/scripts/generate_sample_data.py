#!/usr/bin/env python3
"""
Generate sample data for OpenSearch indices.
Creates 10,000+ rows for each healthcare index.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_claims_data(count: int = 10000) -> List[Dict[str, Any]]:
    """Generate sample claims data."""
    claims = []
    
    # Sample data pools
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily", "James", "Jessica"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    providers = ["City Medical Center", "Regional Hospital", "Community Clinic", "Specialty Care", "Family Practice"]
    payers = ["Blue Cross", "Aetna", "Cigna", "UnitedHealth", "Medicare", "Medicaid"]
    procedures = ["Office Visit", "Lab Work", "X-Ray", "MRI", "Surgery", "Physical Therapy", "Consultation"]
    statuses = ["Paid", "Pending", "Denied", "Under Review", "Partial Payment"]
    
    for i in range(count):
        claim_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        claim = {
            "claim_id": f"CLM-{datetime.now().year}-{str(i+1).zfill(6)}",
            "patient": {
                "first_name": random.choice(first_names),
                "last_name": random.choice(last_names),
                "date_of_birth": f"{random.randint(1950, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "member_id": f"MEM-{random.randint(100000, 999999)}"
            },
            "provider": {
                "name": random.choice(providers),
                "npi": f"{random.randint(1000000000, 9999999999)}",
                "specialty": random.choice(["Internal Medicine", "Cardiology", "Dermatology", "Pediatrics", "Orthopedics"])
            },
            "payer": {
                "name": random.choice(payers),
                "payer_id": f"PAY-{random.randint(100000, 999999)}"
            },
            "claim_details": {
                "claim_date": claim_date.strftime("%Y-%m-%d"),
                "service_date": (claim_date - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "claim_type": random.choice(["Professional", "Institutional", "Pharmacy"]),
                "claim_status": random.choice(statuses),
                "billed_amount": round(random.uniform(100, 5000), 2),
                "allowed_amount": round(random.uniform(80, 4000), 2),
                "paid_amount": round(random.uniform(0, 4000), 2)
            },
            "service_lines": [
                {
                    "procedure_code": f"CPT-{random.randint(10000, 99999)}",
                    "procedure_description": random.choice(procedures),
                    "quantity": random.randint(1, 5),
                    "unit_price": round(random.uniform(50, 500), 2)
                }
                for _ in range(random.randint(1, 3))
            ],
            "adjustments": [
                {
                    "adjustment_type": random.choice(["Contractual", "Patient Responsibility", "Denial"]),
                    "adjustment_reason": random.choice(["CO-45", "CO-97", "CO-96", "CO-23"]),
                    "adjustment_amount": round(random.uniform(10, 200), 2)
                }
                for _ in range(random.randint(0, 2))
            ],
            "edi_835_info": {
                "transaction_id": f"TXN-{random.randint(100000000, 999999999)}",
                "check_number": f"CHK-{random.randint(100000, 999999)}",
                "check_date": (claim_date + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            }
        }
        claims.append(claim)
    
    return claims

def generate_providers_data(count: int = 10000) -> List[Dict[str, Any]]:
    """Generate sample providers data."""
    providers = []
    
    first_names = ["Dr. John", "Dr. Jane", "Dr. Michael", "Dr. Sarah", "Dr. David", "Dr. Lisa", "Dr. Robert", "Dr. Emily"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    specialties = ["Internal Medicine", "Cardiology", "Dermatology", "Pediatrics", "Orthopedics", "Neurology", "Oncology", "Radiology"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA"]
    
    for i in range(count):
        provider = {
            "provider_id": f"PROV-{str(i+1).zfill(6)}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "npi": f"{random.randint(1000000000, 9999999999)}",
            "specialty": random.choice(specialties),
            "credentials": {
                "medical_license": f"MD-{random.randint(100000, 999999)}",
                "dea_number": f"DEA-{random.randint(1000000, 9999999)}",
                "board_certified": random.choice([True, False])
            },
            "contact": {
                "phone": f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "email": f"provider{i+1}@example.com",
                "website": f"https://provider{i+1}.com"
            },
            "address": {
                "street": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar'])} St",
                "city": random.choice(cities),
                "state": random.choice(states),
                "zip_code": f"{random.randint(10000, 99999)}"
            },
            "practice_info": {
                "practice_name": f"{random.choice(['Medical', 'Health', 'Care', 'Clinic'])} {random.choice(['Center', 'Group', 'Associates'])}",
                "practice_type": random.choice(["Individual", "Group Practice", "Hospital", "Clinic"]),
                "years_in_practice": random.randint(1, 40),
                "accepting_new_patients": random.choice([True, False])
            },
            "network_status": {
                "in_network": random.choice([True, False]),
                "contract_effective_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d"),
                "contract_expiry_date": (datetime.now() + timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d")
            },
            "performance_metrics": {
                "patient_satisfaction_score": round(random.uniform(3.0, 5.0), 1),
                "average_rating": round(random.uniform(3.0, 5.0), 1),
                "total_patients": random.randint(50, 2000),
                "years_experience": random.randint(1, 40)
            }
        }
        providers.append(provider)
    
    return providers

def generate_members_data(count: int = 10000) -> List[Dict[str, Any]]:
    """Generate sample members data."""
    members = []
    
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily", "James", "Jessica", "Christopher", "Amanda"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
    plans = ["HMO", "PPO", "EPO", "POS", "HDHP"]
    
    for i in range(count):
        birth_year = random.randint(1950, 2005)
        member = {
            "member_id": f"MEM-{str(i+1).zfill(6)}",
            "personal_info": {
                "first_name": random.choice(first_names),
                "last_name": random.choice(last_names),
                "date_of_birth": f"{birth_year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "gender": random.choice(["M", "F", "Other"]),
                "ssn": f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
            },
            "contact": {
                "phone": f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "email": f"member{i+1}@example.com",
                "address": {
                    "street": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar'])} St",
                    "city": random.choice(cities),
                    "state": random.choice(states),
                    "zip_code": f"{random.randint(10000, 99999)}"
                }
            },
            "insurance": {
                "plan_type": random.choice(plans),
                "plan_name": f"{random.choice(['Gold', 'Silver', 'Bronze', 'Platinum'])} {random.choice(['Health', 'Care', 'Plus'])} Plan",
                "group_number": f"GRP-{random.randint(100000, 999999)}",
                "policy_number": f"POL-{random.randint(100000000, 999999999)}",
                "effective_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d"),
                "expiry_date": (datetime.now() + timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d")
            },
            "benefits": {
                "deductible": random.randint(500, 5000),
                "out_of_pocket_max": random.randint(1000, 10000),
                "copay_primary": random.randint(10, 50),
                "copay_specialist": random.randint(25, 100),
                "prescription_tier_1": random.randint(5, 25),
                "prescription_tier_2": random.randint(15, 50),
                "prescription_tier_3": random.randint(30, 100)
            },
            "enrollment": {
                "enrollment_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d"),
                "status": random.choice(["Active", "Inactive", "Suspended", "Terminated"]),
                "coverage_type": random.choice(["Individual", "Family", "Employee", "Dependent"])
            }
        }
        members.append(member)
    
    return members

def generate_procedures_data(count: int = 10000) -> List[Dict[str, Any]]:
    """Generate sample procedures data."""
    procedures = []
    
    procedure_names = [
        "Office Visit - New Patient", "Office Visit - Established Patient", "Annual Physical Exam",
        "Blood Test - Complete Blood Count", "X-Ray - Chest", "MRI - Brain", "CT Scan - Abdomen",
        "Echocardiogram", "Colonoscopy", "Mammography", "Pap Smear", "Flu Vaccination",
        "Surgery - Appendectomy", "Surgery - Gallbladder Removal", "Physical Therapy Session",
        "Psychiatric Evaluation", "Dermatology Consultation", "Cardiology Consultation"
    ]
    
    categories = ["Preventive", "Diagnostic", "Therapeutic", "Surgical", "Emergency", "Rehabilitation"]
    body_systems = ["Cardiovascular", "Respiratory", "Gastrointestinal", "Neurological", "Musculoskeletal", "Dermatological"]
    
    for i in range(count):
        procedure = {
            "procedure_id": f"PROC-{str(i+1).zfill(6)}",
            "procedure_name": random.choice(procedure_names),
            "cpt_code": f"CPT-{random.randint(10000, 99999)}",
            "icd10_code": f"ICD10-{random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])}{random.randint(10, 99)}.{random.randint(10, 99)}",
            "category": random.choice(categories),
            "body_system": random.choice(body_systems),
            "description": f"Medical procedure for {random.choice(['diagnosis', 'treatment', 'prevention', 'monitoring'])}",
            "duration_minutes": random.randint(15, 240),
            "complexity": random.choice(["Low", "Medium", "High"]),
            "anesthesia_required": random.choice([True, False]),
            "facility_requirements": {
                "outpatient": random.choice([True, False]),
                "inpatient": random.choice([True, False]),
                "specialized_equipment": random.choice([True, False]),
                "operating_room": random.choice([True, False])
            },
            "pricing": {
                "base_fee": round(random.uniform(50, 2000), 2),
                "facility_fee": round(random.uniform(0, 1000), 2),
                "anesthesia_fee": round(random.uniform(0, 500), 2),
                "total_estimated_cost": round(random.uniform(100, 3000), 2)
            },
            "requirements": {
                "prior_authorization": random.choice([True, False]),
                "referral_required": random.choice([True, False]),
                "specialist_required": random.choice([True, False]),
                "age_restrictions": random.choice([True, False])
            },
            "quality_metrics": {
                "success_rate": round(random.uniform(85, 99), 1),
                "complication_rate": round(random.uniform(0.1, 5.0), 1),
                "patient_satisfaction": round(random.uniform(3.0, 5.0), 1),
                "recovery_time_days": random.randint(1, 30)
            }
        }
        procedures.append(procedure)
    
    return procedures

def main():
    """Generate all sample data files."""
    print("Generating sample data for OpenSearch indices...")
    
    # Generate data
    print("Generating claims data...")
    claims_data = generate_claims_data(10000)
    
    print("Generating providers data...")
    providers_data = generate_providers_data(10000)
    
    print("Generating members data...")
    members_data = generate_members_data(10000)
    
    print("Generating procedures data...")
    procedures_data = generate_procedures_data(10000)
    
    # Save to files
    print("Saving data files...")
    
    with open('../data/claims_data.json', 'w') as f:
        json.dump(claims_data, f, indent=2)
    
    with open('../data/providers_data.json', 'w') as f:
        json.dump(providers_data, f, indent=2)
    
    with open('../data/members_data.json', 'w') as f:
        json.dump(members_data, f, indent=2)
    
    with open('../data/procedures_data.json', 'w') as f:
        json.dump(procedures_data, f, indent=2)
    
    print(f"✅ Generated {len(claims_data)} claims records")
    print(f"✅ Generated {len(providers_data)} providers records")
    print(f"✅ Generated {len(members_data)} members records")
    print(f"✅ Generated {len(procedures_data)} procedures records")
    print("Sample data generation completed!")

if __name__ == "__main__":
    main()
