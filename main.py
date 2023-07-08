import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, ChatPermissions
from aiogram.utils.keyboard import InlineKeyboardBuilder
from cred import TOKEN
from Filters import ChatTypeFilter
from Database import DataBase

# ------------------------------------------#

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
print("bot started")


async def check(message: Message, chatId: str = None):
    db = DataBase()
    links = []
    channelsId = db.getId(str(chatId))
    for id in channelsId:
        status = await bot.get_chat_member(id, message.from_user.id)
        if status.status.split('.')[-1] == 'left':
            links.append(db.getInvLink(str(chatId), id))
    return {*links}


async def adminCheck(message: Message) -> bool:
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ['creator', 'administrator']:
        return True
    else:
        return False


# -------Block-Unblock--------------------------#
@dp.message(Command("block"), ChatTypeFilter(chat_type=["group", "supergroup"]))
async def enableBlock(message: Message):
    if await adminCheck(message):
        db = DataBase()
        channelName = message.text.split()[-1]
        try:
            channelData = await bot.get_chat(channelName)
            print(channelData)
            if channelData.invite_link is not None:
                db.enableBlock(str(message.chat.id), str(channelData.id), str(channelData.invite_link))
                await message.answer(
                    text=f"Пользователи, не подписанные на {channelData.title} больше не смогут отправлять сообщения")
            else:
                await message.answer(
                    text=f"Неверно указано название канала или бот не имеет прав")
        except:
            await message.answer(
                text=f"Неверно указано название канала или бот не имеет прав")


@dp.message(Command("unblock"), ChatTypeFilter(chat_type=["group", "supergroup"]))
async def disableBlock(message: Message):
    if await adminCheck(message):
        db = DataBase()
        db.disableBlock(str(message.chat.id))
        await message.answer(text=f"Теперь любые пользователи могут отправлять сообщения")


# -------------------Message Check---------------------------------#
@dp.message(ChatTypeFilter(chat_type=["group", "supergroup"]))
async def checkMessage(message: Message):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Проверить подписку', callback_data="none"))
    links = await check(message, message.chat.id)
    if links:
        try:
            await bot.restrict_chat_member(message.chat.id, message.from_user.id, {'can_send_messages': False})
        except:
            pass
        await message.delete()
        await message.answer(text=f"{message.from_user.username}, приветствую тебя! \nЧтобы иметь возможность"
                                  f" писать в чат, необходимо подписаться на канал(ы): \n"
                                  f"{' '.join(links)}", reply_markup=kb.as_markup())


@dp.callback_query()
async def ch(callback: CallbackQuery):
    links = await check(callback, callback.message.chat.id)
    if links:
        await callback.answer(show_alert=True, text="Вы ещё не подписались на каналы")
    else:
        try:
            await bot.restrict_chat_member(callback.message.chat.id, callback.from_user.id, {'can_send_messages': True})
        except:
            pass
        await callback.answer(show_alert=True, text="Теперь вы можете писать сообщения!")
        await callback.message.delete()


@dp.message(ChatTypeFilter(chat_type="private"))
async def start(message: Message):
    await message.answer("Для использования бота добавтье его в качестве администратора в необходиую группу и чат \n"
                         "Для включения блокировки отправьте следующую комманду в необохдимый чат: /block @channelName, \n"
                         "где @channelName - юзернейм или id канала \n"
                         "Для снятия блокировок воспользуйтесь коммандой /unblock в соответсвующем чате.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
