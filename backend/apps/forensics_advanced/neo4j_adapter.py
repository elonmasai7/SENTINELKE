from neo4j import GraphDatabase
from django.conf import settings


def get_driver():
    return GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))


def upsert_wallet_transfer(tx_hash: str, wallet_from: str, wallet_to: str):
    query = """
    MERGE (a:Wallet {address: $wallet_from})
    MERGE (b:Wallet {address: $wallet_to})
    MERGE (a)-[:TRANSFER {tx_hash: $tx_hash}]->(b)
    """
    with get_driver().session() as session:
        session.run(query, tx_hash=tx_hash, wallet_from=wallet_from, wallet_to=wallet_to)
