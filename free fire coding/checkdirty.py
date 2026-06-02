#!/usr/bin/env python3
"""
FreeFire Dirty Word Checker for Termux
Developer: t.me/danger_ff_like
"""

import os
import time
import requests
import urllib3
from danger_ffjwt import guest_to_jwt
from Crypto.Cipher import AES

# ------------------------------
# Suppress SSL warnings
# ------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------------------
# Configuration (change if needed)
# ------------------------------
UID = "4417073646"
PASSWORD = "DANGERR-LS6WXk-IDS-BY-DANGER_FF_LIKE-IptIfx-pYB8zP"
OB_VERSION = "OB52"
CLIENT_VERSION = "1.120.1"
DEV_TELEGRAM = "t.me/danger_ff_like"

# AES key & IV (from maker.py)
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# ------------------------------
# Protobuf helpers
# ------------------------------
def encode_varint(value: int) -> bytes:
    out = []
    while True:
        b = value & 0x7F
        value >>= 7
        if value:
            out.append(b | 0x80)
        else:
            out.append(b)
            break
    return bytes(out)

def build_payload(name: str, field2: int = 1) -> bytes:
    """Build CheckDirtyWords protobuf payload."""
    name_bytes = name.encode('utf-8')
    payload = b'\x0a' + encode_varint(len(name_bytes)) + name_bytes  # field 1 (string)
    payload += b'\x10' + encode_varint(field2)                       # field 2 (int)
    return payload

def encrypt_packet(plaintext: bytes) -> bytes:
    """AES-128-CBC encrypt with PKCS7 padding."""
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    pad_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad_len]) * pad_len
    return cipher.encrypt(plaintext)

# ------------------------------
# JWT token generation (no cache for simplicity)
# ------------------------------
def get_jwt_token():
    """Generate a fresh JWT token using danger_ffjwt."""
    try:
        jwt_data = guest_to_jwt(UID, PASSWORD,
                                ob_version=OB_VERSION,
                                client_version=CLIENT_VERSION)
        token = jwt_data.get("jwt_token")
        if not token:
            raise Exception("No jwt_token in response")
        return token
    except Exception as e:
        raise Exception(f"Token generation failed: {e}")

# ------------------------------
# Response parser
# ------------------------------
def interpret_response(resp: requests.Response, nickname: str):
    """Convert server response to human-readable message."""
    content = resp.content
    status_code = resp.status_code

    # Try to decode as UTF-8 text
    try:
        text = content.decode('utf-8').strip()
        is_binary = False
    except UnicodeDecodeError:
        text = None
        is_binary = True

    lines = []
    lines.append(f"Nickname: {nickname}")
    lines.append(f"HTTP Status: {status_code}")
    lines.append("-" * 40)

    # Determine result type
    if text and "DIRTY_WORD" in text.upper():
        # Dirty word detected (could be 200 or 400)
        lines.append("❌ RESULT: DIRTY WORDS FOUND")
        lines.append(f"Server message: {text}")
        # No raw hex needed – message is clear
    elif status_code == 200:
        if not is_binary:
            # Clean name
            lines.append("✅ RESULT: NICKNAME IS CLEAN (no dirty words)")
            lines.append(f"Server message: {text if text else '(empty)'}")
        else:
            # Binary response on 200 – unknown
            lines.append("⚠️  RESULT: UNKNOWN (binary response)")
            lines.append(f"Raw hex: {content.hex()}")
    else:
        # Error (non-200) without dirty word
        lines.append("❌ ERROR RESPONSE FROM SERVER")
        if text:
            lines.append(f"Message: {text}")
        # Show raw hex if it's binary OR if we want to see the raw data for debugging
        if is_binary or text:
            lines.append(f"Raw hex: {content.hex()}")
        else:
            # In case text is empty but not binary? Unlikely, but safe
            lines.append(f"Raw hex: {content.hex()}")

    lines.append("-" * 40)
    lines.append(f"Developer: {DEV_TELEGRAM}")
    return "\n".join(lines)

# ------------------------------
# Main
# ------------------------------
def main():
    print("\n🔥 FreeFire Dirty Word Checker 🔥")
    print(f"Developer: {DEV_TELEGRAM}\n")

    # Get nickname from user
    nickname = input("Enter nickname to check: ").strip()
    if not nickname:
        print("❌ No nickname entered. Exiting.")
        return

    print("\n[+] Generating JWT token...")
    try:
        token = get_jwt_token()
        print("[+] Token obtained.")
    except Exception as e:
        print(f"❌ {e}")
        return

    print("[+] Building encrypted payload...")
    plain = build_payload(nickname)
    encrypted = encrypt_packet(plain)
    print(f"[+] Payload encrypted (hex): {encrypted.hex()[:64]}...")  # show first part

    print("[+] Sending request to FreeFire...")
    headers = {
        "Host": "client.ind.freefiremobile.com",
        "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": f"Bearer {token}",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB52",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2022.3.47f1",
    }

    try:
        resp = requests.post(
            "https://client.ind.freefiremobile.com/CheckDirtyWords",
            headers=headers,
            data=encrypted,
            verify=False,
            timeout=10
        )
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return

    # Interpret and print result
    print("\n" + interpret_response(resp, nickname))

if __name__ == "__main__":
    main()