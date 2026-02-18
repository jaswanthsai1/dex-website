
import hmac
import hashlib
import requests
import string
import random
import json
import codecs
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import urllib3
import base64

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- CONSTANTS ---------------- #
HEX_KEY = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
KEY = bytes.fromhex(HEX_KEY)

# Session Helper
def get_session():
    session = requests.Session()
    # Basic retry adapter
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    retry = Retry(total=2, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# ---------------- PROTOBUF ENCODING (For MajorRegister) ---------------- #
def EnC_Vr(N):
    N = int(N)
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))
    return packet

# ---------------- ENCRYPTION ---------------- #
def E_AEs(Pc):
    Z = bytes.fromhex(Pc)
    key_bytes = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    K = AES.new(key_bytes, AES.MODE_CBC, iv)
    R = K.encrypt(pad(Z, AES.block_size))
    return bytes.fromhex(R.hex())

# ---------------- GENERATORS ---------------- #
def generate_random_name(name_prefix):
    characters = string.ascii_letters + string.digits
    return name_prefix + ''.join(random.choice(characters) for _ in range(6)).upper()

def generate_custom_password():
    characters = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(characters) for _ in range(9)).upper()
    return f"DANGER-{random_part}-CORE"

# ---------------- ENCODING HELPERS ---------------- #
def encode_string(original):
    keystream = [
        0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,
        0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
        0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,
        0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30
    ]
    encoded = ""
    for i in range(len(original)):
        orig_byte = ord(original[i])
        key_byte = keystream[i % len(keystream)]
        result_byte = orig_byte ^ key_byte
        encoded += chr(result_byte)
    return {"open_id": original, "field_14": encoded}

def to_unicode_escaped(s):
    return ''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in s)

# ---------------- MAJOR REGISTER ---------------- #
def Major_Regsiter(access_token, open_id, field, uid, password, region, name_prefix):
    # Step 3: Major Register
    session = get_session()
    url = "https://loginbp.ggblueshark.com/MajorRegister"
    internal_name = generate_random_name(name_prefix)

    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "Host": "loginbp.ggblueshark.com",
        "ReleaseVersion": "OB51",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1"
    }

    payload = {
        1: internal_name,
        2: access_token,
        3: open_id,
        5: 102000007,
        6: 4,
        7: 1,
        13: 1,
        14: field,
        15: "en",
        16: 1,
        17: 1
    }

    try:
        payload_hex = CrEaTe_ProTo(payload).hex()
        payload_enc = E_AEs(payload_hex).hex()
        body = bytes.fromhex(payload_enc)
        response = session.post(url, headers=headers, data=body, verify=False, timeout=30)
        
        # If successful (usually 200), we return the credentials
        # We DON'T do the login here. Token Manager will do it.
        if response.status_code == 200 and len(response.text) > 10:
             return {
                "uid": uid,
                "password": password,
                "region": region,
                "status": "registered"
             }
        return None
    except Exception as e:
        print(f"MajorRegister failed: {e}")
        return None

# ---------------- TOKEN GRANT ---------------- #
def token(uid, password, region, name_prefix):
    # Step 2: Token Grant
    session = get_session()
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
    }

    body = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": KEY,
        "client_id": "100067"
    }

    try:
        response = session.post(url, headers=headers, data=body, timeout=30)
        resp_json = response.json()
        open_id = resp_json.get('open_id')
        access_token = resp_json.get("access_token")

        if not open_id or not access_token:
            return None

        result = encode_string(open_id)
        field = to_unicode_escaped(result['field_14'])
        field = codecs.decode(field, 'unicode_escape').encode('latin1')

        return Major_Regsiter(access_token, open_id, field, uid, password, region, name_prefix)
    except Exception as e:
        print(f"Token Grant failed: {e}")
        return None

# ---------------- MAIN ENTRY POINT ---------------- #
def generate_guest_account(region="IND", name_prefix="BOT"):
    """
    Generates a new Guest Account.
    Returns: {"uid": "...", "password": "...", "region": "...", "status": "registered"} or None
    """
    password = generate_custom_password()
    session = get_session()
    
    # Step 1: Guest Register
    # Construct data string for HMAC
    data = f"password={password}&client_type=2&source=2&app_id=100067"
    message = data.encode('utf-8')
    signature = hmac.new(KEY, message, hashlib.sha256).hexdigest()

    url = "https://100067.connect.garena.com/oauth/guest/register"
    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
        "Authorization": "Signature " + signature,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    try:
        response = session.post(url, headers=headers, data=data, timeout=30)
        resp_json = response.json()
        uid = resp_json.get('uid')
        if not uid:
            print(f"Guest Register failed: {resp_json}")
            return None
        
        # Proceed to Step 2
        return token(uid, password, region, name_prefix)
        
    except Exception as e:
        print(f"Guest Register exception: {e}")
        return None

# Test Block
if __name__ == "__main__":
    print("Generating guest account...")
    res = generate_guest_account()
    print("Result:", res)
