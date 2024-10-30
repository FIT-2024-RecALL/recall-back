from sqlalchemy import Connection, select, insert, exists, or_

from app import models, schemas


def get_collection(conn: Connection, collection_id: int):
    query = select(models.CollectionTable.c[*schemas.collection.Collection.model_fields]).where(
        models.CollectionTable.c.id == collection_id
    )
    return conn.execute(query).mappings().first()
