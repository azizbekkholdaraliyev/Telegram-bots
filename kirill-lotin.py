from transliterate import to_cyrillic, to_latin
import telebot

TOKEN = '8886994883:AAHJU6MAJUQGn8GnyUBEaRE3WfuywP3MPRo'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start']) #bu turdagi sozlarga pastdagi funksiya masul degan manoda
def send_welcome(message):  #message --- foydalanuvchi yozgan habar
	javob = "Assalomu alaykum, hush kelibsiz!"
	javob += "\nMatn kiriting: "
	bot.reply_to(message,javob) #reply_to() --- foydalanuvchiga habar yuboradigan funksiya

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	msg = message.text
	javob = lambda msg: to_cyrillic(msg) if msg.isascii() else to_latin(msg)
	bot.reply_to(message, javob(msg))

bot.infinity_polling()
