import telebot
from openai import OpenAI, RateLimitError
import requests
from deep_translator import GoogleTranslator
from API import TOKEN, AI_TOKEN, WEATHER_API, API_CAT, API_GIF

bot = telebot.TeleBot(TOKEN)

dialog = {}

def get_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('🤖Поговорить с нейросетью🤖'))
    markup.add(telebot.types.KeyboardButton('☁️Узнать погоду☁️'))
    markup.add(telebot.types.KeyboardButton('🐶Получить фото котика/собачки😸'))
    markup.add(telebot.types.KeyboardButton('✌️Получить совет✌️'))
    markup.add(telebot.types.KeyboardButton('👀Получить GIF👀'))
    return markup

def get_ai_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Завершить диалог'))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋Приветствую!👋\nВыбери действие:", reply_markup=get_markup())

@bot.message_handler(func=lambda message:True)
def message_user(message):
    chat_id = message.chat.id

    if message.text == 'Завершить диалог': #Проверка диалога с нейронкой
        dialog[chat_id] = False
        bot.send_message(chat_id, "❌Диалог завершен❌.", reply_markup=get_markup())
    elif dialog.get(chat_id, False):
        ai_message(message)

    elif message.text == '🤖Поговорить с нейросетью🤖':
        dialog[chat_id] = True
        bot.send_message(chat_id, "🧠Вы начали диалог с нейросетью. Напишите ваше сообщение:", reply_markup=get_ai_markup())

    elif message.text == '☁️Узнать погоду☁️':
        city = bot.send_message(chat_id, "✍️Введите название города (например, Томск):")
        bot.register_next_step_handler(city, view_weather)

    elif message.text == '🐶Получить фото котика/собачки😸':
        animal_image(chat_id)

    elif message.text == '✌️Получить совет✌️':
        get_random_advice(chat_id)

    elif message.text == '👀Получить GIF👀':
        massege = bot.send_message(chat_id, "✍️Введите тег для поиска GIF (например, cats):")
        bot.register_next_step_handler(massege, send_gif)

    else:
        bot.send_message(chat_id, "❌Пожалуйста, используйте кнопки❌.")

def ai_message(message):
    loading_message = bot.send_message(message.chat.id, "🧐Нейросеть генерирует ответ...")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        )

        response = completion.choices[0].message.content

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=loading_message.message_id,
            text=response
        )
    except RateLimitError:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=loading_message.message_id,
            text="Попытки закончились."
        )

def get_weather(city):
    URL = 'http://api.openweathermap.org/data/2.5/weather'
    try:
        query = requests.get(URL, params={
            'q': city,
            'appid': WEATHER_API,
            'units': 'metric'
        })
        weather_data = query.json()

        response = (
            f"🌆Погода в городе {weather_data['name']}:\n"
            f"⛅Температура: {weather_data['main']['temp']}°C\n"
            f"👌Ощущается как: {weather_data['main']['feels_like']}°C\n"
            f"🌬️Погодные условия: {weather_data['weather'][0]['description']}"
        )
        return response
    except (KeyError, requests.exceptions.HTTPError):
        return "❌Город не найден❌."

def view_weather(message):
    city = message.text
    weather_info = get_weather(city)
    bot.send_message(message.chat.id, weather_info)

def cat_image(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Котика🐱", callback_data="cat_button_clicked"))
    markup.add(telebot.types.InlineKeyboardButton("Собачку🐶", callback_data="dog_button_clicked"))
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    cat_url = response.json()[0]['url']
    bot.send_photo(chat_id, cat_url, reply_markup=markup)

def dog_image(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Котика🐱", callback_data="cat_button_clicked"))
    markup.add(telebot.types.InlineKeyboardButton("Собачку🐶", callback_data="dog_button_clicked"))
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    dog_url = response.json()['message']
    bot.send_photo(chat_id, dog_url, reply_markup=markup)

def animal_image(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Котика🐱", callback_data="cat_button_clicked"))
    markup.add(telebot.types.InlineKeyboardButton("Собачку🐶", callback_data="dog_button_clicked"))
    bot.send_message(chat_id, "Выбирай!👀", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cat_button_clicked":
        cat_image(call.message.chat.id)
    elif call.data == "dog_button_clicked":
        dog_image(call.message.chat.id)

def get_random_advice(chat_id):
    response = requests.get('https://api.adviceslip.com/advice')
    advice_data = response.json()

    advice = advice_data['slip']['advice']

    translated_advice = GoogleTranslator(source='en', target='ru').translate(advice)
    bot.send_message(chat_id, f"🤓{translated_advice}🤓")

def get_random_gif(api_key, tag=None, rating='g'):
    url = 'https://api.giphy.com/v1/gifs/random'
    params = {
        'api_key': api_key,
        'tag': tag,
        'rating': rating
    }
    response = requests.get(url, params=params)
    data = response.json()
    gif_data = data['data']
    gif_info = {
        'url': gif_data['images']['original']['url'],
    }
    return gif_info

def send_gif(message):
    tag = message.text
    gif_info = get_random_gif(API_GIF, tag=tag)
    bot.send_animation(
            message.chat.id,
            gif_info['url'],
            caption=f"👀Случайный GIF по тегу: '{tag}'👀",
            reply_markup=get_markup())

bot.infinity_polling()