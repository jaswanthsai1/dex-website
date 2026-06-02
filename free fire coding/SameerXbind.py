#!/usr/bin/env python3
"""
S A M E E R  B I N D  M A N A G E R
PREMIUM HDR EDITION - HIGH-SPEED API INTERFACE
"""

import os
import sys
import time
import json
import re
import requests
import hashlib
from urllib.parse import urlparse, parse_qs

# --------------------------- CONFIGURATION ---------------------------
_BASE_URL = "https://sameer-rishu-13p9.vercel.app/api"
_APP_ID = "100067"

# --------------------------- HDR PREMIUM COLORS ---------------------------
class Colors:
    GOLD = '\033[38;5;220m'
    CYAN = '\033[38;5;51m'
    MAGENTA = '\033[38;5;201m'
    GREEN = '\033[38;5;46m'
    RED = '\033[38;5;196m'
    WHITE = '\033[38;5;255m'
    VIOLET = '\033[38;5;129m'
    BLUE = '\033[38;5;27m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    HDR_GLOW = '\033[1;96m'

# --------------------------- PREMIUM UI ---------------------------
def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    clear()
    # SAMEER Logo in HDR Cyan/Gold
    print(f"{Colors.GOLD}{Colors.BOLD}")
    print("   ███████╗ █████╗ ███╗   ███╗███████╗███████╗██████╗ ")
    print("   ██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝██╔══██╗")
    print("   ███████╗███████║██╔████╔██║█████╗  █████╗  ██████╔╝")
    print("   ╚════██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══╝  ██╔══██╗")
    print("   ███████║██║  ██║██║ ╚═╝ ██║███████╗███████╗██║  ██║")
    print("   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝")
    
    # EXE Style Premium Divider
    print(f"{Colors.MAGENTA}{'━'*15} PREMIUM EDITION {'━'*15}{Colors.RESET}")
    
    print(f"\n {Colors.CYAN}◍ OWNER     : {Colors.WHITE}SAMEER")
    print(f" {Colors.CYAN}◍ ENGINE    : {Colors.HDR_GLOW}13P9-HIGH-SPEED")
    print(f" {Colors.CYAN}◍ STATUS    : {Colors.GREEN}ENCRYPTED & LIVE")
    
    print(f" {Colors.RED}◍ WARNING   : {Colors.WHITE}[ PRIVATE ACCESS ONLY ]")
    print(f"{Colors.MAGENTA}{'━'*47}{Colors.RESET}\n")

def loader(msg="Processing", sec=2):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for i in range(sec * 10):
        sys.stdout.write(f"\r{Colors.VIOLET}{msg} {Colors.HDR_GLOW}{chars[i % len(chars)]}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r" + " " * (len(msg) + 5) + "\r", end="")

def print_done(msg):
    print(f"{Colors.GREEN}{Colors.BOLD}✔ {Colors.WHITE}{msg}{Colors.RESET}")

def print_fail(msg):
    print(f"{Colors.RED}{Colors.BOLD}✘ {Colors.WHITE}{msg}{Colors.RESET}")

# --------------------------- API HANDLER ---------------------------
def call_api(endpoint, params):
    """
    KAISE SEARCH KAREIN: 
    Ye function _BASE_URL/{endpoint} ko query params ke sath hit karta hai.
    Example: api/send-otp?access_token=...&email=...
    """
    url = f"{_BASE_URL}/{endpoint}"
    try:
        r = requests.get(url, params=params, timeout=25)
        return r.json()
    except Exception as e:
        return {"success": False, "message": f"Network Error: {str(e)}"}

# --------------------------- CORE FEATURES ---------------------------

def handle_otp():
    banner()
    print(f"{Colors.VIOLET}[ ACTION: SEND OTP ]{Colors.RESET}\n")
    token = input(f"{Colors.CYAN}Token: {Colors.RESET}")
    email = input(f"{Colors.CYAN}Email: {Colors.RESET}")
    loader("Sending OTP...")
    res = call_api("send-otp", {"access_token": token, "email": email})
    if res.get("success") or res.get("status") == "SUCCESS":
        print_done("OTP sent to " + email)
    else:
        print_fail(res.get("message", "Failed to send OTP"))
    input("\nPress Enter...")

def handle_bind():
    banner()
    print(f"{Colors.GREEN}[ ACTION: FRESH BIND ]{Colors.RESET}\n")
    token = input(f"{Colors.CYAN}Token: {Colors.RESET}")
    email = input(f"{Colors.CYAN}Email: {Colors.RESET}")
    otp = input(f"{Colors.CYAN}OTP:   {Colors.RESET}")
    sc = input(f"{Colors.CYAN}Set Sec-Code: {Colors.RESET}")
    loader("Binding Account...")
    res = call_api("bind", {"access_token": token, "email": email, "otp": otp, "secondary_password": sc})
    print_done(str(res))
    input("\nPress Enter...")

def handle_info():
    banner()
    print(f"{Colors.CYAN}[ ACTION: CHECK INFO ]{Colors.RESET}\n")
    token = input(f"{Colors.GOLD}Access Token: {Colors.RESET}")
    loader("Fetching Data...")
    res = call_api("get-bind-info", {"access_token": token})
    print(f"\n{Colors.MAGENTA}--- BIND DETAILS ---{Colors.RESET}")
    print(json.dumps(res, indent=4))
    input("\nPress Enter...")

def handle_unbind_sec():
    banner()
    print(f"{Colors.RED}[ ACTION: UNBIND WITH SEC-CODE ]{Colors.RESET}\n")
    token = input(f"{Colors.CYAN}Token: {Colors.RESET}")
    sc = input(f"{Colors.CYAN}Security Code: {Colors.RESET}")
    loader("Unbinding...")
    res = call_api("unbind-with-sec", {"access_token": token, "secondary_password": sc})
    print_done(str(res))
    input("\nPress Enter...")

def handle_revoke():
    banner()
    print(f"{Colors.RED}[ ACTION: REVOKE ACCESS ]{Colors.RESET}\n")
    token = input(f"{Colors.GOLD}Access Token: {Colors.RESET}")
    loader("Logging Out...")
    res = call_api("revoke-token", {"access_token": token})
    print_done("Session Terminated Successfully")
    input("\nPress Enter...")

def handle_eat():
    banner()
    print(f"{Colors.HDR_GLOW}[ ACTION: EAT TO ACCESS ]{Colors.RESET}\n")
    eat = input(f"{Colors.CYAN}Paste EAT Token/Link: {Colors.RESET}")
    loader("Converting Token...")
    res = call_api("eat-token", {"eat_token": eat})
    print(f"\n{Colors.GREEN}ACCESS TOKEN: {Colors.WHITE}{res.get('access_token', 'Not Found')}{Colors.RESET}")
    input("\nPress Enter...")

# --------------------------- MAIN MENU ---------------------------

def main():
    while True:
        banner()
        print(f"{Colors.BOLD}{Colors.WHITE} P R E M I U M   M E N U{Colors.RESET}")
        print(f"{Colors.DIM}{'━'*47}{Colors.RESET}")
        print(f" {Colors.GREEN}[02]{Colors.WHITE} Bind New Email (One-Shot)")
        print(f" {Colors.GREEN}[03]{Colors.WHITE} Cancel Pending Request")
        print(f" {Colors.GREEN}[04]{Colors.WHITE} Unbind via Security Code")
        print(f" {Colors.GREEN}[05]{Colors.WHITE} Unbind via OTP")
        print(f" {Colors.GOLD}[06]{Colors.WHITE} Change Email (SEC)")
        print(f" {Colors.GOLD}[07]{Colors.WHITE} Change Email (OTP )")
        print(f" {Colors.CYAN}[08]{Colors.WHITE} Get Bind Status Info")
        print(f" {Colors.CYAN}[09]{Colors.WHITE} Linked Platform Info")
        print(f" {Colors.RED}[10]{Colors.WHITE} Revoke Session (Logout)")
        print(f" {Colors.MAGENTA}[11]{Colors.WHITE} EAT to Access (Not work)")
        print(f" {Colors.RED}[00]{Colors.WHITE} Exit Manager")
        print(f"{Colors.DIM}{'━'*47}{Colors.RESET}")
        
        choice = input(f"\n{Colors.HDR_GLOW}Selection ➤ {Colors.RESET}")

        if choice == "1": handle_otp()
        elif choice == "2": handle_bind()
        elif choice == "3": 
            token = input("Token: ")
            print(call_api("cancel", {"access_token": token}))
        elif choice == "4": handle_unbind_sec()
        elif choice == "8": handle_info()
        elif choice == "10": handle_revoke()
        elif choice == "11": handle_eat()
        elif choice == "0":
            print_done("Shutting down Sameer Engine...")
            sys.exit()
        else:
            print_fail("Invalid Choice!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit()