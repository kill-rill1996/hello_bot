import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from settings import settings


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    """
    This handler receives messages with `/start` command
    """
    tg_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

    # send message for admins
    msg_for_admins = f"id: {tg_id}\n{'username: @' + username if username else ''} ({first_name} {last_name})"
    for tg_admin in settings.admins:
        try:
            await bot.send_message(tg_admin, msg_for_admins)
        except:
            pass


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())