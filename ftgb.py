import telebot
import sqlite3
import threading
import time
from telebot import TeleBot
from telebot import types

bot = telebot.TeleBot('6013536682:AAFtKRJ95FToI6yAMNxXs1YpaJcV3ndXJMw')

message_history = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    connect = sqlite3.connect(f'passwords_{message.chat.id}.db')
    c = connect.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                UNIQUE(service))''')
    connect.commit()
    welcome_message = "Welcome to the <b>password storage bot</b>!\n\n"
    welcome_message += "To add a new login/password, click <b>SET PASSWORD</b>.\n\n"
    welcome_message += "To see a login/password, click <b>GET PASSWORD</b>.\n\n"
    welcome_message += "To delete a login/password, click <b>DELETE PASSWORD</b>.\n\n"
    welcome_message += "To see services with saved passwords, click <b>SHOW SERVICES</b>.\n\n"
    welcome_message += "To stop the operation you started, click <b>CANCEL</b>."
    bot.reply_to(message, welcome_message, parse_mode='HTML')
    handle_menu(message)

@bot.message_handler(commands=['menu'])
def handle_menu(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('SET PASSWORD', callback_data='set')
    btn2 = types.InlineKeyboardButton('GET PASSWORD', callback_data='get')
    btn3 = types.InlineKeyboardButton('DELETE PASSWORD', callback_data='del')
    btn4 = types.InlineKeyboardButton('SHOW SERVICES', callback_data='services')
    btn5 = types.InlineKeyboardButton('cancel', callback_data='cancel')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(chat_id, "Choose an option:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'set')
def handle_set_callback(call):
    chat_id = call.message.chat.id
    bot_sen = bot.send_message(chat_id, "Please enter the <service> <login> <password> separated by spaces.")
    message_history[chat_id] = ['set']
    message_ids = [bot_sen.id]
    threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()

@bot.callback_query_handler(func=lambda call: call.data == 'get')
def handle_set_callback(call):
    chat_id = call.message.chat.id
    bot_sen = bot.send_message(chat_id, "Please enter the <service> name.")
    message_history[chat_id] = ['get']
    message_ids = [bot_sen.id]
    threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()

@bot.callback_query_handler(func=lambda call: call.data == 'del')
def handle_set_callback(call):
    chat_id = call.message.chat.id
    bot_sen = bot.send_message(chat_id, "Please enter the <service> name.")
    message_history[chat_id] = ['del']
    message_ids = [bot_sen.id]
    threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()

@bot.callback_query_handler(func=lambda call: call.data == 'services')
def handle_services_callback(call):
    chat_id = call.message.chat.id
    connect = sqlite3.connect(f'passwords_{chat_id}.db')
    c = connect.cursor()
    c.execute('''SELECT service FROM users''')
    services = c.fetchall()
    if services:
        services = sorted(set([service[0] for service in services]))
        message = "\n".join(services)
        bot.send_message(chat_id, f"Your saved services:\n{message}")
    else:
        bot.send_message(chat_id, "You haven't saved any services yet.")
    handle_menu(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def handle_cancel_callback(call):
    chat_id = call.message.chat.id
    if chat_id in message_history:
        message_history.pop(chat_id, None)
    bot_sen = bot.send_message(chat_id, "Operation cancelled.")
    handle_menu(call.message)
    message_ids = [bot_sen.id]
    threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()

def delete_messages(chat_id, message_ids):
    for message_id in message_ids:
        bot.delete_message(chat_id, message_id)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    if chat_id in message_history and message_history[chat_id][0] == 'set':
        text = message.text.split()
        if len(text) < 3:
            bot_reply = bot.reply_to(message, "Usage: <service> <login> <password>")
            message_ids = [message.id, bot_reply.id]
            threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()
            return
        service, login, password = text[0], text[1], text[2]
        connect = sqlite3.connect(f'passwords_{chat_id}.db')
        c = connect.cursor()
        c.execute("SELECT COUNT(*) FROM users WHERE service=?", (service,))
        result = c.fetchone()
        if result and result[0] > 0:
            bot_reply = bot.reply_to(message, f"Error: login/password already exists for {service}.")
            message_ids = [message.id, bot_reply.id]
            threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()
            message_history.pop(chat_id, None)
            handle_menu(message)
            return
        c.execute("INSERT OR REPLACE INTO users (service, login, password) VALUES (?, ?, ?)", (service, login, password))
        connect.commit()

        bot_reply = bot.reply_to(message, f"Login/password for {service} set.")
        message_ids = [message.id, bot_reply.id]
        threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()
        message_history.pop(chat_id, None)
        handle_menu(message)

    elif chat_id in message_history and message_history[chat_id][0] == 'get':
        service = message.text.strip()
        connect = sqlite3.connect(f'passwords_{chat_id}.db')
        c = connect.cursor()
        c.execute("SELECT login, password FROM users WHERE service=?", (service,))
        result = c.fetchone()
        if result:
            login, password = result
            bot_reply = bot.reply_to(message, f"Login: {login}\nPassword: {password}")
        else:
            bot_reply = bot.reply_to(message, f"No login/password found for {service}.")
        message_ids = [message.id, bot_reply.id]
        threading.Timer(15, delete_messages, args=[chat_id, message_ids]).start()
        message_history.pop(chat_id, None)
        handle_menu(message)

    elif chat_id in message_history and message_history[chat_id][0] == 'del':
        service = message.text.strip()
        connect = sqlite3.connect(f'passwords_{chat_id}.db')
        c = connect.cursor()
        c.execute("DELETE FROM users WHERE service=?", (service,))
        connect.commit()

        if c.rowcount == 0:
            bot.reply_to(message, f"No login/password found for {service}.")
        else:
            bot.reply_to(message, f"Login/password for {service} deleted.")

        message_history.pop(chat_id, None)
        handle_menu(message)

bot.polling(none_stop=True, interval=0)


