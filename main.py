import telebot
import config
import random
from telebot import types

number = random.randint(1, 10)
n = 3
bot = telebot.TeleBot(config.telegram_token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes) # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text='Привет, поиграем в числа?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Отлично, я загадал число от 1 до 10. Угадай какое?')
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Жаль(')

@bot.message_handler(content_types=['text'])
def game(message):
    global user_number
    try:
        global n
        user_number = int(message.text)
        if int(message.text) == number:
            bot.send_message(message.chat.id, 'Ты угадал, поздравляю!!!')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEL29iMzBOZVNNlxh_aPkDmvc7hMZtDQACGgEAAlKJkSPGYmpoYYli_SME')
            n = 3
        elif int(message.text) > number:
            n -= 1
            if n == 0:
                bot.send_message(message.chat.id, 'Ты проиграл.')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEMqNiNE4CunoVtM3_BsXkNiR1EX5HgwACIgEAAlKJkSPI4ZRB58JpMyME')
                n = 3
            else:
                bot.send_message(message.chat.id, 'Осталось попыток: ' + str(n))
                bot.send_message(message.chat.id, 'Моё число меньше.')
        else:
            n -= 1
            if n == 0:
                bot.send_message(message.chat.id, 'Ты проиграл.')
                bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAEEMqNiNE4CunoVtM3_BsXkNiR1EX5HgwACIgEAAlKJkSPI4ZRB58JpMyME')
                n = 3
            else:
                bot.send_message(message.chat.id, 'Осталось попыток: ' + str(n))
                bot.send_message(message.chat.id, 'Моё число больше.')
    except Exception:
        bot.send_message(message.chat.id, 'Вводите цифрами, а не буквами.')

bot.polling(none_stop=True)