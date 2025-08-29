from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    bot_token: str = Field(..., env='BOT_TOKEN')
    admins: list = Field(..., env='ADMINS')


settings = Settings()
