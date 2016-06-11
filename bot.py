import telebot
import os.path as path
import sys
import ipdb

# Creamos el bot
if not path.isfile("bot.token"):
    print("Error: \"bot.token\" not found!")
    sys.exit()

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Ignorar mensajes antiguos
bot.skip_pending = True

# Listener


def listener(messages):
    # When new messages arrive TeleBot will call this function.
    for m in messages:
        if m.content_type == 'text':
            # Prints the sent message to the console
            if m.chat.type == 'private':
                print("Chat -> " + str(m.chat.first_name) +
                      " [" + str(m.chat.id) + "]: " + m.text)
            else:
                print("Group -> " + str(m.chat.title) +
                      " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'document':
            print("Se ha enviado un documento")
        else:
            print("Se ha enviado otra cosa")

# Initializing listener
bot.set_update_listener(listener)


# Handlers


@bot.message_handler(content_types=['document'])
def spam_pdf(message):
    bot.reply_to(message, "Un documento :D")

@bot.message_handler(commands=['hello'])
def spam_txt(m):
    bot.reply_to(m, "Texto! :D")


# Correr bot
print("Running...")
bot.polling()
