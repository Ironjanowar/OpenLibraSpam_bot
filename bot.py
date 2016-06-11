import telebot
import os.path as path
import sys

# Creamos el bot
if not path.isfile("bot.token"):
    print("Error: \"bot.token\" not found!")
    sys.exit()

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Handlers


@bot.message_handler(content_types=['document'])
def spam_pdf(message):
    bot.forward_message("@openlibra_channel", message.chat.id, message.message_id, disable_notification=True)
    bot.reply_to(message, "Mensaje reenviado a @openlibra_channel")

# Correr bot
print("Running...")
bot.polling()
