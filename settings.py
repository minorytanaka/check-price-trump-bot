from environs import Env


env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
SUBSCRIBED_CHAT_ID = env.int("SUBSCRIBED_CHAT_ID")
