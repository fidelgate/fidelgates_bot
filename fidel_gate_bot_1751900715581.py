
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# States for tutor and student flows
TUTOR_NAME, TUTOR_gradeLEVELS, TUTOR_SUBJECTS, TUTOR_LOCATION = range(4)
STUDENT_NAME, STUDENT_GRADE, STUDENT_REQUEST = range(3)


SUPPORT_USERNAME = "@fidelgatesupport"
RESOURCE_CHANNEL_LINK = "https://t.me/+2repcvnrUdBiMGY0"
BOT_TOKEN = "8161255016:AAF-VKJtOKuYwagdG2VAiB2DXKIkCri3Ffw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Register as a Tutor"), KeyboardButton("I am a Student")],
        [KeyboardButton("Access Past Exams"), KeyboardButton("Support & Payment")]
    ]
    await update.message.reply_text(
        "Welcome to Fidel Gate!\n\nChoose what you need:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ---- TUTOR FLOW ----
async def tutor_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Let's register you as a tutor.\nWhat is your full name?")
    return TUTOR_NAME

async def tutor_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tutor_name"] = update.message.text
    await update.message.reply_text("Which grade levels do you teach?")
    return TUTOR_LEVELS

async def tutor_levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tutor_levels"] = update.message.text
    await update.message.reply_text("What subject(s) do you teach?")
    return TUTOR_SUBJECTS

async def tutor_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tutor_subjects"] = update.message.text
    await update.message.reply_text("Where are you located? (City/Sub-city)")
    return TUTOR_LOCATION

async def tutor_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tutor_location"] = update.message.text
    msg = f"New Tutor Registration:\nName: {context.user_data['tutor_name']}\nGrades: {context.user_data['tutor_levels']}\nSubjects: {context.user_data['tutor_subjects']}\nLocation: {context.user_data['tutor_location']}"
    await context.bot.send_message(chat_id=SUPPORT_USERNAME, text=msg)
    await update.message.reply_text("Thank you for registering! We'll get back to you soon.")
    return ConversationHandler.END

# ---- STUDENT FLOW ----
async def student_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Let's help you.\nWhat is your name?")
    return STUDENT_NAME

async def student_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["student_name"] = update.message.text
    await update.message.reply_text("What is your grade level?")
    return STUDENT_GRADE

async def student_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["student_grade"] = update.message.text
    await update.message.reply_text("What subject or support do you need?")
    return STUDENT_REQUEST

async def student_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["student_request"] = update.message.text
    msg = f"New Student Request:\nName: {context.user_data['student_name']}\nGrade: {context.user_data['student_grade']}\nRequest: {context.user_data['student_request']}"
    await context.bot.send_message(chat_id=SUPPORT_USERNAME, text=msg)
    await update.message.reply_text("Thank you! We'll contact you shortly.")
    return ConversationHandler.END

# ---- OTHER FLOWS ----
async def access_past_exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Access all past exams here:\n{RESOURCE_CHANNEL_LINK}")

async def support_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"For support or payment, contact: {SUPPORT_USERNAME}\nFidel Gate is expanding to include AI tools, e-books, and more.")

# ---- CANCEL ----
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# Application setup
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex("Access Past Exams"), access_past_exams))
app.add_handler(MessageHandler(filters.Regex("Support & Payment"), support_payment))

# Tutor Conversation
tutor_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Register as a Tutor"), tutor_start)],
    states={
        TUTOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, tutor_name)],
        TUTOR_LEVELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, tutor_levels)],
        TUTOR_SUBJECTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, tutor_subjects)],
        TUTOR_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, tutor_location)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

# Student Conversation
student_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("I am a Student"), student_start)],
    states={
        STUDENT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, student_name)],
        STUDENT_GRADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, student_grade)],
        STUDENT_REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, student_request)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

app.add_handler(tutor_conv)
app.add_handler(student_conv)

print("Fidel Gate Bot is running...")
app.run_polling()
