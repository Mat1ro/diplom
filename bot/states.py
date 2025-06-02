"""
Модуль определения состояний FSM (Finite State Machine) для бота.

Этот модуль содержит класс состояний, используемых для управления диалогом с пользователем.
"""

from aiogram.fsm.state import StatesGroup, State


class QuizStates(StatesGroup):
    """
    Класс состояний для управления процессом выбора задач.
    
    Состояния:
        waiting_for_topic: Ожидание выбора темы
        waiting_for_difficulty_from: Ожидание выбора минимальной сложности
        waiting_for_difficulty_to: Ожидание выбора максимальной сложности
    """
    waiting_for_topic = State()
    waiting_for_difficulty_from = State()
    waiting_for_difficulty_to = State()