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
git clone [repository-url]
cd [repository-name]
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start the services:
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

### Google Colab

A Jupyter notebook is provided for running the system in Google Colab. See `notebooks/colab_demo.ipynb` for details.

## API Endpoints

- `POST /scenarios/`: Create a new scenario
- `POST /scenarios/{id}/run`: Execute a scenario
- `GET /documents/`: List documents
- `POST /documents/`: Upload a document
- `GET /variables/`: List variables
- `POST /variables/`: Create a variable

## Testing

Run tests using:
```bash
pytest
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 