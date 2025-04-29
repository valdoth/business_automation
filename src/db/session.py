from contextlib import contextmanager
from neo4j import GraphDatabase
from src.core.config import settings

@contextmanager
def get_db():
    driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )
    try:
        with driver.session() as session:
            yield session
    finally:
        driver.close() 