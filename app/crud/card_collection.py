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

# нет проверки на то, все ли карточки существуют
def check_connections(conn: Connection, collection_id: int, cards: list[int]) -> list[int]:
    unique_cards = list(set(cards))
    query = select(CardCollectionTable.c.card_id).where(
        CardCollectionTable.c.collection_id == collection_id,
        CardCollectionTable.c.card_id.in_(unique_cards)
    )
    return [x for x in cards if x not in conn.execute(query).all()]

# можно переписать через подзапрос (Deep Alchemy)
def create_card_collection(conn: Connection, collection_id: int, cards: list[int]):
    sifted_cards = check_connections(conn, collection_id, cards)
    conn.execute(
        insert(CardCollectionTable),
        [
            {"collection_id": collection_id, "card_id": card_id}
            for card_id in sifted_cards
        ],
    )
    conn.commit()
