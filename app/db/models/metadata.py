from sqlalchemy import MetaData


__all__ = ["get_metadata"]


__metadata = MetaData()


def get_metadata():
    return __metadata
