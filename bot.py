import telebot
from telebot import types
from database import DataBase

f = open('.idea/token.txt', 'r')
TOKEN = f.readline()
bot = telebot.TeleBot(TOKEN)
db = DataBase()
db.insert()


@bot.message_handler(commands=['start'])
def url(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pizza_btn = types.KeyboardButton(text='🍕 Пицца')
    pasta_btn = types.KeyboardButton(text='🍜 Паста')
    hot_dish_btn = types.KeyboardButton(text='🍲 Горячие блюда')
    salad_btn = types.KeyboardButton(text='🥗 Салаты и закуски')

    markup.add(pizza_btn, pasta_btn, hot_dish_btn, salad_btn)
    text = "Доброго времени суток!\nЯ бот, берущий данные с сайта ресторана Il Patio!\nКакую катеорию меню вы хотите выбрать?"
    bot.send_message(message.from_user.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_item(message):
    category = ['🍕 Пицца', '🍜 Паста', '🍲 Горячие блюда', '🥗 Салаты и закуски']
    if message.text in category:
        text = f'🍽 Весь ассортимент выбранной категории перед вами {message.text[:1]}:\n\n'
        for elem in db.select_name(message.text[2:]).fetchall():
            text += message.text[:1] + ' ' + elem[0] + '\n'
        text += '\n💵 Чтобы узнать описание и цену, напишите название блюда.'
        bot.send_message(message.from_user.id, text)
    #else:
    #    bot.send_message(message.from_user.id, "Извините, такой категории нет!")

    for item in category:
        all_item = db.select_name(item[2:]).fetchall()
        for cur_item in all_item:
            if message.text == cur_item[0]:
                item = db.select_elem(cur_item[0]).fetchall()
                text = '📍 Название: ' + item[0][0] + ' ' + item[0][1] + '\n' + '📍 Описание: ' + item[0][
                    2] + '\n\n' + '💵 ' + item[0][3]
                bot.send_message(message.from_user.id, text)
    #    if message.text not in all_item:
    #        bot.send_message(message.from_user.id, "Извините, такого блюда в меню нет!")


print('hello world')
bot.polling(none_stop=True, interval=0)
