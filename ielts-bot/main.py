import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai

# === KONFIGURATSIYA ===
BOT_TOKEN = "8515663139:AAFP2W2ArtUpIVOjExgTBHnNriLDbXlfGbg"
GEMINI_API_KEY = "AQ.Ab8RN6LRugJFgI8DxLyIGM7AEyLh89iQ09n7s5cOp8NgtjIICw"

# Loggingni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher ob'ektlarini yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Gemini AI yangi async mijozini yaratish
client = genai.Client(api_key=GEMINI_API_KEY, http_options={'api_version': 'v1'})

# /start komandasi uchun xabar
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Welcome to IELTS Hub Bot!\n\n"
        "✍️ Writing Essay (Task 1 or Task 2) matnini shu yerga yuboring. "
        "Men uni IELTS kriteriyalari bo'yicha tahlil qilib, xatolaringizni tuzatib, "
        "taxminiy Band Score (ball) chiqarib beraman!"
    )

# Essey matnini qabul qilib, Gemini orqali tekshirish
@dp.message()
async def check_essay(message: types.Message):
    # Foydalanuvchiga kuttirmaslik uchun "yozilmoqda..." statusini ko'rsatish
    await message.answer("⏳ Essey tahlil qilinmoqda, biroz kuting...")
    
    user_essay = message.text
    
    prompt = f"""
    You are an expert IELTS Writing Examiner. Analyze the following user essay carefully.
    Provide a detailed feedback in Uzbek language, but keep grammatical corrections and IELTS terms in English.

    Structure your response as follow:
    1. Overall Band Score (Estimated)
    2. Detailed criteria breakdown (Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy)
    3. Strong points of the essay.
    4. Mistakes found and their corrections (with explanations).
    5. A fully improved model version of this essay.

    User Essay:
    {user_essay}
    """
    
    try:
        # Model nomini to'liq va aniq ko'rsatamiz
        response = await client.aio.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        await message.answer(response.text)
        
    except Exception as e:
        # Xatolikni terminalda ko'rish uchun tafsilotli log
        logging.error(f"Xatolik tafsiloti: {e}")
        await message.answer("❌ Kechirasiz, essey tahlil qilishda xatolik yuz berdi.")

# Botni yurgizish (Polling)
async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())