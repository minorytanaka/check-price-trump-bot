from environs import Env


env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
API_TOKEN = env.str("API_TOKEN")
