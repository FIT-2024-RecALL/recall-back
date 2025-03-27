from fastapi import APIRouter

from app.schemas import AIFeedback, TrainRecord, TrainRecordCreate, UserAnswer

from .dependencies import TrainRecordServiceDep, UserIdDep


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.get("/last/{card_id}", response_model=TrainRecord|None)
async def read_card_last_train_record(
        user_id: UserIdDep, card_id: int, train_record_service: TrainRecordServiceDep
) -> TrainRecord | None:
    return await train_record_service.get_user_card_last_train_record(user_id, card_id)


@router.post("/{card_id}", response_model=TrainRecord)
async def create_train_record(
        user_id: UserIdDep, card_id: int, train_record: TrainRecordCreate,
        train_record_service: TrainRecordServiceDep
):
    return await train_record_service.create_train_record(user_id, card_id, train_record)


@router.post("/{card_id}/compare", response_model=AIFeedback)
async def compare_answers_by_ai(
        user_id: UserIdDep, card_id: int, user_answer: UserAnswer,
        train_record_service: TrainRecordServiceDep
):
    await train_record_service.compare_answers_by_ai(user_id, card_id, user_answer)
