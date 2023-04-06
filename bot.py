import telebot
from db_connect1 import DataBaseWork


api_token = '1618675109:AAFwJaMeNM7TJvg49DJbEMMQN1OA_8YHmpM'
bot = telebot.TeleBot(api_token)

if not DataBaseWork.check_db():
    DataBaseWork.start_db()


# user_id = 736460899
# user = DataBaseWork.get_user(user_id)
# if user is None:
#     user = DataBaseWork.create_user(user_id, "name")


# DataBaseWork.create_room(user.id, 'test_room')
#
# rooms = DataBaseWork.get_all_rooms_user(user_id)
# print(rooms)
# print(rooms[0].title)

@bot.message_handler(commands=['start'])
def get_user(message):
    user_id = message.chat.id
    user = DataBaseWork.get_user(user_id)
    if user is None:
        user = DataBaseWork.create_user(user_id, message.chat.first_name)
    bot.send_message(message.chat.id, text='Hello, {name}'.format(name=user.name))


@bot.message_handler(commands=['rooms'])
def get_rooms(message):
    user_id = message.chat.id
    rooms = DataBaseWork.get_all_rooms_user(user_id)
    rooms = [room.title for room in rooms]
    text = "rooms: " + ', '.join(rooms)
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['create_room'])
def create_room(message):
    user_id = message.chat.id
    user = DataBaseWork.get_user(user_id)
    if user is None:
        get_user(message)
        user = DataBaseWork.get_user(user_id)
    room = DataBaseWork.create_room(user.id, 'test_room')
    bot.send_message(message.chat.id, text=room.title)

bot.polling(none_stop=True)
