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
    cache


@bot.message_handler(commands=['rooms'])
def get_rooms(message):
    user_id = message.chat.id
    rooms = DataBaseWork.get_all_rooms_user(user_id)
    markup = telebot.types.InlineKeyboardMarkup()
    for room in rooms:
        markup.add(telebot.types.InlineKeyboardButton(text=room.title, callback_data=f"check_in_{str(room.id)}"))
    bot.send_message(message.chat.id, text="Выбрать одну из комнат:", reply_markup=markup)


@bot.message_handler(commands=['create_room'])
def pre_create_room(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data="cancel"))
    msg = bot.send_message(message.chat.id, text="Введите имя для новой комнаты", reply_markup=markup)
    bot.register_next_step_handler(msg, create_room)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    if call.data == 'cancel':
        bot.send_message(call.message.chat.id, "отмена")
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data.startswith('check_in_'):
        room_id = call.data.split('check_in_')[-1]
        bot.send_message(call.message.chat.id, room_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)


def create_room(message):
    user_id = message.chat.id
    user = DataBaseWork.get_user(user_id)
    if user is None:
        get_user(message)
        user = DataBaseWork.get_user(user_id)
    room = DataBaseWork.create_room(user.id, message.text)
    bot.send_message(message.chat.id, text="Комната {} создана".format(room.title))

bot.polling(none_stop=True)
