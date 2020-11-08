import telebot
import os
from telebot import types


bot = telebot.TeleBot('')


@bot.message_handler(commands=['start', 'help'])
def f(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/new_item', '/delete', '/all')
    bot.send_message(message.chat.id, 'Welcome! I am todo bot', reply_markup=markup)


@bot.message_handler(commands=['new_item'])
def new_item(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id,'Enter the item'), add_new_item)

def add_new_item(message):
    directory = os.path.join('list_of_user', str(message.from_user.id) + '.txt')
    c = 'a' if os.path.exists(directory) else 'w'
    with open(directory, c) as file:
        file.write(message.text + '\n')
    bot.send_message(message.chat.id, 'done')


@bot.message_handler(commands=['all'])
def all(message):
    directory = os.path.join('list_of_user', str(message.from_user.id) + '.txt')
    tasks = ''.join(('{}. {}'.format(number, item) for number, item in enumerate(open(directory).readlines(), 1))) if os.path.exists(directory) else ''
    bot.send_message(message.chat.id, "You don't have items" if not tasks else tasks)


@bot.message_handler(commands=['delete'])
def numbers_delete(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id,'Enter numbers of items that should be delete separated by commas'), delete)

def delete(message):
    directory = os.path.join('list_of_user', str(message.from_user.id) + '.txt')
    try:
        tasks = open(directory).readlines()
        for number in message.text.split(','):
            int(number)
            tasks[int(number) - 1]
    except:
        bot.send_message(message.chat.id, "Invalid request")
        return
    tasks = (item for number, item in enumerate(open(directory).readlines(), 1) if not(number in set(map(int, message.text.split(',')))))
    with open(directory, 'w') as file:
        file.writelines(tasks)
    bot.send_message(message.chat.id, 'done')


bot.polling()