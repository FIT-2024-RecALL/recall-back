from .cards import router as cards_router
from .collections import router as collections_router
from .storage import router as storage_router
from .train_records import router as training_router
from .users import router as users_router


all_routers = [cards_router, collections_router, storage_router, training_router, users_router]
