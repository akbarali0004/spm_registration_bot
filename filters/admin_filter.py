from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import ADMIN


class IsDigitMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text is not None and message.text.isdigit()
    

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ADMIN