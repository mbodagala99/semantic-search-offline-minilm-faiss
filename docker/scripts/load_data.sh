#!/bin/bash
# Load sample data into OpenSearch indices

echo "📊 Loading sample data into OpenSearch indices..."

# Wait for OpenSearch to be ready
echo "⏳ Waiting for OpenSearch to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
        echo "✅ OpenSearch is ready!"
        break
    else
        echo "Waiting... ($i/30)"
        sleep 2
    fi
done

# Create indices with mappings
echo "📋 Creating indices..."

# Claims index
curl -X PUT "localhost:9200/healthcare_claims_index" -H 'Content-Type: application/json' -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "claim_id": {"type": "keyword"},
      "patient": {
        "properties": {
          "first_name": {"type": "text"},
          "last_name": {"type": "text"},
          "date_of_birth": {"type": "date"},
          "member_id": {"type": "keyword"}
        }
      },
      "provider": {
        "properties": {
          "name": {"type": "text"},
          "npi": {"type": "keyword"},
          "specialty": {"type": "keyword"}
        }
      },
      "payer": {
        "properties": {
          "name": {"type": "keyword"},
          "payer_id": {"type": "keyword"}
        }
      },
      "claim_details": {
        "properties": {
          "claim_date": {"type": "date"},
          "service_date": {"type": "date"},
          "claim_type": {"type": "keyword"},
          "claim_status": {"type": "keyword"},
          "billed_amount": {"type": "float"},
          "allowed_amount": {"type": "float"},
          "paid_amount": {"type": "float"}
        }
      }
    }
  }
}'

# Providers index
curl -X PUT "localhost:9200/healthcare_providers_index" -H 'Content-Type: application/json' -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "provider_id": {"type": "keyword"},
      "name": {"type": "text"},
      "npi": {"type": "keyword"},
      "specialty": {"type": "keyword"},
      "credentials": {
        "properties": {
          "medical_license": {"type": "keyword"},
          "dea_number": {"type": "keyword"},
          "board_certified": {"type": "boolean"}
        }
      },
      "contact": {
        "properties": {
          "phone": {"type": "keyword"},
          "email": {"type": "keyword"}
        }
      },
      "address": {
        "properties": {
          "city": {"type": "keyword"},
          "state": {"type": "keyword"},
          "zip_code": {"type": "keyword"}
        }
      }
    }
  }
}'

# Members index
curl -X PUT "localhost:9200/healthcare_members_index" -H 'Content-Type: application/json' -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "member_id": {"type": "keyword"},
      "personal_info": {
        "properties": {
          "first_name": {"type": "text"},
          "last_name": {"type": "text"},
          "date_of_birth": {"type": "date"},
          "gender": {"type": "keyword"}
        }
      },
      "insurance": {
        "properties": {
          "plan_type": {"type": "keyword"},
          "plan_name": {"type": "text"},
          "group_number": {"type": "keyword"},
          "policy_number": {"type": "keyword"}
        }
      },
      "benefits": {
        "properties": {
          "deductible": {"type": "integer"},
          "out_of_pocket_max": {"type": "integer"},
          "copay_primary": {"type": "integer"}
        }
      }
    }
  }
}'

# Procedures index
curl -X PUT "localhost:9200/healthcare_procedures_index" -H 'Content-Type: application/json' -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "procedure_id": {"type": "keyword"},
      "procedure_name": {"type": "text"},
      "cpt_code": {"type": "keyword"},
      "icd10_code": {"type": "keyword"},
      "category": {"type": "keyword"},
      "body_system": {"type": "keyword"},
      "description": {"type": "text"},
      "duration_minutes": {"type": "integer"},
      "complexity": {"type": "keyword"},
      "pricing": {
        "properties": {
          "base_fee": {"type": "float"},
          "total_estimated_cost": {"type": "float"}
        }
      }
    }
  }
}'

echo "✅ Indices created successfully!"

# Load sample data
echo "📊 Loading sample data..."

# Generate sample data if not exists
if [ ! -f "../data/claims_data.json" ]; then
    echo "Generating sample data..."
    python3 generate_sample_data.py
fi

# Load claims data
echo "Loading claims data..."
curl -X POST "localhost:9200/healthcare_claims_index/_bulk" -H 'Content-Type: application/json' --data-binary @<(cat ../data/claims_data.json | jq -c '.[] | {"index": {"_index": "healthcare_claims_index"}}, .')

# Load providers data
echo "Loading providers data..."
curl -X POST "localhost:9200/healthcare_providers_index/_bulk" -H 'Content-Type: application/json' --data-binary @<(cat ../data/providers_data.json | jq -c '.[] | {"index": {"_index": "healthcare_providers_index"}}, .')

# Load members data
echo "Loading members data..."
curl -X POST "localhost:9200/healthcare_members_index/_bulk" -H 'Content-Type: application/json' --data-binary @<(cat ../data/members_data.json | jq -c '.[] | {"index": {"_index": "healthcare_members_index"}}, .')

# Load procedures data
echo "Loading procedures data..."
curl -X POST "localhost:9200/healthcare_procedures_index/_bulk" -H 'Content-Type: application/json' --data-binary @<(cat ../data/procedures_data.json | jq -c '.[] | {"index": {"_index": "healthcare_procedures_index"}}, .')

echo "✅ Sample data loaded successfully!"

# Show index stats
echo "📊 Index statistics:"
curl -s "localhost:9200/_cat/indices?v"
