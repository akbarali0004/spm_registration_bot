from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


admin_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить вакансию", callback_data="add_job")],
        [InlineKeyboardButton(text="📋 Список вакансий", callback_data="list_jobs")]
    ])


# Rozilik berish
check_btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я согласен", callback_data="checked")]
    ])


# Erkak/Ayol
gender_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍🦱 Мужской", callback_data="man"),
            InlineKeyboardButton(text="👩‍🦰 Женский", callback_data="woman")
        ]
    ]
)


ask_experience_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="yes"),
            InlineKeyboardButton(text="Нет", callback_data="no")
        ]
    ]
)


# Til bilishi
lang_ask_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="yes")
        ],
        [
            InlineKeyboardButton(text="Нет", callback_data="no")
        ],
        [
            InlineKeyboardButton(text="Базовый уровень", callback_data="base_level")
        ]
    ]
)


# Oilaviy xolati
family_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Не женат / не замужем", callback_data="family_single")
        ],
        [
            InlineKeyboardButton(text="Женат / замужем", callback_data="nofamily_married")
        ],
        [
            InlineKeyboardButton(text="Разведён / разведена", callback_data="family_divorced")
        ]
    ]
)


# Phone
phone_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='📞 Отправить контакт', request_contact=True)
    ]
], resize_keyboard=True)


markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да ✅", callback_data="currently_yes")],
        [InlineKeyboardButton(text="Нет ❌", callback_data="currently_no")]
    ])