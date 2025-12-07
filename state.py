from aiogram.fsm.state import State, StatesGroup



class AddJobState(StatesGroup):
    wait_job_title = State()
    wait_job_description = State()
    wait_job_question = State()


class Form(StatesGroup):
    full_name = State()
    birth_year = State()
    gender = State()
    education = State()
    edu_start = State()
    edu_end = State()
    has_experience = State()
    position = State()
    company = State()
    work_period = State()
    currently_working = State()
    uzbek = State()
    russian = State()
    other_langs = State()
    family = State()
    audio = State()
    photo = State()
    video = State()
    phone = State()
    telegram = State()