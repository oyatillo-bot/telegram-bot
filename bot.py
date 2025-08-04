from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)
import asyncio

# TOKENINGIZ
BOT_TOKEN = "7708531342:AAGiFrP_cj6wVdi5_pAKXlm2_K3A1e8ygmM"   # BotFather dan olingan token

# ADMIN ID (Userinfobot orqali topasiz)
ADMIN_ID = 6211000252

# Kurslar ro'yxati
courses = {
    "Python": "Python dasturlash asoslari : 3 oy davomida o'rganasiz.",
    "English": "Ingliz tili kursi : Beginner dan Intermediate darajagacha.",
    "Design": "Grafik dizayn: Photoshop va Illustrator darslari.",
    "Nemis": "Nemis tili kursi : A1 dan B1 darajagacha.",
    "Koreys": "Koreys tili kursi : Asosiy darajadan o'rta darajaga.",
    "Logistic": "Logistika kursi : 2 oy davomida nazariy va amaliy darslar."
}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kurslar uchun tugmalar
    keyboard = [[course] for course in courses.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Kurslardan birini tanlang:", reply_markup=reply_markup)


# Xabarlarni boshqarish (kurs tanlash, ism va telefon olish)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    # Har bir xabarni admin ga yuborish
    contact = update.message.contact
    msg_text = text if text else (contact.phone_number if contact else "Xabar yo'q")

    await context.bot.send_message(
    chat_id=ADMIN_ID,
    text=f"Yangi xabar:\n\nUser: {user.full_name} ({user.id})\nXabar: {msg_text}"
)


    step = context.user_data.get("step")

    # Agar kurs tanlangan bo‘lsa
    if text in courses.keys() and step is None:
        context.user_data["course"] = text
        context.user_data["step"] = "name"

        await update.message.reply_text(
            f"Siz {text} kursini tanladingiz.\n\nIsmingizni yuboring:"
        )

    # Agar ism kiritilgan bo‘lsa
    elif step == "name":
        context.user_data["name"] = text
        context.user_data["step"] = "phone"

        # Telefon tugmasi
        contact_button = KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)

        await update.message.reply_text("Rahmat! Endi telefon raqamingizni yuboring:", reply_markup=reply_markup)

    # Agar telefon yuborilayotgan bo‘lsa
    elif step == "phone" and (contact or text):
        phone = contact.phone_number if contact else text
        name = context.user_data.get("name")
        course = context.user_data.get("course")

    # Faylga yozish
    with open("registrations.txt", "a", encoding="utf-8") as f:
        f.write(f"{name} | {phone} | {course}\n")

    # Admin uchun umumiy xabar
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Yangi ro'yxatdan o'tish:\n\n"
             f"Ism: {name}\n"
             f"Telefon: {phone}\n"
             f"Kurs: {course}\n"
             f"User ID: {user.id}"
    )

    # Foydalanuvchiga javob
    await update.message.reply_text(
        f"Tabriklaymiz, {name}! Siz {course} kursiga muvaffaqiyatli ro'yxatdan o'tdingiz.\n\n"
        f"Tez orada siz bilan bog'lanamiz☺"
    )

    context.user_data.clear()




# Asosiy funksiya
def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(MessageHandler(filters.CONTACT, message_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
