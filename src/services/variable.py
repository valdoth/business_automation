from typing import List, Optional
from src.db.session import get_db
from src.models.variable import VariableCreate, VariableUpdate
from src.core.config import settings

class VariableService:
    @staticmethod
    async def create_variable(variable: VariableCreate) -> dict:
        with get_db() as session:
            result = session.run(
                """
                CREATE (v:Variable {
                    name: $name,
                    value: $value,
                    description: $description,
                    created_at: datetime(),
                    updated_at: datetime()
                })
                RETURN v
                """,
                name=variable.name,
                value=variable.value,
                description=variable.description
            )
            return dict(result.single()["v"])

    @staticmethod
    async def list_variables() -> List[dict]:
        with get_db() as session:
            result = session.run(
                """
                MATCH (v:Variable)
                RETURN v
                ORDER BY v.created_at DESC
                """
            )
            return [dict(record["v"]) for record in result]

    @staticmethod
    async def get_variable(variable_id: str) -> Optional[dict]:
        with get_db() as session:
            result = session.run(
                """
                MATCH (v:Variable)
                WHERE v.name = $variable_id
                RETURN v
                """,
                variable_id=variable_id
            )
            record = result.single()
            return dict(record["v"]) if record else None

    @staticmethod
    async def update_variable(variable_id: str, variable: VariableUpdate) -> Optional[dict]:
        with get_db() as session:
            result = session.run(
                """
                MATCH (v:Variable)
                WHERE v.name = $variable_id
                SET v.value = $value,
                    v.description = $description,
                    v.updated_at = datetime()
                RETURN v
                """,
                variable_id=variable_id,
                value=variable.value,
                description=variable.description
            )
            record = result.single()
            return dict(record["v"]) if record else None

    @staticmethod
    async def delete_variable(variable_id: str) -> bool:
        with get_db() as session:
            result = session.run(
                """
                MATCH (v:Variable)
                WHERE v.name = $variable_id
                DELETE v
                RETURN count(v) as deleted
                """,
                variable_id=variable_id
            )
            return result.single()["deleted"] > 0 