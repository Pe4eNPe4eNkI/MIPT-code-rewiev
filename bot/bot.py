import telebot
import urllib
from telebot import types
import psycopg2


conn = psycopg2.connect(
            dbname="il_patio_db",
            user="postgres",
            password="root",
            host="database")

cur = conn.cursor()

def select_all():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Menu')
    conn.commit()
    return cursor

def select_category(category):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Menu WHERE type_p =%s', (category,))
    conn.commit()
    return cursor

def select_elem(elem):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Menu WHERE name_p =%s', (elem,))
    conn.commit()
    return cursor

def select_name(category):
    cursor = conn.cursor()
    cursor.execute('SELECT name_p FROM Menu WHERE type_p =%s', (category,))
    conn.commit()
    return cursor

def select_all_category():
    cursor = conn.cursor()
    cursor.execute('SELECT type_p FROM Menu')
    conn.commit()
    return cursor


f = open('token.txt', 'r')
TOKEN = f.readline()
bot = telebot.TeleBot(TOKEN)
f.close()


@bot.message_handler(commands=['start'])
def greeting(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pizza_btn = types.KeyboardButton(text='🍕 Пицца')
    pasta_btn = types.KeyboardButton(text='🍜 Паста')
    hot_dish_btn = types.KeyboardButton(text='🍲 Горячие блюда')
    salad_btn = types.KeyboardButton(text='🥗 Салаты и закуски')

    markup.add(pizza_btn, pasta_btn, hot_dish_btn, salad_btn)
    text = "Доброго времени суток!\n" \
           "Я бот, берущий данные с сайта ресторана Il Patio!\nКакую катеорию меню вы хотите выбрать?"
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def choise_category(message):
    category = ['🍕 Пицца', '🍜 Паста', '🍲 Горячие блюда', '🥗 Салаты и закуски']
    if message.text in category:
        text = f'🍽 Весь ассортимент выбранной категории перед вами {message.text[:1]}:\n\n'
        for elem in select_name(message.text[2:]).fetchall():
            text += message.text[:1] + ' ' + elem[0] + '\n'
        text += '\n💵 Чтобы узнать описание и цену, напишите название блюда.'
        bot.send_message(message.from_user.id, text)

    for item in category:
        all_item = select_name(item[2:]).fetchall()
        for cur_item in all_item:
            if message.text == cur_item[0]:
                item = select_elem(cur_item[0]).fetchall()
                text = '📍 Название: ' + item[0][0] + ' ' + item[0][1] + '\n' + '📍 Описание: ' + item[0][
                    2] + '\n\n' + '💵 ' + item[0][3]

                url = item[0][4]
                f1 = open('img.jpg', 'wb')
                f1.write(urllib.request.urlopen(url).read())
                f1.close()
                bot.send_chat_action(message.from_user.id, 'upload_photo')
                img = open('img.jpg', 'rb')

                bot.send_photo(message.chat.id, img, text, reply_to_message_id=message.message_id)
                img.close()


print('hello world')
bot.polling(none_stop=True, interval=0)
