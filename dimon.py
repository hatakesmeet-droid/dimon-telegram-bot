
import os
import random
import sqlite3
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram.error import TelegramError

TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = "dimon_users.db"
KYIV = ZoneInfo("Europe/Kyiv")

JOKES = [
    "🍆 Дімон вошёл в комнату. Уверенность вышла на новый уровень!",
    "Почему Максимус не боится конкурентов? Потому что у него харизма с турбонаддувом 😂",
    "Девушки любят ушами. Поэтому Дімон сначала включает чувство юмора 😏",
    "Сегодня твоя харизма настолько мощная, что зеркало попросило автограф.",
    "Не сантиметры красят мужчину, а умение рассмешить девушку. Ну и чувство такта 😈",
    "Дімон, твоя уверенность сегодня длиннее очереди в супермаркете!"
]

SECRETS = [
    "🤫 Секрет Максимуса: не покупай чудо-средства с обещанием +10 см за три дня.",
    "😏 Секрет №2: уверенность — лучший аксессуар мужчины.",
    "🍆 Секрет №3: чувство юмора иногда работает лучше дорогого парфюма.",
    "👑 Секрет №4: настоящий Дімон не сравнивает себя с другими.",
    "🔥 Секрет №5: уважение и взаимное согласие всегда в моде."
]

PREDICTIONS = [
    "🔮 Сегодня тебя ждёт успех. Возможно, даже две порции борща!",
    "🍆 Звёзды говорят: твоя харизма сегодня зашкаливает.",
    "😈 Сегодня удачный день для комплиментов и хорошего настроения.",
    "👑 Судьба готовит тебе приятный сюрприз. Не забудь улыбнуться!",
    "🔥 Сегодня твоя уверенность способна зажечь даже выключенную лампочку.",
    "😂 День обещает быть настолько хорошим, что даже носки найдут свою пару."
]


def init_db():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY
            )
        """)


def save_user(chat_id):
    with sqlite3.connect(DB_NAME) as db:
        db.execute(
            "INSERT OR IGNORE INTO users (chat_id) VALUES (?)",
            (chat_id,)
        )


def remove_user(chat_id):
    with sqlite3.connect(DB_NAME) as db:
        db.execute(
            "DELETE FROM users WHERE chat_id = ?",
            (chat_id,)
        )


def get_users():
    with sqlite3.connect(DB_NAME) as db:
        return [
            row[0]
            for row in db.execute("SELECT chat_id FROM users").fetchall()
        ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_user(chat_id)

    await update.message.reply_text(
        "🍆 ДОБРО ПОЖАЛОВАТЬ!\n"
        "Я — ПІПІСЬ МАКСІМУС ДІМОН!\n\n"
        "Здесь прокачиваем харизму, уверенность "
        "и чувство юмора 18+ 😈\n\n"
        "📏 /size — рейтинг богатыря\n"
        "💪 /boost — мотивация\n"
        "😂 /joke — пошлая шутка\n"
        "🤫 /secret — секрет Максимуса\n"
        "🔮 /prediction — предсказание дня\n"
        "🔔 /daily_on — ежедневные предсказания\n"
        "🔕 /daily_off — отключить предсказания\n"
        "❓ /help — помощь\n\n"
        "Дімон уже на посту. Берегите чувство юмора! 😂"
    )


async def size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📏 РЕЗУЛЬТАТ ИЗМЕРЕНИЯ:\n\n"
        "Уверенность: 1000/10 👑\n"
        "Харизма: легендарная 🔥\n"
        "Чувство юмора: 3000/10 😂\n"
        "Самооценка: императорская!\n\n"
        "Реальные сантиметры не измеряем. "
        "Дімон уважает науку! 😎"
    )


async def boost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💪 СЛУШАЙ, БОГАТЫРЬ!\n\n"
        "Подними голову, расправь плечи и улыбнись.\n"
        "Ты не обязан быть идеальным, чтобы быть крутым.\n\n"
        "Дімон верит в тебя! 🍆👑"
    )


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JOKES))


async def secret(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(SECRETS))


async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(PREDICTIONS))


async def daily_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_chat.id)
    await update.message.reply_text(
        "🔔 Ежедневные предсказания включены!\n"
        "Каждое утро в 09:00 по Киеву Дімон "
        "будет присылать тебе прогноз 🍆🔮"
    )


async def daily_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    remove_user(update.effective_chat.id)
    await update.message.reply_text(
        "🔕 Ежедневные предсказания отключены.\n"
        "Если соскучишься по Дімону — жми /daily_on 😎"
    )


async def send_daily_predictions(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in get_users():
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text="🌞 ДОБРОЕ УТРО ОТ ДІМОНА!\n\n"
                     + random.choice(PREDICTIONS)
                     + "\n\nПусть день будет легендарным! 🍆👑"
            )
        except TelegramError as error:
            print(f"Не удалось отправить сообщение {chat_id}: {error}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 КОМАНДЫ ДІМОНА:\n\n"
        "/start — запуск бота\n"
        "/size — рейтинг богатыря\n"
        "/boost — заряд уверенности\n"
        "/joke — шутка 18+\n"
        "/secret — секрет\n"
        "/prediction — предсказание\n"
        "/daily_on — ежедневные сообщения\n"
        "/daily_off — отключить сообщения"
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Добавь токен в переменные окружения."
        )

    init_db()

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("size", size))
    app.add_handler(CommandHandler("boost", boost))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("secret", secret))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("daily_on", daily_on))
    app.add_handler(CommandHandler("daily_off", daily_off))
    app.add_handler(CommandHandler("help", help_command))

    # Ежедневная рассылка в 09:00 по Киеву
    app.job_queue.run_daily(
        send_daily_predictions,
        time=time(hour=9, minute=0, tzinfo=KYIV),
        name="daily_predictions"
    )

    print("🍆 ПІПІСЬ МАКСІМУС ДІМОН запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
