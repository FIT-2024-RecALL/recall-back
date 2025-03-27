from fastapi import HTTPException

from app.core import compute_card_new_progress, compute_repeat_interval_duration, compare_answers
from app.repositories import CardRepository, TrainRecordRepository, UserRepository
from app.schemas import AIFeedback, Card, TrainRecord, TrainRecordCreate, UserAnswer

from .base import BaseService


__all__ = ["TrainRecordService"]


class TrainRecordService(BaseService):
    async def create_train_record(
            self, user_id: int, card_id: int, training: TrainRecordCreate
    ) -> TrainRecord:
        async with self.uow.begin():
            if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            if not await self.uow.get_repository(CardRepository).exists_card_with_id(card_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            train_record_repo = self.uow.get_repository(TrainRecordRepository)
            last_training = await (train_record_repo
                                   .get_user_card_last_train_record(user_id, card_id, TrainRecord))
            prev_progress = 0.0 if last_training is None else last_training.progress
            progress = compute_card_new_progress(prev_progress, training.mark)
            interval = compute_repeat_interval_duration(progress)
            train_data = training.model_dump()
            train_data.update(card_id=card_id, user_id=user_id, progress=progress)
            return await train_record_repo.create_train_record(train_data, interval, TrainRecord)

    async def get_user_card_last_train_record(
            self, user_id: int, card_id: int
    ) -> TrainRecord | None:
        async with self.uow.begin():
            if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            if not await self.uow.get_repository(CardRepository).exists_card_with_id(card_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            train_record_repo = self.uow.get_repository(TrainRecordRepository)
            return await train_record_repo.get_user_card_last_train_record(user_id, card_id, TrainRecord)

    async def compare_answers_by_ai(
            self, user_id, card_id, user_answer: UserAnswer
    ) -> AIFeedback:
        async with self.uow.begin():
            if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            card_repo = self.uow.get_repository(CardRepository)
            if not await card_repo.exists_card_with_id(card_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            if (card := await card_repo.get_card_by_id(card_id, Card)) is None:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await compare_answers(card.front_side, card.back_side, user_answer.answer)
