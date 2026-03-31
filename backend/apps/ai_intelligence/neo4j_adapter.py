from neo4j import GraphDatabase
from django.conf import settings


def get_driver():
    return GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))


def upsert_subject_score(subject_ref: str, score: int):
    query = """
    MERGE (s:Subject {ref: $subject_ref})
    SET s.latest_score = $score, s.updated_at = datetime()
    """
    with get_driver().session() as session:
        session.run(query, subject_ref=subject_ref, score=score)
