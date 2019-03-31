from app.giphy import gif
import random
from datetime import datetime
import telebot
from telebot import apihelper
import requests

token = '566972231:AAE8g1vVuxhbvrrWLEv5WJgWfDJy329wBmc'

# I use proxy because in Russia Telegram is forbidden
apihelper.proxy = {'https': '200.255.122.174:8080'}

# data for deals
data = dict()

#for game geo
countries = []
capitals = []

#api geo
geo_dict = requests.get('https://restcountries.eu/rest/v2/all').json()
bot = telebot.TeleBot(token)


#storage for list
def storage(new_user, deal):
    try:
        if data.get(new_user) is None:
            data[new_user] = [deal]
        else:
            data[new_user].append(deal)
    except:
        pass


# add task
@bot.message_handler(commands=['add'])
def start_add(message):
    try:
        deal = message.text.replace('/add ', '')
        storage(message.from_user.id, deal)
        bot.send_message(message.chat.id, text='Saved')
    except:
        bot.send_message(message.chat.id, text='Example: /add make a cake🍰')


# show to-do list
@bot.message_handler(commands=['list'])
def get_list(message):
    try:
        deals = data[message.from_user.id]

        for deal in deals:
            bot.send_message(message.chat.id, deal)
    except:
        bot.send_message(message.chat.id, text='In the beginning /add что-нибудь\n'
                                               'Example: /add make a cake🍰')


# delete to-do list
@bot.message_handler(commands=['reset'])
def reset(message):
    try:
        if message.from_user.id in data.keys():
            del data[message.from_user.id]
            bot.send_message(message.chat.id, text='Deleted✅')
        else:
            bot.send_message(message.chat.id, text='list is empty🌚')
    except:
        bot.send_message(message.chat.id, text="/reset: error🌚")


# send text to admin
@bot.message_handler(commands=['send'])
def send_list_to_andrei(message):
    try:
        deals = data[message.from_user.id]
        bot.send_message(266695507, text='to-do list from client')
        for deal in deals:
            bot.send_message(266695507, text='{}'.format(deal))
    except:
        bot.send_message(message.chat.id, text='In the beginning /add что-нибудь\n'
                                               'Example: /add make a cake🍰')


# get gif
@bot.message_handler(commands=['gif'])
def send_gif(message):
    try:
        tag = message.text.replace('/gif ', '')
        url_gif = gif(tag)
        if url_gif is None:
            bot.send_message(message.chat.id, text="I can't find gif with this tag🌚")
        else:
            bot.send_video(message.chat.id, url_gif)
    except:
        bot.send_message(message.chat.id, text="/gif: error🌚")


#cache for countries
def storage_geo():
    try:
        del countries[:]
        del capitals[:]
        for i in range(5):
            rand_geo = random.randint(0, len(geo_dict) - 1)
            countries.append(geo_dict[rand_geo]['name'])
            capitals.append(geo_dict[rand_geo]['capital'])
    except:
        pass


# start play game
@bot.message_handler(commands=['startgeo'])
def start_geo(message):
    try:
        storage_geo()
        bot.send_message(message.chat.id, text="Guess the capital")
        for country in countries:
            bot.send_message(message.chat.id, text=country)
        bot.send_message(message.chat.id, text="Example of answer: /answer London Moscow Berlin ...\n"
                                               "You can answer not all of capitals")

    except:
        bot.send_message(message.chat.id, text="/startgeo: error🌚")


# answers for game
@bot.message_handler(commands=['answer'])
def answer_geo(message):
    try:
        result = 0

        if len(capitals) == 0:
            bot.send_message(message.chat.id, text="Start game🏁 /startgeo")
            return 0

        answers = message.text.replace('/answer ', '').split()
        len_answers = len(answers)
        if len_answers > 5:
            len_answers = 5
        for i in range(len_answers):
            if answers[i] in capitals:
                result += 1

        bot.send_message(message.chat.id, text="Right answer:")
        for capital in capitals:
            bot.send_message(message.chat.id, text=capital)
        if result == 5:
            bot.send_message(message.chat.id, text="Good job, result {}:5".format(result))
        bot.send_message(message.chat.id, text="result {}:5\n"
                                               "try again?🤔 /startgeo".format(result))
        del capitals[:]

    except:
        bot.send_message(message.chat.id, text="/answer: error")
        del capitals[:]
        bot.send_message(message.chat.id, text="Try again /startgeo")


# feedback
@bot.message_handler(commands=['feedback'])
def feedback(message):
    try:
        bot.send_message(266695507, text=message.text)
        bot.send_message(message.chat.id, text="feedback sent")
    except:
        bot.send_message(message.chat.id, text="/feedback: error")


# show functions of bot
@bot.message_handler(commands=['help'])
def help(message):
    try:
        bot.send_message(message.chat.id, text="Gifs:\n"
                                               "\t/gif {tag} - \n\t example: /gif cat\n"
                                               "\t/gif -  random gif\n\n"
                                               "Game: guess the capital 🇩🇰🇨🇦🇮🇪\n"
                                               "\t/startgeo - start game\n"
                                               "\t/answer - London Moscow ... - your answers\n\n"
                                               "to-do list🏝🍪💰:\n"
                                               "\t/add {task} - \n\t example: /add don't forget buy a car\n"
                                               "\t/list - show to-do list\n"
                                               "\t/reset - delete to-do list\n"
                                               "\t/send - send admin your to-do list (I don't know why)\n\n"
                                               "/feedback {text} - give us authors your feedback💬\n"
                                               "/help show all functions🔎")
    except:
        bot.send_message(message.chat.id, text="/help: error")


# hello function
@bot.message_handler()
def handle_message(message):
    try:
        hour = datetime.now().hour
        if 12 > hour >= 4:
            time_compliment = 'Good morning'
        elif 18 > hour >= 12:
            time_compliment = 'Good afternoon'
        elif 23 >= hour >= 18:
            time_compliment = 'Good evening'
        else:
            time_compliment = 'It is time to sleep'

        bot.send_message(message.chat.id, text="{}".format(time_compliment))
        message.text = 'cat'
        send_gif(message)
        bot.send_message(message.chat.id, text="/help show all functions")

    except:
        bot.send_message(message.chat.id, text="/main: error")


bot.polling()
