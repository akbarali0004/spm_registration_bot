from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN = env.int("ADMIN")
GROUP_ID = env.int("GROUP_ID")
CHANNEL_ID = env.int("CHANNEL_ID")