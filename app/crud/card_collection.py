from sqlalchemy import Connection, select, insert

from app.models import CardTable, CardCollectionTable, CollectionTable
from app.schemas import card, collection


# наверное можно сделать запрос эффективнее
def get_collection_cards(conn: Connection, collection_id: int):
    query = select(CardTable.c[*card.Card.model_fields]).where(
        CardTable.c.id == CardCollectionTable.c.card_id,
        CardCollectionTable.c.collection_id == collection_id
    )
    return conn.execute(query).mappings().all()


def get_card_collections():
    pass


def check_connections(conn: Connection, collection_id: int, cards: list[int]) -> list[int]:
    unique_cards: list[int] = list(set(cards))
    query = select(CardCollectionTable.c.card_id).where(
        CardCollectionTable.c.collection_id == collection_id,
        CardCollectionTable.c.card_id.in_(unique_cards)
    )
    result_cards: list[int] = [x[0] for x in conn.execute(query).all()]
    return [x for x in unique_cards if x not in result_cards]


def sift_exist_cards(conn: Connection, cards: list[int]):
    unique_cards: list[int] = list(set(cards))
    query = select(CardTable.c.id).where(CardTable.c.id.in_(unique_cards))
    return [x[0] for x in conn.execute(query).all()]

# можно переписать через подзапрос (Deep Alchemy)
def create_card_collection(conn: Connection, collection_id: int, cards: list[int]):
    sifted_cards = sift_exist_cards(conn, check_connections(conn, collection_id, cards))
    if sifted_cards:
        conn.execute(
            insert(CardCollectionTable),
            [
                {"card_id": card_id, "collection_id": collection_id}
                for card_id in sifted_cards
            ],
        )
        conn.commit()



