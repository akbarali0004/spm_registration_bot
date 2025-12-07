from .admin import router as admin_rt
from .user import router as user_rt

from aiogram import Router

router = Router()
router.include_routers(admin_rt, user_rt)