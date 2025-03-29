__all__ = ["compute_repeat_interval_duration", "compute_card_new_progress"]


BASE_MARK_EFFECT = 2.8
PROGRESS_CHANGE_FACTOR = 0.22
MIN_INTERVAL_MINUTES_DURATION = 5
MAX_INTERVAL_MINUTES_DURATION = 259_200
INTERVAL_EXP_CHANGE_FACTOR = 5


def compute_card_new_progress(prev_progress: float, mark: int) -> float:
    new_progress: float = (prev_progress + PROGRESS_CHANGE_FACTOR * (mark - BASE_MARK_EFFECT)
                    * (1 - prev_progress))
    if new_progress < 0.0:
        return 0.0
    elif new_progress > 1.0:
        return 1.0
    return new_progress


def compute_repeat_interval_duration(curr_progress: float) -> int:
    return int((curr_progress ** INTERVAL_EXP_CHANGE_FACTOR)
                * (MAX_INTERVAL_MINUTES_DURATION - MIN_INTERVAL_MINUTES_DURATION)
                + MIN_INTERVAL_MINUTES_DURATION)
