from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BaseEntity(BaseModel):
    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Document(BaseEntity):
    type: str = Field(..., description="Document type (e.g., invoice, contract)")
    minio_key: str = Field(..., description="Key in MinIO storage")
    metadata: dict = Field(default_factory=dict)

class Variable(BaseEntity):
    name: str = Field(..., description="Variable name")
    value: str = Field(..., description="Variable value")
    document_id: str = Field(..., description="Associated document ID")

class Scenario(BaseEntity):
    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    steps: list[dict] = Field(..., description="List of scenario steps")
    document_ids: list[str] = Field(default_factory=list)
    variable_ids: list[str] = Field(default_factory=list)

class Automation(BaseEntity):
    scenario_id: str = Field(..., description="Associated scenario ID")
    ai_model: str = Field(..., description="AI model to use")
    parameters: dict = Field(default_factory=dict)
    status: str = Field(default="inactive", description="Automation status") 