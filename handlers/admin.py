from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command

from state import AddJobState
from keyboards import admin_menu
from filters import IsAdmin


router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(CommandStart())
async def start_ans(message:Message):
    await message.answer("<b>👋 Здравствуйте, администратор!</b>\n\nПожалуйста, используйте кнопки ниже для работы.", reply_markup=admin_menu)


# Yangi ish nomini so'rash
@router.callback_query(F.data=="add_job")
async def ask_job_title(call: CallbackQuery, state: FSMContext):
    await call.message.answer("<b>Введите название вакансии:</b>")
    await state.set_state(AddJobState.wait_job_title)
    await call.answer()


# Yangi ish tasnifini so'rash
@router.message(F.text, AddJobState.wait_job_title)
async def get_job_title(message:Message, state:FSMContext):
    await state.update_data(title=message.text)
    await message.answer("<b>Введите описание вакансии:</b>")
    await state.set_state(AddJobState.wait_job_description)


# Anketa so'rovini so'rash
@router.message(F.text, AddJobState.wait_job_description)
async def get_job_title(message:Message, state:FSMContext):
    await state.update_data(description=message.text)
    await state.update_data(questions=[])
    await message.answer("<b>📋 Пожалуйста, укажите вопросы анкеты, которые вы хотите задать пользователю ✏️</b>")
    await state.set_state(AddJobState.wait_job_question)


@router.message(Command("done"), AddJobState.wait_job_question)
async def done_job_save(message:Message, state:FSMContext):
    print(await state.get_data())
    await message.answer("Done!")


# Anketa so'rovini olish
@router.message(F.text, AddJobState.wait_job_question)
async def get_job_title(message:Message, state:FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])
    questions.append(message.text)
    await state.update_data(questions=questions)
    await message.answer(f"<b>📌 Вопрос {len(questions)} принят.</b> Теперь вы можете отправить следующий вопрос.\n\n"
                        "<i>↩️ Если нужно удалить последний вопрос — используйте /undo</i>\n"
                        "<i>✅ Когда закончите, отправьте /done для сохранения анкеты</i>")
    
