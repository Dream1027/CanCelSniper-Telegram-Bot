import telebot
from telebot import TeleBot, types
import threading
import script

userStep = {}
token = "telegrambotkn"
bot = TeleBot(token)
stop_event = threading.Event()


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    
def start_MainMenu(message):
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    cid = message.chat.id

    keyboard.row(
        telebot.types.InlineKeyboardButton("🎟️Cancel", callback_data="cancel"),
        telebot.types.InlineKeyboardButton("📘Sell Profit", callback_data="profit"),
    )
    bot.send_message(cid, "Please choose an option.", reply_markup=keyboard)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    
    start_MainMenu(message)   


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith("cancel"):
        markup = types.ForceReply(selective=False)
        minuteText = "Please enter the number of minutes:"
        bot.send_message(query.message.chat.id, minuteText, reply_markup=markup)
        userStep[query.message.chat.id] = 1
        # await script.stop()
        # stop_event.set()

    # mainMenu Callback
    elif data.startswith("profit"):
        markup = types.ForceReply(selective=False)
        profitText = "Please enter Sell Profit Percent:"
        bot.send_message(query.message.chat.id, profitText, reply_markup=markup)
        userStep[query.message.chat.id] = 2
        # await script.stop()
        # stop_event.set()

    elif data.startswith('main'): 
       print('Main Menu')      
       start_MainMenu(query.message)


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 1)
def add_cancelMinutes(message):

    minutesText = message.text
    print(minutesText)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("📒Main Menu", callback_data="main"))
    minutesContent = "Cancel set to " + minutesText + " minutes"
    bot.send_message(
        message.chat.id, minutesContent, parse_mode="HTML", reply_markup=keyboard
    )
    script.changeMinutes(60*int(minutesText))


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 2)
def add_profit(message):

    profitText = message.text
    print(profitText)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("📒Main Menu", callback_data="main"))
    profitContent = "Sell Order Limit set to " + profitText + " minutes"
    bot.send_message(
        message.chat.id, profitContent, parse_mode="HTML", reply_markup=keyboard
    )
    
    script.changePercent(profitText)
    
telethon_thread = threading.Thread(target=script.start)
telethon_thread.start()

bot.polling(none_stop=True)
