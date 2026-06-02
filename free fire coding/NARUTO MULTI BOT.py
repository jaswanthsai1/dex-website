import telebot
import requests
import json
import os
import random
import string
import sys  # Bot stop karne ke liye
from telebot import types

# --- CONFIGURATION & SECURITY CHECK ---
# Yahan apni ID dalo
OWNER_ID = 7668569080 
API_TOKEN = 'BOT TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# --- SECURITY HANDLER ---
# Ye check karega ki script chalane wala asli owner hai ya nahi
try:
    me = bot.get_me()
    print(f"Checking Security for: @{me.username}")
    
    # Agar kisi ne OWNER_ID badli, toh bot nahi chalega
    if OWNER_ID != 7668569080:
        print("❌ SECURITY ALERT: Admin ID Mismatch! Bot is stopping...")
        sys.exit() # Script ko stop kar dega
    else:
        print("✅ Security Verified: Welcome NARUTO CODEX")
except Exception as e:
    print(f"❌ Error starting bot: {e}")
    sys.exit()

# --- CHANNELS & DATA ---
CHANNELS = ["narutocodex7", "narutocodex8"]
DATA_FILE = 'bot_data.json'
user_steps = {}

EMOTES = {
    "P90": "909049010", "M60": "909051003", "MP5": "909033002", "GROZA": "909041005",
    "THOMPSON EVO": "909038010", "M10 RED": "909039011", "MP40 BLUE": "909040010",
    "M10 GREEN": "909000081", "XM8": "909000085", "AK": "909000063", "MP40": "909000075",
    "M4A1": "909033001", "FAMAS": "909000090", "SCAR": "909000068", "UMP": "909000098",
    "M18": "909035007", "FIST": "909037011", "G18": "909038012", "AN94": "909035012",
    "WOODPECKER": "909042008", "THRONE": "909000014", "PIRATE": "909000034", "LOL": "909000002"
}

# --- DATABASE HELPERS ---
def load_data():
    if not os.path.exists(DATA_FILE): return {"users": {}, "codes": {}}
    try:
        with open(DATA_FILE, 'r') as f:
            d = json.load(f)
            if 'users' not in d: d['users'] = {}
            if 'codes' not in d: d['codes'] = {}
            return d
    except: return {"users": {}, "codes": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=4)

# --- KEYBOARDS ---
def main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = ["🔍FF INFO", "PROFILE VISIT", "JWT & ACCESS TOKEN", "FF EMOTE", "GUEST GEN", "REFER", "🎁REDEEM", "OWNER ☠️"]
    markup.add(*(types.KeyboardButton(b) for b in btns))
    if user_id == OWNER_ID: markup.add(types.KeyboardButton("ADMIN PANNEL"))
    return markup

def admin_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📢 BROADCAST", callback_data="adm_bc"),
        types.InlineKeyboardButton("➕ GEN REDEEM", callback_data="adm_gen"),
        types.InlineKeyboardButton("📊 STATUS", callback_data="adm_stat")
    )
    return markup

def server_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    btns = [types.InlineKeyboardButton(r, callback_data=f"srv_{r.lower()}") for r in ["IND", "BR", "US", "ID", "ME", "PK"]]
    return markup.add(*btns)

# --- API RUNNER ---
def run_api(chat_id, user_id, url):
    data = load_data()
    uid = str(user_id)
    if data['users'].get(uid, {}).get('coins', 0) < 1:
        bot.send_message(chat_id, "<b>❌ Coins khatam!</b>", parse_mode="HTML")
        return
    wait = bot.send_message(chat_id, "<b>⏳ Processing JSON Data...</b>", parse_mode="HTML")
    try:
        res = requests.get(url, timeout=100)
        data['users'][uid]['coins'] -= 1
        save_data(data)
        try:
            json_resp = json.dumps(res.json(), indent=4)
        except:
            json_resp = res.text[:1000]
        bot.edit_message_text(f"✅ <b>Success!</b>\n\n<pre>{json_resp}</pre>", chat_id, wait.message_id, parse_mode="HTML")
    except: bot.edit_message_text("❌ API Timeout!", chat_id, wait.message_id)

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(m):
    uid, data = str(m.from_user.id), load_data()
    if uid not in data['users']:
        data['users'][uid] = {"coins": 20}
        save_data(data)
    bot.send_message(m.chat.id, "<b>Security Verified. Naruto Bot Active!</b>", reply_markup=main_keyboard(m.from_user.id), parse_mode="HTML")

@bot.message_handler(func=lambda m: True)
def handle_menu(m):
    uid = str(m.from_user.id)
    
    if m.text in ["🔍FF INFO", "PROFILE VISIT"]:
        user_steps[uid] = {'action': m.text}
        msg = bot.send_message(m.chat.id, "<b>Enter Player UID:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, get_uid_for_srv)
    
    elif m.text == "JWT & ACCESS TOKEN":
        user_steps[uid] = {}
        msg = bot.send_message(m.chat.id, "<b>Enter Guest UID:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, jwt_step_2)
    
    elif m.text == "FF EMOTE":
        user_steps[uid] = {}
        msg = bot.send_message(m.chat.id, "<b>Enter Player UID:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, emote_step_2)
    
    elif m.text == "GUEST GEN":
        user_steps[uid] = {}
        msg = bot.send_message(m.chat.id, "<b>Enter Name:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, guest_step_2)
    
    elif m.text == "REFER":
        bot.send_message(m.chat.id, f"🔗 <b>Refer Link:</b>\nhttps://t.me/{(bot.get_me().username)}?start={uid}", parse_mode="HTML")
    
    elif m.text == "🎁REDEEM":
        msg = bot.send_message(m.chat.id, "<b>Enter Redeem Code:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_redeem)
        
    elif m.text == "OWNER ☠️":
        bot.send_message(m.chat.id, "<b>OWNER - @narutocodex9</b>", parse_mode="HTML")
        
    elif m.text == "ADMIN PANNEL" and int(uid) == OWNER_ID:
        bot.send_message(m.chat.id, "<b>Admin Panel:</b>", reply_markup=admin_inline(), parse_mode="HTML")

# --- FLOW LOGIC ---
def get_uid_for_srv(m):
    user_steps[str(m.from_user.id)]['p_uid'] = m.text
    bot.send_message(m.chat.id, "<b>Select Server:</b>", reply_markup=server_keyboard(), parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: c.data.startswith("srv_"))
def finalize_srv(c):
    uid = str(c.from_user.id)
    if uid in user_steps:
        s, p, a = c.data.split('_')[1], user_steps[uid]['p_uid'], user_steps[uid]['action']
        url = f"https://free-fire-api--tsandesh756.replit.app/get_player_personal_show?server={s}&uid={p}" if a == "🔍FF INFO" else f"https://egvisitapi.vercel.app/{s}/{p}"
        run_api(c.message.chat.id, c.from_user.id, url)

def jwt_step_2(m):
    user_steps[str(m.from_user.id)]['guid'] = m.text
    msg = bot.send_message(m.chat.id, "<b>Enter Password:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, jwt_final)

def jwt_final(m):
    uid = str(m.from_user.id)
    url = f"https://end-jwt-api.vercel.app/token?uid={user_steps[uid]['guid']}&password={m.text}"
    run_api(m.chat.id, m.from_user.id, url)

def emote_step_2(m):
    user_steps[str(m.from_user.id)]['p_uid'] = m.text
    msg = bot.send_message(m.chat.id, "<b>Enter Team Code:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, emote_step_3)

def emote_step_3(m):
    user_steps[str(m.from_user.id)]['tc'] = m.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(name, callback_data=f"em_{id}") for name, id in EMOTES.items()]
    bot.send_message(m.chat.id, "<b>Select Emote:</b>", reply_markup=markup.add(*btns), parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: c.data.startswith("em_"))
def finalize_emote(c):
    uid = str(c.from_user.id)
    if uid in user_steps:
        eid = c.data.split('_')[1]
        url = f"http://fi10.bot-hosting.net:21505/join?tc={user_steps[uid]['tc']}&uid1={user_steps[uid]['p_uid']}&emote_id={eid}"
        run_api(c.message.chat.id, c.from_user.id, url)

def guest_step_2(m):
    user_steps[str(m.from_user.id)]['name'] = m.text
    msg = bot.send_message(m.chat.id, "<b>How many accounts?</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, guest_step_3)

def guest_step_3(m):
    user_steps[str(m.from_user.id)]['count'] = m.text
    markup = types.InlineKeyboardMarkup(row_width=3)
    btns = [types.InlineKeyboardButton(r, callback_data=f"greg_{r}") for r in ["IND", "BR", "US", "ID"]]
    bot.send_message(m.chat.id, "<b>Select Region:</b>", reply_markup=markup.add(*btns), parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: c.data.startswith("greg_"))
def finalize_guest(c):
    uid = str(c.from_user.id)
    reg = c.data.split('_')[1]
    url = f"https://star-guest.vercel.app/gen?name={user_steps[uid]['name']}&count={user_steps[uid]['count']}&region={reg}"
    run_api(c.message.chat.id, c.from_user.id, url)

def process_redeem(m):
    data = load_data()
    code = m.text.strip()
    if code in data['codes']:
        val = data['codes'][code]
        data['users'][str(m.from_user.id)]['coins'] += val
        del data['codes'][code]
        save_data(data)
        bot.send_message(m.chat.id, f"✅ <b>Redeemed! {val} coins added.</b>", parse_mode="HTML")
    else: bot.send_message(m.chat.id, "❌ <b>Invalid Redeem!</b>", parse_mode="HTML")

# --- ADMIN PANEL LOGIC ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("adm_"))
def admin_callbacks(c):
    if c.data == "adm_bc":
        msg = bot.send_message(c.message.chat.id, "<b>Enter Message:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, finalize_bc)
    elif c.data == "adm_gen":
        msg = bot.send_message(c.message.chat.id, "<b>Coins amount:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, finalize_gen_code)
    elif c.data == "adm_stat":
        data = load_data()
        bot.send_message(c.message.chat.id, f"📊 <b>Stats:</b> Users: {len(data['users'])}", parse_mode="HTML")

def finalize_gen_code(m):
    val = int(m.text)
    code = "NARUTO-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    data = load_data()
    data['codes'][code] = val
    save_data(data)
    bot.send_message(m.chat.id, f"✅ <b>Code:</b> <code>{code}</code>", parse_mode="HTML")

def finalize_bc(m):
    data = load_data()
    for u in data['users']:
        try: bot.send_message(u, f"📢 <b>ADMIN:</b> {m.text}", parse_mode="HTML")
        except: pass
    bot.send_message(m.chat.id, "✅ Done!")

if __name__ == "__main__":
    import time
    while True:
        try: bot.polling(none_stop=True, interval=0, timeout=20)
        except: time.sleep(5)
        