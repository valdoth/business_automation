# AI-Powered Business Process Automation System

This project implements an AI-powered automation system for business processes using FastAPI, Neo4j, and MinIO. The system allows for the creation and execution of automated business scenarios using AI agents.

## Architecture

The system consists of the following main components:

- **FastAPI**: REST API backend
- **Neo4j**: Graph database for storing entities and relationships
- **MinIO**: Object storage for documents
- **AI Agents**: LLM-powered automation agents

### Core Entities

- **Document**: Files stored in MinIO with metadata
- **Variable**: Attributes linked to documents
- **Scenario**: Business process steps
- **Automation**: AI agent configurations

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Neo4j Desktop (for local development)
- MinIO Server

## Installation

1. Clone the repository:
```bash
git clone https://github.com/valdoth/business_automation
cd business_automation
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:
```bash
docker-compose up --build
```

## Usage

### Local Development

1. Start the services:
```bash
docker-compose up --build
```

2. Access the API at `http://localhost:8000`
3. Access the API documentation at `http://localhost:8000/docs`
   Access for MINIO: `http://127.0.0.1:9001/login`
   Access for Neo4j: `http://localhost:7474/browser/`


## API Endpoints

### Documents

- `GET /documents/` - Get all documents
- `POST /documents/` - Upload a new document
- `GET /documents/{document_id}` - Get a specific document
- `GET /documents/{document_id}/download` - Download a document

### Variables

- `GET /variables/` - Get all variables
- `POST /variables/` - Create a new variable
- `GET /variables/document/{document_id}` - Get all variables for a document
- `PUT /variables/{variable_id}` - Update a variable

### Scenarios

- `GET /scenarios/` - Get all scenarios
- `POST /scenarios/` - Create a new scenario
- `GET /scenarios/{scenario_id}` - Get a specific scenario
- `POST /scenarios/{scenario_id}/run` - Execute a scenario

## Testing

Run tests using:
```bash
pytest
```

## License

MIT License
