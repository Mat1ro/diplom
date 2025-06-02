from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from app.crud.problem_crud import ProblemCRUD
from app.database import AsyncSessionLocal
from bot.bot import dp
from bot.keyboards import get_topics_keyboard, get_difficulties_keyboard, get_difficulties_to_keyboard
from bot.states import QuizStates


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    text = "👋 Выбери тему:"
    keyboard = get_topics_keyboard(page=0)
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(QuizStates.waiting_for_topic)


@dp.callback_query(lambda c: c.data and c.data.startswith("page:"))
async def process_page_callback(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(":", 1)[1])
    keyboard = get_topics_keyboard(page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data and c.data.startswith("topic:"))
async def topic_chosen(callback: types.CallbackQuery, state: FSMContext):
    topic = callback.data.split(":", 1)[1]
    await state.update_data(chosen_topic=topic)
    await callback.message.edit_text(
        f"Выбрана тема: {topic}\nТеперь выбери минимальную сложность:",
        reply_markup=get_difficulties_keyboard()
    )
    await state.set_state(QuizStates.waiting_for_difficulty_from)
    await callback.answer()


@dp.callback_query(lambda c: c.data and c.data.startswith("difficulty:"))
async def difficulty_from_chosen(callback: types.CallbackQuery, state: FSMContext):
    difficulty_str = callback.data.split(":", 1)[1]
    try:
        difficulty_from = float(difficulty_str)
    except ValueError:
        await callback.answer("Некорректное значение сложности", show_alert=True)
        return

    # Сохраняем значение сложности "от"
    await state.update_data(difficulty_from=difficulty_from)
    await callback.message.edit_text(
        "Теперь выбери максимальную сложность (до):",
        reply_markup=get_difficulties_to_keyboard(difficulty_from)
    )
    await state.set_state(QuizStates.waiting_for_difficulty_to)
    await callback.answer()


@dp.callback_query(lambda c: c.data and c.data.startswith("difficulty_to:"))
async def difficulty_to_chosen(callback: types.CallbackQuery, state: FSMContext):
    difficulty_to_str = callback.data.split(":", 1)[1]
    try:
        difficulty_to = float(difficulty_to_str)
    except ValueError:
        await callback.answer("Некорректное значение сложности", show_alert=True)
        return

    data = await state.get_data()
    topic = data.get("chosen_topic")
    difficulty_from = data.get("difficulty_from")

    if not topic or not difficulty_from:
        await callback.answer("Пожалуйста, сначала выбери тему и минимальную сложность.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        crud = ProblemCRUD(session)
        problems = await crud.get_random_by_tag_and_points_range(
            topic,
            difficulty_from,
            difficulty_to,
            limit=10
        )

    if not problems:
        await callback.message.edit_text("По вашему запросу задач не найдено.")
    else:
        text = "Вот задачи для тебя:\n\n" + "\n\n".join(
            f"{i + 1}. 🔗 [Задача {p.contest_id}{p.index}](https://codeforces.com/problemset/problem/{p.contest_id}/{p.index}) — *{p.name}*"
            for i, p in enumerate(problems)
        )
        await callback.message.edit_text(text)

    await state.clear()
    await callback.answer()
