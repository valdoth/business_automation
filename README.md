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

### Authentication

- `POST /auth/token` - Get access token
- `POST /auth/register` - Register new user
- `GET /auth/me` - Get current user info

### Documents

- `GET /documents/` - Get all documents
- `POST /documents/` - Upload a new document
- `GET /documents/{document_id}` - Get a specific document
- `GET /documents/{document_id}/download` - Download a document
- `POST /documents/{document_id}/upload` - Upload a file for a document

### Variables

- `GET /variables/` - Get all variables
- `POST /variables/` - Create a new variable
- `GET /variables/{variable_id}` - Get a specific variable
- `PUT /variables/{variable_id}` - Update a variable
- `DELETE /variables/{variable_id}` - Delete a variable
- `GET /variables/document/{document_id}` - Get all variables for a document

### Scenarios

- `GET /scenarios/` - Get all scenarios
- `POST /scenarios/` - Create a new scenario
- `GET /scenarios/{scenario_id}` - Get a specific scenario
- `PUT /scenarios/{scenario_id}` - Update a scenario
- `DELETE /scenarios/{scenario_id}` - Delete a scenario
- `POST /scenarios/{scenario_id}/run` - Execute a scenario
- `POST /scenarios/from-pdf` - Create a scenario from PDF
- `POST /scenarios/{scenario_id}/upload` - Upload a file for a scenario

## Data Models

### Document
```json
{
  "id": "string",
  "type": "string",
  "minio_key": "string",
  "metadata": {},
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Variable
```json
{
  "id": "string",
  "name": "string",
  "value": "string",
  "description": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Scenario
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "steps": [],
  "created_at": "datetime",
  "updated_at": "datetime",
  "status": "string"
}
```

## Development

### Running Tests
```bash
pytest
```

MIT License
