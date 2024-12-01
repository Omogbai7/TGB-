import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from time import sleep
import sqlite3
import threading
import itertools

BOT_TOKEN = "7337227185:AAEYRhSSFLZyBi39BjgNeoF6fN21qNuzHrY"
bot = telebot.TeleBot(BOT_TOKEN)

DEFAULT_BALANCE = 500
REFERRAL_REWARD = 500
WELCOME_IMAGE_PATH = "monitoken.jpg"
CHANNEL_LINK = "https://t.me/earnmoneytokenupdatesandmore"
FOLLOW_X = "https://x.com/moneytoken123"
YOUTUBE_LINK = "https://youtube.com/@moneytoken123"

def initialize_database():
    connection = sqlite3.connect("referral_system.db")
    cursor = connection.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referrer_id INTEGER,
            balance INTEGER DEFAULT 0
        )
    """)
    connection.commit()
    connection.close()

initialize_database()

def add_user(user_id, referrer_id=None):
    connection = sqlite3.connect("referral_system.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id, referrer_id, balance) VALUES (?, ?, ?)",
                       (user_id, referrer_id, DEFAULT_BALANCE))
        if referrer_id:
            cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",
                           (REFERRAL_REWARD, referrer_id))
            connection.commit()
            bot.send_message(referrer_id, f"🎉 500 tokens have been added to your balance as a referral reward!")
    connection.commit()
    connection.close()

def get_user_balance(user_id):
    connection = sqlite3.connect("referral_system.db")
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()
    connection.close()
    return balance[0] if balance else 0

def send_main_menu(chat_id, message_id):
    main_menu = InlineKeyboardMarkup(row_width=1)
    main_menu.add(
        InlineKeyboardButton("Check Balance", callback_data="check_balance"),
        InlineKeyboardButton("Referral Links", callback_data="referral_link"),
        InlineKeyboardButton("Submit X Username + 500 Tokens", callback_data="submit_x_username"),
        InlineKeyboardButton("Join Channel + 500 Tokens", callback_data="join_channel"),
        InlineKeyboardButton("Follow X + 500 Tokens", callback_data="follow_x"),
        InlineKeyboardButton("Subscribe YouTube + 500 Tokens", callback_data="subscribe_youtube"),
        InlineKeyboardButton("Enter Polygon Address + 500 Tokens", callback_data="polygon_address"),
        InlineKeyboardButton("Road Map", callback_data="road_map"),
        InlineKeyboardButton("Terms and Conditions", callback_data="terms")
    )
    bot.edit_message_text("Welcome back to the main menu. What would you like to do?", chat_id, message_id, reply_markup=main_menu)

def animate_spinner(chat_id, message_id):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    for _ in range(30):
        current_spin = next(spinner)
        bot.edit_message_text(f"Please wait, verifying your subscription {current_spin}", chat_id, message_id)
        sleep(1)
    update_user_balance(chat_id, 500)
    bot.edit_message_text("✅ You have successfully earned 500 $MONEY for subscribing!", chat_id, message_id)

    back_to_menu_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")
    )
    bot.edit_message_text(
        "✅ You have successfully earned 500 $MONEY for subscribing!\n\nClick below to return to the main menu.",
        chat_id,
        message_id,
        reply_markup=back_to_menu_button
    )

def update_user_balance(user_id, amount):
    connection = sqlite3.connect("referral_system.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    connection.commit()
    connection.close()

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    args = message.text.split()

    referrer_id = None
    if len(args) > 1 and args[1].isdigit():
        referrer_id = int(args[1])

    add_user(chat_id, referrer_id)

    welcome_message = (
        f"🚀 Welcome {message.from_user.username} to $Money on Polygon.\n\n"
        "Let's repeat the history of Pepe on Binance Chain where it grew 700X.\n"
        "Here on Polygon Chain, we are targeting 1000X potential growth.\n\n"
        "🚀 Complete the airdrop task & get 500 $MONEY on Polygon.\n"
        "🚀 Earn 500 $MONEY on Polygon for each free referral.\n"
        "🚀 Complete different tasks & get 500 $MONEY on Polygon.\n"
        "🚀 Click on the verify button after completing tasks so that tokens will be added to your balance."
    )

    try:
        with open(WELCOME_IMAGE_PATH, 'rb') as image:
            bot.send_photo(chat_id, photo=image, caption=welcome_message)
    except FileNotFoundError:
        bot.send_message(chat_id, welcome_message)

    msg = bot.send_message(chat_id, "Main Menu: Select an option below:")
    send_main_menu(chat_id, msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "check_balance":
        balance = get_user_balance(chat_id)
        bot.edit_message_text(
            f"Your balance is {balance} $MONEY on Polygon.\n\n",
            chat_id,
            message_id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")
            )
        )
    elif call.data == "referral_link":
        referral_link = f"https://t.me/MomeyAirdropBot?start={chat_id}"
        bot.edit_message_text(
            "🎉 Here's your referral link to invite new people & earn 500 $MONEY on Polygon for each referral! \n\n"
            "🔗 Share this link to refer others: \n"
            f"{referral_link}\n\n"
            "Click below to return to the main menu.",
            chat_id,
            call.message.message_id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")
            )
        )
    elif call.data == "join_channel":
        bot.edit_message_text(
            f"🔗 Please click [here]({CHANNEL_LINK}) to join our Telegram channel and earn 500 $MONEY on Polygon!\n\n"
            "After you join, come back and click 'Verify' to earn 500 tokens!",
            chat_id,
            message_id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Verify", callback_data="verify_channel"),
                InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")
            ),
            parse_mode="Markdown"
        )
    elif call.data == "verify_channel":
        threading.Thread(target=animate_spinner, args=(chat_id, message_id)).start()
    elif call.data == "follow_x":
        bot.edit_message_text(
            f"🔗 Click [here]({FOLLOW_X}) to follow us and earn 500 $MONEY.\n\n"
            "After following, click 'Verify' to claim your tokens.",
            chat_id,
            message_id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Verify", callback_data="verify_follow"),
                InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")
            ),
            parse_mode="Markdown"
        )
    elif call.data == "verify_follow":
        threading.Thread(target=animate_spinner, args=(chat_id, message_id)).start()
    elif call.data == "subscribe_youtube":
        bot.edit_message_text(
            f"🔗 Please click [here]({YOUTUBE_LINK}) to subscribe to our YouTube channel and earn 500 $MONEY on Polygon!\n\n"
            "After subscribing, come back and click 'Verify' to claim your tokens.",
            chat_id,
            message_id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Verify", callback_data="verify_youtube"),
                InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")
            ),
            parse_mode="Markdown"
        )
    elif call.data == "verify_youtube":
        threading.Thread(target=animate_spinner, args=(chat_id, message_id)).start()
    elif call.data == "main_menu":
        send_main_menu(chat_id, message_id)
        
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling()
