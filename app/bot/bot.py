import os
import telebot
from django.conf import settings

# Замените на ваш токен бота
BOT_TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
👋 Привет! Я бот для игры "Угадай число"

🎮 Правила просты:
• Я загадываю число от 1 до 100
• Ты пытаешься угадать
• Я подсказываю "больше" или "меньше"

🚀 Нажми кнопку ниже, чтобы начать играть!
    """
    
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(
        text="🎮 Играть в Угадай число", 
        web_app=telebot.types.WebAppInfo(url="https://your-domain.com/game/")
    )
    markup.add(button)
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup
    )

@bot.message_handler(commands=['game'])
def send_game(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(
        text="🎮 Начать игру", 
        web_app=telebot.types.WebAppInfo(url="https://your-domain.com/game/")
    )
    markup.add(button)
    
    bot.send_message(
        message.chat.id,
        "Нажми кнопку ниже, чтобы открыть игру:",
        reply_markup=markup
    )

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()