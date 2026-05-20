import logging
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# BOT TOKENINGIZNI SHU YERGA YOZING
BOT_TOKEN = "8813368350:AAH09qyyzf629XWTH9rlKdy6X5y9hhAoXLg" 
DAILY_TEST_CODE = "A2"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

active_timers = {}

# --- 🎯 SAVOLLAR RO'YXATI (HAR BIRI ALOHIDA SPISKADA) ---
ALL_QUESTIONS = [
    # 1-savol alohida spiskada
    [
        "Yesterday, I ___ to the cinema and saw a great movie.", 
        "go", "gone", "went", "was go", 
        "went"
    ],
    
    # 2-savol alohida spiskada
    [
        "London is ___ than Manchester.", 
        "big", "more big", "bigger", "biggest", 
        "bigger"
    ],
    
    # 3-savol alohida spiskada
    [
        "We need to buy ___ milk from the supermarket.", 
        "any", "some", "a", "many", 
        "some"
    ],
    
    # 4-savol alohida spiskada
    [
        "He doesn't like coffee, and she doesn't like it ___.", 
        "too", "either", "neither", "also", 
        "either"
    ],
    
    # 5-savol alohida spiskada
    [
        "Have you ___ been to Paris?", 
        "ever", "never", "yet", "already", 
        "ever"
    ],
    
    # 6-savol alohida spiskada
    [
        "If it ___ tomorrow, we won't go to the park.", 
        "rain", "rains", "will rain", "rained", 
        "rains"
    ],
    
    # 7-savol alohida spiskada
    [
        "This is the ___ book I have ever read.", 
        "good", "better", "best", "more good", 
        "best"
    ],
    
    # 8-savol alohida spiskada
    [
        "I ___ my homework when the phone rang.", 
        "was doing", "did", "am doing", "were doing", 
        "was doing"
    ],
    
    # 9-savol alohida spiskada
    [
        "Where ___ you born?", 
        "did", "was", "were", "are", 
        "were"
    ],
    
    # 10-savol alohida spiskada
    [
        "She ___ speak English very well now.", 
        "can", "canned", "cans", "is can", 
        "can"
    ],
    
    # 11-savol alohida spiskada
    [
        "I usually ___ up at 7 o'clock in the morning.", 
        "gets", "get", "getting", "got", 
        "get"
    ],
    
    # 12-savol alohida spiskada
    [
        "Look! The birds ___ in the sky.", 
        "fly", "flies", "is flying", "are flying", 
        "are flying"
    ],
    
    # 13-savol alohida spiskada
    [
        "There ___ any apples left in the fridge.", 
        "isn't", "aren't", "not", "don't", 
        "aren't"
    ],
    
    # 14-savol alohida spiskada
    [
        "How ___ money do you need for the trip?", 
        "many", "much", "few", "long", 
        "much"
    ],
    
    # 15-savol alohida spiskada
    [
        "I think it ___ rain this evening, take an umbrella.", 
        "will", "is going", "does", "shall", 
        "will"
    ],
    
    # 16-savol alohida spiskada
    [
        "This car is ___ expensive than that one.", 
        "more", "most", "much", "very", 
        "more"
    ],
    
    # 17-savol alohida spiskada
    [
        "They have lived in Tashkent ___ five years.", 
        "since", "for", "during", "ago", 
        "for"
    ],
    
    # 18-savol alohida spiskada
    [
        "She is interested ___ learning new languages.", 
        "on", "at", "in", "with", 
        "in"
    ],
    
    # 19-savol alohida spiskada
    [
        "We ___ a great time at the party last weekend.", 
        "have", "had", "has", "having", 
        "had"
    ],
    
    # 20-savol alohida spiskada
    [
        "Whose bag is this? It's ___.", 
        "me", "mine", "my", "myself", 
        "mine"
    ],
    
    # 21-savol alohida spiskada
    [
        "You ___ touch that, it's very hot!", 
        "shouldn't", "must", "don't", "needn't", 
        "shouldn't"
    ],
    
    # 22-savol alohida spiskada
    [
        "He is the ___ runner in our class.", 
        "fast", "faster", "fastest", "most fast", 
        "fastest"
    ],
    
    # 23-savol alohida spiskada
    [
        "Would you like ___ orange juice?", 
        "any", "some", "an", "many", 
        "some"
    ],
    
    # 24-savol alohida spiskada
    [
        "I promise I ___ help you with your project tomorrow.", 
        "will", "going to", "am", "do", 
        "will"
    ],
    
    # 25-savol alohida spiskada
    [
        "They ___ football every Saturday afternoon.", 
        "plays", "playing", "play", "played", 
        "play"
    ]
]

class QuizState(StatesGroup):
    waiting_for_code = State()
    answering = State()

@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if user_id in active_timers:
        active_timers[user_id].cancel()
        del active_timers[user_id]
        
    await message.answer(
        f"Salom {message.from_user.first_name}!\n\n"
        f"Bugungi 25 talik testda qatnashish uchun guruhda berilgan pin-kodni yuboring."
    )
    await state.set_state(QuizState.waiting_for_code)

@dp.message(QuizState.waiting_for_code)
async def check_code(message: types.Message, state: FSMContext):
    user_code = message.text.strip()
    chat_id = message.chat.id
    
    if user_code.upper() == DAILY_TEST_CODE.upper():
        quiz_questions = list(ALL_QUESTIONS)
        random.shuffle(quiz_questions)
        selected_25 = quiz_questions[:25]
        
        await state.update_data(
            questions=selected_25,
            current_question=0,
            correct_answers=0
        )

        await message.answer("✅ Pin-kod to'g'ri!")
        await asyncio.sleep(0.5)
        
        await message.answer("3...")
        await asyncio.sleep(1)
        await message.answer("2...")
        await asyncio.sleep(1)
        await message.answer("1...")
        await asyncio.sleep(1)
        await message.answer("🚀 Test boshlandi! Omad tilaymiz!")
        await asyncio.sleep(0.5)
        
        await send_question(chat_id, state)
    else:
        await message.answer("❌ Noto'g'ri pin-kod. Qaytadan urinib ko'ring.")

async def question_timer(chat_id: int, q_index: int, state: FSMContext, msg_id: int):
    try:
        await asyncio.sleep(60)
        current_data = await state.get_data()
        if current_data.get('current_question') == q_index:
            try:
                await bot.edit_reply_markup(chat_id=chat_id, message_id=msg_id, reply_markup=None)
            except:
                pass
            await bot.send_message(chat_id, f"⏰ Vaqt tugadi! {q_index + 1}-savolga ulgurmadingiz.")
            
            await state.update_data(current_question=q_index + 1)
            await send_question(chat_id, state)
    except asyncio.CancelledError:
        pass

async def send_question(chat_id: int, state: FSMContext):
    try:
        data = await state.get_data()
        questions = data['questions']
        q_index = data['current_question']
        
        if q_index >= len(questions):
            await finish_quiz(chat_id, state)
            return

        single_quiz = questions[q_index]
        
        # Alohida o'ralgan spiskadan indeks orqali ajratib olish
        question_text = single_quiz[0]
        options = [single_quiz[1], single_quiz[2], single_quiz[3], single_quiz[4]]
        
        labels = ["A", "B", "C", "D"]
        builder = InlineKeyboardBuilder()
        
        random.shuffle(options)

        for i, option in enumerate(options):
            builder.button(
                text=f"{labels[i]}) {option}", 
                callback_data=f"splitquiz_{q_index}_{option}"
            )
        builder.adjust(2)

        msg = await bot.send_message(
            chat_id=chat_id,
            text=f"❓ {q_index + 1}-savol: {question_text}\n\nJavob berish uchun vaqt: 60 soniya",
            reply_markup=builder.as_markup()
        )
        
        await state.set_state(QuizState.answering)
        
        if chat_id in active_timers:
            active_timers[chat_id].cancel()
            
        task = asyncio.create_task(question_timer(chat_id, q_index, state, msg.message_id))
        active_timers[chat_id] = task
        
    except Exception as e:
        print(f"❌ SAVOL YUBORISHDA XATOLIK: {e}")

@dp.callback_query(QuizState.answering, F.data.startswith("splitquiz_"))
async def handle_answer(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    
    if chat_id in active_timers:
        active_timers[chat_id].cancel()
        del active_timers[chat_id]

    info = callback.data.split("_")
    clicked_q_index = int(info[1])
    user_answer = info[2]
    
    data = await state.get_data()
    questions = data['questions']
    q_index = data['current_question']
    correct_count = data['correct_answers']

    if clicked_q_index != q_index:
        await callback.answer("Bu savolning vaqti o'tib ketgan!", show_alert=True)
        return

    # To'g'ri javob spiskamizning eng oxirida (5-indeksda) turadi
    correct_answer = questions[q_index][5]

    if user_answer == correct_answer:
        correct_count += 1
        await callback.answer("To'g'ri! ✅", show_alert=False)
    else:
        await callback.answer(f"❌ Noto'g'ri! To'g'ri javob: {correct_answer}", show_alert=True)

    await state.update_data(current_question=q_index + 1, correct_answers=correct_count)
    
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass
        
    await send_question(chat_id, state)

async def finish_quiz(chat_id: int, state: FSMContext):
    if chat_id in active_timers:
        active_timers[chat_id].cancel()
        del active_timers[chat_id]

    data = await state.get_data()
    correct = data['correct_answers']
    total = len(data['questions'])
    percentage = int((correct / total) * 100)

    result_text = (
        f"🏁 Imtihon yakunlandi!\n\n"
        f"📊 Batafsil natijalar:\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"✅ To'g'ri javoblar: {correct} ta\n"
        f"❌ Noto'g'ri / Ulgurilmagan: {total - correct} ta\n"
        f"📈 Umumiy ko'rsatkich: {percentage}%\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎉 Qatnashganingiz uchun rahmat!"
    )
    
    await bot.send_message(chat_id, result_text)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())