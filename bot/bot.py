import telebot
import urllib
from telebot import types
import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    choice_btn = types.KeyboardButton(text='Choice')
    menu_btn = types.KeyboardButton(text='Menu')

    text = '''Доброго времени суток!\n" \
            Я бот, берущий данные с сайта ресторана Il Patio!\n
            Вы можете посмотреть меню ресторана либо получить персональную подборку блюд.\n
            Чтобы сделать выбор, нажмите соответствующую кнопку.
            '''

    markup.add(choice_btn, menu_btn)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def choice_category(message):
    category = ['🍕 Пицца', '🍜 Паста', '🍲 Горячие блюда', '🥗 Салаты и закуски']

    if message.text == 'Menu':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        pizza_btn = types.KeyboardButton(text='🍕 Пицца')
        pasta_btn = types.KeyboardButton(text='🍜 Паста')
        hot_dish_btn = types.KeyboardButton(text='🍲 Горячие блюда')
        salad_btn = types.KeyboardButton(text='🥗 Салаты и закуски')

        markup.add(pizza_btn, pasta_btn, hot_dish_btn, salad_btn)
        text = "Какую катеорию меню вы хотите выбрать?"

        bot.send_message(message.chat.id, text, reply_markup=markup)

    elif message.text == 'Choice':
        text = '''Выберете категорию и укажите сумму в рублях, на которую хотите получить персональную подборку:\n
                🍕 Пицца\n
                🍜 Паста\n
                🍲 Горячие блюда\n
                🥗 Салаты и закуски\n
                Пример запроса: Пицца, 3000
                '''
        bot.send_message(message.from_user.id, text)

        cur_category, cur_price = message.text.split()
        personal_selection = requests.get(f'http://backend:8080/selection/{cur_category[:-1]}/{cur_price}').json()
        desc = 'Ваша персональная подборка блюд:\n'
        cur_sum = 0
        for dishes in personal_selection:
            desc += dishes[1] + '\n'
            cur_sum += dishes[3]
        desc += '\nСумма блюд: ' + str(cur_sum) + '₽\n'
        desc += '\nЕсли хотите получить более подробную информацию о блюде, напишите его название в чат'
        bot.send_message(message.from_user.id, desc)

    elif message.text in category:
        text = f'🍽 Весь ассортимент выбранной категории перед вами {message.text[:1]}:\n\n'
        req = requests.get(f'http://backend:8080/select_name/{message.text[2:]}').json()

        for elem in req:
            text += message.text[:1] + ' ' + elem[0] + '\n'
        text += '\n💵 Чтобы узнать описание и цену, напишите название блюда.'
        bot.send_message(message.from_user.id, text)

    for item in category:
        all_item = requests.get(f'http://backend:8080/select_name/{item[2:]}').json()
        for cur_item in all_item:
            if message.text == cur_item[0]:
                item = requests.get(f'http://backend:8080/select_elem/{cur_item[0]}').json()
                text = '📍 Название: ' + item[0][0] + ' ' + item[0][1] + '\n' + '📍 Описание: ' + item[0][
                    2] + '\n\n' + '💵 цена: ' + item[0][3] + '₽'
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
