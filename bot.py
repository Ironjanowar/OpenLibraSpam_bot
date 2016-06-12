import telebot
import os.path as path
import sys
import json

# Creamos el bot
if not path.isfile("bot.token"):
    print("Error: \"bot.token\" not found!")
    sys.exit()

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

if not path.isfile("./data/admins.json"):
    with open('./data/admins.json', 'w') as adminData:
        adminData.write('{}')
        adminData.close

with open('./data/admins.json', 'r') as adminData:
    admins = json.load(adminData)

# Funciones


def isAdmin_fromPrivate(message):
    if message.chat.type == 'private':
        userID = message.from_user.id
        if str(userID) in admins:
            return True
    return False

# Handlers


@bot.message_handler(content_types=['document'])
def spam_pdf(message):
    if message.document.file_name.endswith(".pdf"):
#        bot.forward_message("@openlibra_channel", message.chat.id, message.message_id, disable_notification=True)
        bot.send_document("@openlibra_channel", message.document)
        bot.reply_to(message, "Mensaje reenviado a @openlibra_channel")


@bot.message_handler(commands=['update'])
def auto_update(message):
    if isAdmin_fromPrivate(message):
        bot.reply_to(message, "Reiniciando..\n\nPrueba algun comando en 10 segundos")
        print("Updating..")
        sys.exit()
    else:
        bot.reply_to(message, "Este comando es solo para admins y debe ser enviado por privado")

# Correr bot
print("Running...")
bot.polling()
