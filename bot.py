import telebot
from db_connect1 import DataBaseWork


api_token = '1618675109:AAFwJaMeNM7TJvg49DJbEMMQN1OA_8YHmpM'
bot = telebot.TeleBot(api_token)

if not DataBaseWork.check_db():
    DataBaseWork.start_db()


user_id = 736460899
user = DataBaseWork.get_user(user_id)
if user is None:
    user = DataBaseWork.create_user(user_id, "name")

rooms = DataBaseWork.get_all_rooms_user(user_id)
print(rooms)

# @bot.message_handler(commands=['start'])
# def get_weather(message):
#     user_id = message.chat.id
#     user = DataBaseWork.get_user(user_id)
#     if user is None:
#         user = DataBaseWork.create_user(user_id, message.chat.first_name)
#     bot.send_message(message.chat.id, text='Hello, {name}'.format(name=user.name))
#
#
# @bot.message_handler(commands=['rooms'])
# def get_weather(message):
#     bot.send_message(message.chat.id, "hello")
#
#
# bot.polling(none_stop=True)
