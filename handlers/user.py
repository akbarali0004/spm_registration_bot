import asyncio
import os
import re

from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from state import Form
from keyboards import *
from config import GROUP_ID, CHANNEL_ID
from create_file import write_template

router = Router()
date_regex = r"^(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[0-2])\.(19|20)\d\d$"


# Start komandasi
@router.message(F.text, F.text == "/start", StateFilter(None))
async def start(message: Message, state: FSMContext):
    await message.answer("<b>Здравствуйте!</b>\n\nМы рады приветствовать вас в нашем боте. Прежде чем продолжить, пожалуйста, ознакомьтесь с нашими условиями:\n\n<a href='https://telegra.ph/Polzovatelskoe-soglashenie-12-04-33'>Ссылка на условия</a>\n\nНажмите кнопку <b>«Я согласен»</b>, чтобы начать регистрацию.", reply_markup=check_btn)


@router.callback_query(F.data == "checked")
async def start(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<b>1. Фамилия, имя ✍️</b>\n\nПожалуйста, введите вашу фамилию и имя:\n<i>(Например: Иванов Сергей)</i>")
    await state.set_state(Form.full_name)


# 1 — ism familiya
@router.message(F.text, Form.full_name)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("<b>2. Полная дата рождения 🎂</b>\n\nВведите вашу дату рождения в формате <i>ДД.ММ.ГГГГ</i>:\n<i>(Например: 25.12.2001)</i>")
    await state.set_state(Form.birth_year)


# 2 — tug'ilgan yil
@router.message(F.text.regexp(date_regex), Form.birth_year)
async def birth_year(message: Message, state: FSMContext):
    await state.update_data(birth_year=message.text)
    await message.answer("<b>3. Пол 🚻</b>\n\nВыберите ваш пол:", reply_markup=gender_btn)
    await state.set_state(Form.gender)


@router.message(F.text, Form.birth_year)
async def birth_year(message: Message, state: FSMContext):
    await message.answer("<b>❌ Ошибка!</b>\n\nПожалуйста, введите дату вашего рождения в правильном формате.\n<i>Пример: 25.12.2001</i>")


# 3 — jins
@router.callback_query(Form.gender)
async def gender(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)

    if call.data=="man":
        await state.update_data(gender="Мужской")
    elif call.data=="woman":
        await state.update_data(gender="Женский")

    await call.message.answer("<b>4.1. Учебное заведение 🏫</b>\n\nУкажите, в каком учебном заведении вы учились или учитесь сейчас.")
    await state.set_state(Form.education)


# 4.1 — ta'lim muassasasi
@router.message(F.text, Form.education)
async def education(message: Message, state: FSMContext):
    await state.update_data(education=message.text)
    await message.answer("<b>4.2. Дата начала обучения 📅</b>\n\nВведите дату начала обучения в формате <b>ДД.ММ.ГГГГ</b>\n\n<i>(Например, 31.12.2020)</i>")
    await state.set_state(Form.edu_start)


# 4.2
@router.message(F.text, Form.edu_start)
async def edu_start(message: Message, state: FSMContext):
    if re.match(date_regex, message.text):
        await state.update_data(edu_start=message.text)
        await message.answer("<b>4.3. Дата окончания обучения 📆</b>\n\nВведите дату начала обучения в формате <b>ДД.ММ.ГГГГ.</b>\n\n<i>(Например, 31.12.2020)</i>")
        await state.set_state(Form.edu_end)
    else:
        await message.answer(
            "❌ Неверный формат даты!\n"
            "Пожалуйста, введите дату в формате <b>ДД.ММ.ГГГГ</b> .\n\n(Например: 31.12.2020)"
        )


# 4.3
@router.message(F.text, Form.edu_end)
async def edu_end(message: Message, state: FSMContext):
    if re.match(date_regex, message.text):
        await state.update_data(edu_end=message.text)
        await message.answer("<b>4.4. Формат обучения:</b>\n\n⬇️ Выберите подходящий вариант ⬇️", reply_markup=study_format_btn)
        await state.set_state(Form.study_format)
    else:
        await message.answer(
            "❌ Неверный формат даты!\n"
            "Пожалуйста, введите дату в формате <b>ДД.ММ.ГГГГ</b> .\n\n(Например: 31.12.2020)"
        )


# 4.4
@router.callback_query(Form.study_format)
async def study_format(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    study_format=''
    if call.data == "study_format_fulltime":
        study_format = "Очный"
    if call.data == "study_format_parttime":
        study_format = "Заочный"
    if call.data == "study_format_online":
        study_format = "Онлайн"

    await state.update_data(study_format = study_format)
    await call.message.answer("<b>5. Опыт работы 💼</b>\n\nИмеется ли у вас опыт работы?", reply_markup=ask_experience_btn)
    await state.set_state(Form.has_experience)


# 5 — bor/yo'q
@router.callback_query(Form.has_experience)
async def has_experience(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data == "yes":
        await state.update_data(has_experience="Да")
        await call.message.answer("<b>6.1. Должность 🧑‍💼</b>\n\nНа какой должности вы работали?")
        await state.set_state(Form.position)
    else:
        # Agar tajriba bo'lmasa keyingi bosqichga o'tadi
        await state.update_data(has_experience="Нет")
        await state.update_data(position="-", company="-", work_period="-")
        await ask_languages(call, state)


# 6.1 — lavozim
@router.message(F.text, Form.position)
async def position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer("<b>6.2. Организация / компания 🏢</b>\n\nНазвание организации или компании:")
    await state.set_state(Form.company)


# 6.2
@router.message(F.text, Form.company)
async def company(message: Message, state: FSMContext):
    await state.update_data(company=message.text)
    await message.answer("<b>6.3. Период работы ⏳</b>\n\nУкажите период работы.")
    await state.set_state(Form.work_period)

# 6.3
@router.message(F.text, Form.work_period)
async def currently_working(message:Message, state:FSMContext):
    await state.update_data(work_period=message.text)
    await message.answer("<b>6.4. В настоящее время вы работаете? 🕒</b>\n\nВы сейчас работаете на этой должности?",reply_markup=markup)
    await state.set_state(Form.currently_working)


# 6.4
@router.callback_query(Form.currently_working)
async def work_period(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data=="currently_yes":
        await state.update_data(currently_working="Да")
    elif call.data=="currently_no":
        await state.update_data(currently_working="Нет")

    await call.message.answer("<b>7. Владение узбекским языком 🇺🇿</b>\n\nВыберите один вариант:", reply_markup=lang_ask_btn)
    await state.set_state(Form.uzbek)


# Tillarni sorash
async def ask_languages(call: CallbackQuery, state: FSMContext):
    await call.message.answer("<b>7. Владение узбекским языком 🇺🇿</b>\n\nВыберите один вариант:", reply_markup=lang_ask_btn)
    await state.set_state(Form.uzbek)


# 7
@router.callback_query(Form.uzbek)
async def uzbek(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data=="yes":
        await state.update_data(uzbek="Да")
    else:
        await state.update_data(uzbek="Нет")
    await call.message.answer("<b>8. Владение русским языком 🇷🇺</b>\n\nВыберите один вариант:", reply_markup=lang_ask_btn)
    await state.set_state(Form.russian)


# 8
@router.callback_query(Form.russian)
async def uzbek(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data=="yes":
        await state.update_data(russian="Да")
    else:
        await state.update_data(russian="Нет")
    await call.message.answer("<b>9. Другие языки 🌍</b>\n\nКакими другими языками вы владеете?")
    await state.set_state(Form.other_langs)


# 9
@router.message(F.text, Form.other_langs)
async def other_langs(message: Message, state: FSMContext):
    await state.update_data(other_langs=message.text)
    await message.answer("<b>10. Семейное положение ❤️</b>\n\nВыберите вариант:", reply_markup=family_btn)
    await state.set_state(Form.family)


# 10
@router.callback_query(Form.family)
async def family(call: CallbackQuery, state: FSMContext, bot:Bot):
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data=="family_single":
        await state.update_data(family="Не женат / не замужем")
    elif call.data=="nofamily_married":
        await state.update_data(family="Женат / замужем")
    elif call.data=="family_divorced":
        await state.update_data(family="Разведён / разведена")

    await call.message.answer("<b>11. Голосовая информация 🎤</b>\n\nПожалуйста, отправьте краткое голосовое сообщение о себе.")
    await bot.copy_messages(chat_id=call.from_user.id, from_chat_id=CHANNEL_ID, message_ids=[3, 4])
    await state.set_state(Form.audio)


# 11 — audio
@router.message(F.voice, Form.audio)
async def audio(message: Message, state: FSMContext):
    await state.update_data(voice=message.voice.file_id)
    await message.answer("<b>12. Фото 📸</b>\n\nОтправьте ваше фото.")
    await state.set_state(Form.photo)


# 12 — photo
@router.message(F.photo, Form.photo)
async def photo(message: Message, state: FSMContext, bot:Bot):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer("<b>13. Видеосообщение 🎥</b>\n\nОтправьте короткое видеосообщение.")
    await bot.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL_ID, message_id=2)
    await state.set_state(Form.video)


# 13 — video
@router.message(F.video_note, Form.video)
async def video(message: Message, state: FSMContext):
    await state.update_data(video_note=message.video_note.file_id)
    await message.answer("<b>14. Контактный номер телефона 📞</b>\n\nПожалуйста, введите ваш номер телефона вручную или воспользуйтесь кнопкой отправки контакта ниже.\n\n<i>Например: 998901234567</i>", reply_markup=phone_btn)
    await state.set_state(Form.phone)


# 14 — phone
@router.message(F.text.regexp(r'^998\d{9}$'), Form.phone)
async def phone(message: Message, state: FSMContext, bot:Bot):
    await state.update_data(phone=f"+{message.text}")
    await send_result(message, state, bot)


@router.message(F.contact, Form.phone)
async def phone(message: Message, state: FSMContext, bot:Bot):
    await state.update_data(phone=f"+{message.contact.phone_number}")
    await send_result(message, state, bot)


async def send_result(message, state, bot):
    if message.from_user.username:
        await state.update_data(telegram=f"@{message.from_user.username}")
    else:
        await state.update_data(telegram='-')


    data = await state.get_data()

    # Yakuniy natija
    text = (
        f"📝 <b>Anketa natijalari:</b>\n\n"
        f"👤 Familiya, ism: {data['full_name']}\n"
        f"🎂 Tug‘ilgan yil: {data['birth_year']}\n"
        f"🚻 Jinsi: {data['gender']}\n"
        f"🎓 Ta’lim: {data['education']}\n"
        f"   📅 Boshlangan: {data['edu_start']}\n"
        f"   📆 Tugagan: {data['edu_end']}\n"
        f"   🏢 Ta'lim shakli: {data['study_format']}\n"
        f"💼 Ish tajribasi: {data['has_experience']}\n"
        f"   🏷️ Lavozim: {data['position']}\n"
        f"   🏢 Tashkilot: {data['company']}\n"
        f"   ⏳ Muddat: {data.get('work_period', '-')}\n"
        f"   🟢 Hozirda ishlayaptimi: {data.get('currently_working', '-')}\n"
        f"🇺🇿 O‘zbek tili: {data['uzbek']}\n"
        f"🇷🇺 Rus tili: {data['russian']}\n"
        f"🌐 Boshqa tillar: {data['other_langs']}\n"
        f"👨‍👩‍👧 Oilaviy holat: {data['family']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"💬 Telegram: {data['telegram']}"
    )

    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    write_template(data=data)
    await asyncio.sleep(2)

    file_path = f"template/{data['full_name']}.docx"

    await bot.send_document(chat_id=GROUP_ID, document=FSInputFile(file_path), caption=text)
    if os.path.exists(file_path):
        os.remove(file_path)

    if data['photo']:
        await bot.send_photo(chat_id=GROUP_ID, photo=data['photo'])
    if data['voice']:
        await bot.send_voice(chat_id=GROUP_ID, voice=data['voice'])
    if data['video_note']:
        await bot.send_video_note(GROUP_ID, video_note=data['video_note'])
    await state.clear()


@router.message()
async def error_message_type(message:Message, state:FSMContext):
    current_state = await state.get_state()
    if current_state==Form.audio:
        return await message.answer("❗ Пожалуйста, отправьте <b>голосовое сообщение</b> (voice).")
    if current_state==Form.photo:
        return await message.answer("❗ Пожалуйста, отправьте <b>фотографию</b>.")
    if current_state==Form.video:
        return await message.answer("❗ Пожалуйста, отправьте <b>круглое видео</b> (video note).")