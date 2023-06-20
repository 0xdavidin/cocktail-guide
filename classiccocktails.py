from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import json

# Загружаем данные о классических коктейлях из файла JSON
with open("cocktails.json", "r") as file:
    cocktails_data = json.load(file)

def start(update, context):
    reply_markup = create_keyboard_markup()
    update.message.reply_text("Привет! Я знаю много классических коктейлей. Выбери коктейль, чтобы узнать больше.", reply_markup=reply_markup)

def create_keyboard_markup():
    # Создаем инлайн-клавиатуру с кнопками для выбора коктейля
    keyboard = [[InlineKeyboardButton(cocktail["name"], callback_data=cocktail["name"])] for cocktail in cocktails_data]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def get_cocktail_info(update, context):
    query = update.callback_query
    cocktail_name = query.data

    # Находим информацию о выбранном коктейле
    cocktail_info = next(cocktail for cocktail in cocktails_data if cocktail["name"] == cocktail_name)

    # Отправляем информацию о коктейле пользователю
    query.edit_message_text(text=f"Название: {cocktail_info['name']}\nИнгредиенты: {', '.join(cocktail_info['ingredients'])}\nРецепт: {cocktail_info['recipe']}")

def main():
    # Замените "YOUR_TELEGRAM_TOKEN" на ваш токен Telegram Bot API
    updater = Updater(token="YOUR_TELEGRAM_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    cocktail_handler = CallbackQueryHandler(get_cocktail_info)
    dispatcher.add_handler(cocktail_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
