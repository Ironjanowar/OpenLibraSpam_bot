import telebot
import os.path as path
import sys
import json
from telebot import types

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

# Vars
formats = [".pdf", ".epub", ".mobi", ".azw"]

# Funciones


def isAdmin_fromPrivate(message):
    if message.chat.type == 'private':
        userID = message.from_user.id
        if str(userID) in admins:
            return True
    return False


def file_format(file_name):
    for file_format in formats:
        if file_name.endswith(file_format):
            return True
    # Si no es un formate valido
    return False

# Handlers


@bot.message_handler(content_types=['document'])
def spam_pdf(message):
    print("Documento detectado\n")
    if message.document.file_name is not None and file_format(message.document.file_name):
        markup = types.InlineKeyboardMarkup()
        button_callback = "Si:" + str(message.document.file_id)
        si_button = types.InlineKeyboardButton("Si", callback_data=button_callback)
        no_button = types.InlineKeyboardButton("No", callback_data="No")
        markup.add(si_button, no_button)
        bot.reply_to(message, "Quieres reenviar este archivo?", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("Si:"))
def catch_si(c):
    bot.send_document("@openlibra_channel", c.data.split(':')[1])
    bot.edit_message_text("Archivo reenviado a @openlibra_channel", chat_id=c.message.chat.id, message_id=c.message.message_id)
    print("Documento enviado\n")


@bot.callback_query_handler(func=lambda callback: callback.data == "No")
def catch_no(c):
    bot.edit_message_text("El archivo no se enviará", chat_id=c.message.chat.id, message_id=c.message.message_id)
    print("Archivo ignorado\n")


@bot.message_handler(commands=['update'])
def auto_update(message):
    if isAdmin_fromPrivate(message):
        bot.reply_to(message, "Reiniciando..\n\nPrueba algun comando en 10 segundos")
        print("Updating..")
        sys.exit()
    else:
        bot.reply_to(message, "Este comando es solo para admins y debe ser enviado por privado")


@bot.message_handler(commands=['isup'])
def is_up(message):
    bot.reply_to(message, "I'm up! :D")


# Quitar
bot.skip_pending = True

# Correr bot
print("Running...")
bot.polling()
