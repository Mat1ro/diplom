from aiogram.fsm.state import StatesGroup, State

class QuizStates(StatesGroup):
    waiting_for_topic = State()
    waiting_for_difficulty_from = State()
    waiting_for_difficulty_to = State()