import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import sqlite3
import random
import string
import time
from datetime import datetime
import threading
import os
import json

# ============= CONFIGURATION =============
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
ADMIN_IDS = [123456789]  # Replace with your Telegram user ID

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Database setup
def init_db():
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  join_date TEXT,
                  last_active TEXT)''')
    
    # Files table
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (file_id TEXT PRIMARY KEY,
                  unique_code TEXT UNIQUE,
                  file_name TEXT,
                  file_size INTEGER,
                  mime_type TEXT,
                  upload_date TEXT,
                  uploaded_by INTEGER)''')
    
    # Force join channels table
    c.execute('''CREATE TABLE IF NOT EXISTS force_channels
                 (channel_id TEXT PRIMARY KEY,
                  channel_username TEXT,
                  added_date TEXT)''')
    
    # Promo buttons table
    c.execute('''CREATE TABLE IF NOT EXISTS promo_buttons
                 (button_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  button_name TEXT,
                  button_url TEXT,
                  added_date TEXT)''')
    
    conn.commit()
    return conn

conn = init_db()

# ============= HELPER FUNCTIONS =============

def generate_unique_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def add_user(user_id, username, first_name):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, username, first_name, join_date, last_active) VALUES (?, ?, ?, ?, ?)",
                      (user_id, username, first_name, str(datetime.now()), str(datetime.now())))
        conn.commit()
    except:
        cursor.execute("UPDATE users SET last_active = ? WHERE user_id = ?", (str(datetime.now()), user_id))
        conn.commit()

def get_force_channels():
    cursor = conn.cursor()
    cursor.execute("SELECT channel_username FROM force_channels")
    return [row[0] for row in cursor.fetchall()]

def get_promo_buttons():
    cursor = conn.cursor()
    cursor.execute("SELECT button_name, button_url FROM promo_buttons")
    return cursor.fetchall()

def get_file_by_code(code):
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, file_name FROM files WHERE unique_code = ?", (code,))
    return cursor.fetchone()

def save_file(file_id, file_name, file_size, mime_type, user_id):
    code = generate_unique_code()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (file_id, unique_code, file_name, file_size, mime_type, upload_date, uploaded_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (file_id, code, file_name, file_size, mime_type, str(datetime.now()), user_id))
    conn.commit()
    return code

def check_force_join(user_id):
    channels = get_force_channels()
    if not channels:
        return True
    
    for channel in channels:
        try:
            channel_username = channel if channel.startswith('@') else f'@{channel}'
            member = bot.get_chat_member(channel_username, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            continue
    return True

def get_force_join_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = get_force_channels()
    
    for channel in channels:
        channel_username = channel if channel.startswith('@') else f'@{channel}'
        keyboard.add(InlineKeyboardButton(f"📢 Join {channel}", url=f"https://t.me/{channel.replace('@', '')}"))
    
    keyboard.add(InlineKeyboardButton("✅ I've Joined", callback_data="verify_join"))
    return keyboard

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Add promo buttons from database
    promo_buttons = get_promo_buttons()
    for name, url in promo_buttons:
        keyboard.add(InlineKeyboardButton(name, url=url))
    
    return keyboard

# ============= ADMIN COMMANDS =============

def is_admin(user_id):
    return user_id in ADMIN_IDS

@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user
    add_user(user.id, user.username, user.first_name)
    
    # Check force join
    if not check_force_join(user.id):
        keyboard = get_force_join_keyboard()
        bot.send_message(message.chat.id, 
                        "🚫 <b>Access Denied!</b>\n\n"
                        "You must join our channel(s) first to use this bot.\n\n"
                        "👇 Click the buttons below to join:",
                        reply_markup=keyboard,
                        parse_mode='HTML')
        return
    
    welcome_text = (f"🎉 <b>Welcome {user.first_name}!</b>\n\n"
                   f"🤖 <b>BBYTOP FILE BOT</b>\n\n"
                   f"✅ You have unlimited access to all files!\n\n"
                   f"📁 <b>How to use:</b>\n"
                   f"• Click on any file link shared in channels\n"
                   f"• Or use direct file codes\n\n"
                   f"📢 <b>Our Channels:</b>\n")
    
    channels = get_force_channels()
    for channel in channels:
        welcome_text += f"• {channel}\n"
    
    keyboard = get_main_keyboard()
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, parse_mode='HTML')

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📤 Upload File", callback_data="admin_upload"),
        InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton("➕ Add Channel", callback_data="admin_add_channel"),
        InlineKeyboardButton("➖ Remove Channel", callback_data="admin_remove_channel"),
        InlineKeyboardButton("📋 List Channels", callback_data="admin_list_channels"),
        InlineKeyboardButton("🔘 Add Promo Button", callback_data="admin_add_promo"),
        InlineKeyboardButton("❌ Remove Promo Button", callback_data="admin_remove_promo"),
        InlineKeyboardButton("📜 Promo Buttons List", callback_data="admin_list_promo")
    )
    
    bot.send_message(message.chat.id, "🔧 <b>Admin Control Panel</b>\n\nSelect an option:", 
                    reply_markup=keyboard, parse_mode='HTML')

# File upload handling
user_upload_states = {}

@bot.callback_query_handler(func=lambda call: call.data == "admin_upload")
def admin_upload_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    bot.send_message(call.message.chat.id, "📤 Send me any file (video, document, photo, text) to upload.\n\nSend /cancel to cancel.")
    user_upload_states[call.from_user.id] = "waiting_file"
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: user_upload_states.get(message.from_user.id) == "waiting_file")
def handle_file_upload(message):
    if not is_admin(message.from_user.id):
        return
    
    if message.text == "/cancel":
        del user_upload_states[message.from_user.id]
        bot.reply_to(message, "❌ Upload cancelled.")
        return
    
    try:
        if message.document:
            file = message.document
            file_id = file.file_id
            file_name = file.file_name
            file_size = file.file_size
            mime_type = file.mime_type
        elif message.video:
            file = message.video
            file_id = file.file_id
            file_name = file.file_name if hasattr(file, 'file_name') else "video.mp4"
            file_size = file.file_size
            mime_type = "video/mp4"
        elif message.photo:
            file = message.photo[-1]
            file_id = file.file_id
            file_name = "photo.jpg"
            file_size = file.file_size
            mime_type = "image/jpeg"
        else:
            bot.reply_to(message, "❌ Unsupported file type. Send document, video, or photo.")
            return
        
        code = save_file(file_id, file_name, file_size, mime_type, message.from_user.id)
        bot_token = BOT_TOKEN
        share_link = f"https://t.me/{bot.get_me().username}?start={code}"
        
        response = (f"✅ <b>File Uploaded Successfully!</b>\n\n"
                   f"📁 <b>File:</b> {file_name}\n"
                   f"📊 <b>Size:</b> {file_size} bytes\n"
                   f"🔗 <b>Share Link:</b>\n<code>{share_link}</code>\n\n"
                   f"🔑 <b>Direct Code:</b> <code>{code}</code>")
        
        bot.reply_to(message, response, parse_mode='HTML')
        del user_upload_states[message.from_user.id]
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error uploading file: {str(e)}")
        del user_upload_states[message.from_user.id]

# Handle file access via start with code
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/start ') and len(message.text) > 7)
def handle_file_access(message):
    user = message.from_user
    add_user(user.id, user.username, user.first_name)
    
    # Check force join
    if not check_force_join(user.id):
        keyboard = get_force_join_keyboard()
        bot.send_message(message.chat.id, 
                        "🚫 <b>Access Denied!</b>\n\nYou must join our channel(s) first.",
                        reply_markup=keyboard,
                        parse_mode='HTML')
        return
    
    code = message.text.split(' ')[1]
    file_data = get_file_by_code(code)
    
    if file_data:
        file_id, file_name = file_data
        try:
            # Send file based on mime type
            cursor = conn.cursor()
            cursor.execute("SELECT mime_type FROM files WHERE unique_code = ?", (code,))
            mime_type = cursor.fetchone()[0]
            
            if mime_type.startswith('image/'):
                bot.send_photo(message.chat.id, file_id, caption=f"📁 {file_name}")
            elif mime_type.startswith('video/'):
                bot.send_video(message.chat.id, file_id, caption=f"📁 {file_name}")
            else:
                bot.send_document(message.chat.id, file_id, caption=f"📁 {file_name}")
        except:
            bot.send_message(message.chat.id, "❌ Error sending file. Please try again.")
    else:
        bot.send_message(message.chat.id, "❌ Invalid or expired file code.")

@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_join_callback(call):
    user_id = call.from_user.id
    
    if check_force_join(user_id):
        bot.edit_message_text("✅ <b>Verification Successful!</b>\n\nYou now have access to all files.",
                             call.message.chat.id, call.message.message_id,
                             parse_mode='HTML')
        
        welcome_text = (f"🎉 <b>Welcome {call.from_user.first_name}!</b>\n\n"
                       f"🤖 <b>BBYTOP FILE BOT</b>\n\n"
                       f"✅ You now have full access!")
        
        keyboard = get_main_keyboard()
        bot.send_message(call.message.chat.id, welcome_text, reply_markup=keyboard, parse_mode='HTML')
    else:
        bot.answer_callback_query(call.id, "❌ You haven't joined all channels yet!", show_alert=True)

# Statistics
@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM files")
    total_files = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM force_channels")
    total_channels = cursor.fetchone()[0]
    
    stats_text = (f"📊 <b>Bot Statistics</b>\n\n"
                 f"👥 <b>Total Users:</b> {total_users}\n"
                 f"📁 <b>Total Files:</b> {total_files}\n"
                 f"📢 <b>Force Channels:</b> {total_channels}\n"
                 f"👑 <b>Admins:</b> {len(ADMIN_IDS)}")
    
    bot.edit_message_text(stats_text, call.message.chat.id, call.message.message_id, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# Channel management
@bot.callback_query_handler(func=lambda call: call.data == "admin_add_channel")
def add_channel_prompt(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    msg = bot.send_message(call.message.chat.id, "Send channel username (e.g., @channelname):\nSend /cancel to cancel.")
    bot.register_next_step_handler(msg, process_add_channel)
    bot.answer_callback_query(call.id)

def process_add_channel(message):
    if not is_admin(message.from_user.id):
        return
    
    if message.text == "/cancel":
        bot.reply_to(message, "❌ Operation cancelled.")
        return
    
    channel = message.text.strip()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO force_channels (channel_id, channel_username, added_date) VALUES (?, ?, ?)",
                      (channel, channel, str(datetime.now())))
        conn.commit()
        bot.reply_to(message, f"✅ Channel {channel} added to force join list!")
    except:
        bot.reply_to(message, f"❌ Channel {channel} already exists!")

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_channel")
def remove_channel_prompt(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    channels = get_force_channels()
    if not channels:
        bot.send_message(call.message.chat.id, "No channels in force join list.")
        bot.answer_callback_query(call.id)
        return
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        keyboard.add(InlineKeyboardButton(f"❌ {channel}", callback_data=f"remove_channel_{channel}"))
    keyboard.add(InlineKeyboardButton("🔙 Back", callback_data="admin_back"))
    
    bot.edit_message_text("Select channel to remove:", call.message.chat.id, 
                         call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_channel_"))
def process_remove_channel(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    channel = call.data.replace("remove_channel_", "")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM force_channels WHERE channel_username = ?", (channel,))
    conn.commit()
    
    bot.answer_callback_query(call.id, f"✅ {channel} removed!")
    bot.edit_message_text(f"✅ Channel {channel} removed!", call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_list_channels")
def list_channels(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    channels = get_force_channels()
    if channels:
        text = "📋 <b>Force Join Channels:</b>\n\n"
        for i, ch in enumerate(channels, 1):
            text += f"{i}. {ch}\n"
    else:
        text = "No channels added yet."
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# Promo button management
@bot.callback_query_handler(func=lambda call: call.data == "admin_add_promo")
def add_promo_prompt(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    msg = bot.send_message(call.message.chat.id, "Send button name and URL in format:\n<code>Button Name|https://t.me/...</code>\n\nSend /cancel to cancel.", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_promo)
    bot.answer_callback_query(call.id)

def process_add_promo(message):
    if not is_admin(message.from_user.id):
        return
    
    if message.text == "/cancel":
        bot.reply_to(message, "❌ Operation cancelled.")
        return
    
    try:
        name, url = message.text.split('|', 1)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO promo_buttons (button_name, button_url, added_date) VALUES (?, ?, ?)",
                      (name.strip(), url.strip(), str(datetime.now())))
        conn.commit()
        bot.reply_to(message, f"✅ Promo button added!\n\nName: {name}\nURL: {url}")
    except:
        bot.reply_to(message, "❌ Invalid format! Use: Button Name|URL")

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_promo")
def remove_promo_prompt(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    buttons = get_promo_buttons()
    if not buttons:
        bot.send_message(call.message.chat.id, "No promo buttons available.")
        bot.answer_callback_query(call.id)
        return
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    for name, url in buttons:
        keyboard.add(InlineKeyboardButton(f"❌ {name}", callback_data=f"remove_promo_{name}"))
    keyboard.add(InlineKeyboardButton("🔙 Back", callback_data="admin_back"))
    
    bot.edit_message_text("Select promo button to remove:", call.message.chat.id,
                         call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_promo_"))
def process_remove_promo(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    name = call.data.replace("remove_promo_", "")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM promo_buttons WHERE button_name = ?", (name,))
    conn.commit()
    
    bot.answer_callback_query(call.id, f"✅ {name} removed!")
    bot.edit_message_text(f"✅ Promo button '{name}' removed!", call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_list_promo")
def list_promo(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    buttons = get_promo_buttons()
    if buttons:
        text = "🔘 <b>Promo Buttons:</b>\n\n"
        for i, (name, url) in enumerate(buttons, 1):
            text += f"{i}. {name}\n   URL: {url}\n\n"
    else:
        text = "No promo buttons added yet."
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# Broadcast
@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def broadcast_prompt(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Unauthorized!", show_alert=True)
        return
    
    msg = bot.send_message(call.message.chat.id, "📢 Send message to broadcast to all users.\n\nSend /cancel to cancel.")
    bot.register_next_step_handler(msg, process_broadcast)
    bot.answer_callback_query(call.id)

def process_broadcast(message):
    if not is_admin(message.from_user.id):
        return
    
    if message.text == "/cancel":
        bot.reply_to(message, "❌ Broadcast cancelled.")
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    success = 0
    fail = 0
    
    status_msg = bot.reply_to(message, "📡 Broadcasting message...")
    
    for user in users:
        try:
            bot.send_message(user[0], message.text)
            success += 1
            time.sleep(0.1)
        except:
            fail += 1
    
    bot.edit_message_text(f"✅ Broadcast completed!\n\nSuccess: {success}\nFailed: {fail}", 
                         status_msg.chat.id, status_msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_back")
def admin_back(call):
    admin_panel(call.message)

# ============= RUN BOT =============
if __name__ == "__main__":
    print("🤖 BBYTOP FILES BOT Started!")
    print(f"✅ Bot username: @{bot.get_me().username}")
    print(f"👑 Admins: {ADMIN_IDS}")
    print("🚀 Bot is running...")
    
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Error: {e}")
        bot.stop_polling()