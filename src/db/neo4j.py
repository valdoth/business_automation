from neo4j import GraphDatabase
from typing import Optional, List, Dict, Any
from ..core.config import settings

class Neo4jDatabase:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def create_document(self, document: Dict[str, Any]) -> str:
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_document_tx,
                document
            )
            return result

    def create_variable(self, variable: Dict[str, Any]) -> str:
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_variable_tx,
                variable
            )
            return result

    def create_scenario(self, scenario: Dict[str, Any]) -> str:
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_scenario_tx,
                scenario
            )
            return result

    def get_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.read_transaction(
                self._get_scenario_tx,
                scenario_id
            )
            return result

    def get_all_documents(self) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_documents_tx)
            return result

    def get_all_variables(self) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_variables_tx)
            return result

    def get_all_scenarios(self) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_scenarios_tx)
            return result

    @staticmethod
    def _create_document_tx(tx, document: Dict[str, Any]) -> str:
        query = """
        CREATE (d:Document {
            id: $id,
            type: $type,
            minio_key: $minio_key,
            metadata: $metadata,
            created_at: $created_at,
            updated_at: $updated_at
        })
        RETURN d.id
        """
        result = tx.run(query, **document)
        return result.single()[0]

    @staticmethod
    def _create_variable_tx(tx, variable: Dict[str, Any]) -> str:
        query = """
        MATCH (d:Document {id: $document_id})
        CREATE (v:Variable {
            id: $id,
            name: $name,
            value: $value,
            created_at: $created_at,
            updated_at: $updated_at
        })
        CREATE (v)-[:BELONGS_TO]->(d)
        RETURN v.id
        """
        result = tx.run(query, **variable)
        return result.single()[0]

    @staticmethod
    def _create_scenario_tx(tx, scenario: Dict[str, Any]) -> str:
        query = """
        CREATE (s:Scenario {
            id: $id,
            name: $name,
            description: $description,
            steps: $steps,
            created_at: $created_at,
            updated_at: $updated_at
        })
        WITH s
        UNWIND $document_ids as doc_id
        MATCH (d:Document {id: doc_id})
        CREATE (s)-[:USES]->(d)
        WITH s
        UNWIND $variable_ids as var_id
        MATCH (v:Variable {id: var_id})
        CREATE (s)-[:USES]->(v)
        RETURN s.id
        """
        result = tx.run(query, **scenario)
        return result.single()[0]

    @staticmethod
    def _get_scenario_tx(tx, scenario_id: str) -> Optional[Dict[str, Any]]:
        query = """
        MATCH (s:Scenario {id: $scenario_id})
        OPTIONAL MATCH (s)-[:USES]->(d:Document)
        OPTIONAL MATCH (s)-[:USES]->(v:Variable)
        RETURN s, collect(distinct d) as documents, collect(distinct v) as variables
        """
        result = tx.run(query, scenario_id=scenario_id)
        record = result.single()
        if record:
            return {
                "scenario": dict(record["s"]),
                "documents": [dict(doc) for doc in record["documents"]],
                "variables": [dict(var) for var in record["variables"]]
            }
        return None

    @staticmethod
    def _get_all_documents_tx(tx) -> List[Dict[str, Any]]:
        query = """
        MATCH (d:Document)
        RETURN d
        """
        result = tx.run(query)
        return [dict(record["d"]) for record in result]

    @staticmethod
    def _get_all_variables_tx(tx) -> List[Dict[str, Any]]:
        query = """
        MATCH (v:Variable)-[:BELONGS_TO]->(d:Document)
        RETURN v, d.id as document_id
        """
        result = tx.run(query)
        return [dict(record["v"]) for record in result]

    @staticmethod
    def _get_all_scenarios_tx(tx) -> List[Dict[str, Any]]:
        query = """
        MATCH (s:Scenario)
        OPTIONAL MATCH (s)-[:USES]->(d:Document)
        OPTIONAL MATCH (s)-[:USES]->(v:Variable)
        RETURN s, collect(distinct d) as documents, collect(distinct v) as variables
        """
        result = tx.run(query)
        return [{
            "scenario": dict(record["s"]),
            "documents": [dict(doc) for doc in record["documents"]],
            "variables": [dict(var) for var in record["variables"]]
        } for record in result]

# Create a global database instance
db = Neo4jDatabase() 