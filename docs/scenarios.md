# API des Scénarios

Cette documentation décrit l'API REST pour la gestion des scénarios.

## Endpoints

### Créer un scénario
```http
POST /scenarios/
```

Crée un nouveau scénario.

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "steps": [
    {
      "type": "string",
      "details": {}
    }
  ]
}
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "steps": [],
  "created_at": "string",
  "status": "string"
}
```

### Lister les scénarios
```http
GET /scenarios/
```

Récupère la liste de tous les scénarios disponibles.

**Response:**
```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "steps": [],
    "created_at": "string",
    "status": "string"
  }
]
```

### Récupérer un scénario
```http
GET /scenarios/{scenario_id}
```

Récupère les détails d'un scénario spécifique.

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "steps": [],
  "created_at": "string",
  "status": "string"
}
```

### Exécuter un scénario
```http
POST /scenarios/{scenario_id}/run
```

Exécute un scénario spécifique.

**Response:**
```json
{
  "scenario_id": "string",
  "status": "string",
  "steps": [
    {
      "type": "string",
      "status": "string",
      "result": {}
    }
  ]
}
```

### Ajouter une étape
```http
POST /scenarios/{scenario_id}/steps
```

Ajoute une nouvelle étape à un scénario existant.

**Request Body:**
```json
{
  "type": "string",
  "details": {}
}
```

**Response:**
```json
{
  "id": "string",
  "type": "string",
  "details": {}
}
```

### Télécharger un fichier
```http
POST /scenarios/{scenario_id}/upload
```

Télécharge un fichier pour un scénario spécifique.

**Request:**
- `file`: Fichier à télécharger (multipart/form-data)

**Response:**
```json
{
  "filename": "string",
  "size": "number",
  "uploaded_at": "string"
}
```

## Types d'étapes

### PDF
```json
{
  "type": "pdf",
  "file": "UploadFile"
}
```

### Template
```json
{
  "type": "template",
  "template": "string",
  "context": {}
}
```

## Codes d'erreur

- `400 Bad Request`: Requête invalide
- `404 Not Found`: Scénario non trouvé
- `500 Internal Server Error`: Erreur serveur

## Exemples

### Création d'un scénario avec une étape PDF
```json
{
  "name": "Extraction PDF",
  "description": "Extrait le texte d'un PDF",
  "steps": [
    {
      "type": "pdf",
      "file": "document.pdf"
    }
  ]
}
```

### Création d'un scénario avec une étape Template
```json
{
  "name": "Génération de rapport",
  "description": "Génère un rapport à partir d'un template",
  "steps": [
    {
      "type": "template",
      "template": "report.html",
      "context": {
        "title": "Rapport mensuel",
        "data": {}
      }
    }
  ]
}
``` 