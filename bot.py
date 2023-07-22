import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from cred import TOKEN
from Filters import ChatTypeFilter


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
print("bot started")


async def check(message: CallbackQuery, chatId: str = None):
    try:
        status = await bot.get_chat_member(chatId, message.from_user.id)
        return False if status.status == "left" else True
    except:
        return False


async def giftMessage(message: Message):
    await asyncio.sleep(3)
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Я подписался. Хочу сессию!", callback_data="subscribe"))
    giftText = f'''{message.from_user.first_name}, если Вы не просто скачали подарок, но и подписались на мой канал, то для подписчиков у меня есть подарок - я дам обратную связь Вам, как руководителю, в рамках Диагностической сессии по итогам Опросника

Пройти Опросник здесь <a href='https://abc.com'>(тут ссылка)</a>

Подписывайтесь на мой канал, если еще этого не сделали, и забирайте бесплатно <b>Диагностическую сессию</b>! ⬇️⬇️⬇️ '''

    await message.answer(text=giftText, reply_markup=kb.as_markup(), parse_mode="HTML")


@dp.message(Command("start"))
async def start(message: Message):
    userName = message.from_user.first_name
    startText = f"""Ваш подарок для лидеров команд здесь 

{userName}, добрый день! Я Ольга Седакова
Я помогаю руководителям настроить эффективную работу в командах и почувствовать себя лидерами

Возьмите Ваш подарок здесь - https://t.me/sedakovacoach (он в закрепленном сообщении в канале)

Познакомимся поближе?

Я в коучинге с 2019г., имею статус коуча PCC ICF

Провела более 800 часов коуч-сессий с руководителями проектных офисов, ИТ подразделений, директорами региональных отделений и VIP офисов банка

Как агент изменений выступаю в ролях:
• Executive-коуч
• Командный коуч
• Agile Coach

Как Executive-коуч работаю в корпоративном формате и в частной практике. Среди клиентов в коучинге компания JTI, руководители ВТБ, Газпромбанк 

В Executive-коучинге использую как коучинговые инструменты, так и инструменты НЛП, когнитивно-поведенческую терапию. Выбор инструментария согласовываю с клиентом.
При необходимости могу дополнить консультацией по проектному менеджменту, Scrum framework, масштабируемому Agile и групповым динамикам в команде

Обо мне также можно почитать на сайте www.olgasedakova.ru
А сейчас забирайте Ваш подарок – нажмите кнопку """

    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(url="https://t.me/sedakovacoach", text="Поучить подарок", callback_data="subscribe"))

    await message.answer_photo(photo=FSInputFile("Photo/start.png"), caption=startText[:1024], reply_markup=kb.as_markup())
    await asyncio.create_task(giftMessage(message))


# -------------------Message Check---------------------------------#
@dp.callback_query()
async def checkMessage(callback: CallbackQuery):
    if not await check(callback, "@ugabuga3301"):
        await callback.answer(show_alert=True, text="Вы ещё не подписались на канал!")
    else:
        text = f"{callback.from_user.first_name}, чтобы забронировать <b>диагностическую сессию</b>, \n" \
               f"выберите удобное для Вас время в календаре ⬇️⬇️⬇️\n" \
               f"<a href='https://abc.com'>(тут ссылка)</a> \n \n" \
               f"Если у Вас появились вопросы, со мной можно продолжить общение в чате WhatsApp"
        kb = InlineKeyboardBuilder().add(InlineKeyboardButton(url="https://wa.me/+79774916345", text="Перейти в WhatsApp"))
        await callback.message.answer(text=text, reply_markup=kb.as_markup(),
                                      parse_mode="HTML", disable_web_page_preview=False)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
