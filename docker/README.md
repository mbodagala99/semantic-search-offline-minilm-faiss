# OpenSearch Docker Management

This folder contains everything needed to run OpenSearch in Docker/Podman containers with sample healthcare data.

## 🏗️ Structure

```
docker/
├── docker-compose.yml          # Main orchestration file
├── opensearch/                 # OpenSearch configuration
│   ├── Dockerfile             # Custom OpenSearch image
│   ├── opensearch.yml         # OpenSearch configuration
│   └── jvm.options           # JVM settings
├── data/                      # Sample data files (10K+ rows each)
│   ├── claims_data.json
│   ├── providers_data.json
│   ├── members_data.json
│   └── procedures_data.json
└── scripts/                   # Management scripts
    ├── start.sh              # Start containers
    ├── stop.sh               # Stop containers
    ├── status.sh             # Check status
    ├── load_data.sh          # Load sample data
    └── generate_sample_data.py # Generate sample data
```

## 🚀 Quick Start

### Prerequisites
- Podman or Docker installed
- `podman-compose` or `docker-compose` installed

### 1. Start Containers
```bash
cd docker/scripts
./start.sh
```

### 2. Check Status
```bash
./status.sh
```

### 3. Load Sample Data
```bash
./load_data.sh
```

### 4. Access Services
- **OpenSearch**: http://localhost:9200
- **Dashboards**: http://localhost:5601

## 📊 Sample Data

Each index contains **10,000+ sample records**:

- **Claims Index**: Healthcare claims with patient, provider, payer info
- **Providers Index**: Healthcare providers with credentials and contact info
- **Members Index**: Insurance members with benefits and enrollment info
- **Procedures Index**: Medical procedures with pricing and requirements

## 🛠️ Management Commands

| Command | Description |
|---------|-------------|
| `./start.sh` | Start OpenSearch and Dashboards containers |
| `./stop.sh` | Stop all containers |
| `./status.sh` | Check container and cluster health |
| `./load_data.sh` | Load sample data into indices |

## 🔧 Configuration

### OpenSearch Settings
- **Memory**: 1GB heap size
- **Security**: Disabled for development
- **Ports**: 9200 (HTTP), 9600 (Performance Analyzer)
- **Data**: Persistent volume for data retention

### Sample Data Generation
- **Claims**: 10,000 records with realistic healthcare data
- **Providers**: 10,000 records with medical specialties
- **Members**: 10,000 records with insurance plans
- **Procedures**: 10,000 records with medical procedures

## 🐳 Podman Compatibility

This setup is fully compatible with Podman:
- Uses `podman-compose` when available
- Falls back to `docker-compose` if needed
- All scripts work with both container runtimes

## 📝 Notes

- Data is persisted in Docker volumes
- Containers include health checks
- Sample data is generated automatically
- All scripts are executable and ready to use
