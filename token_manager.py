import json
import base64
import asyncio
import httpx
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import json_format, message
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# === Settings ===
MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"
RELEASEVERSION = "OB50"
MASTER_TOKEN_FILE = "master_token.txt"

# === Import Protobuf Modules ===
try:
    from proto import FreeFire_pb2, main_pb2, AccountPersonalShow_pb2
except ImportError:
    print(f"{Fore.RED}Error: Protobuf modules not found. "
          f"Please ensure FreeFire_pb2.py, main_pb2.py, and AccountPersonalShow_pb2.py "
          f"are in the proto/ directory.{Style.RESET_ALL}")
    exit(1)

# === Helper Functions ===
def pad_data(text: bytes) -> bytes:
    padding_length = AES.block_size - (len(text) % AES.block_size)
    return text + bytes([padding_length] * padding_length)

def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(pad_data(plaintext))

async def json_to_proto(json_data: str, proto_message: message.Message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)
    return proto_message.SerializeToString()

async def get_access_token(account: str):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = f"{account}&response_type=token&client_type=2&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
    headers = {
        'User-Agent': USERAGENT,
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
        resp = await client.post(url, data=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        access_token = data.get("access_token", "0")
        open_id = data.get("open_id", "0")
        return access_token, open_id

async def create_jwt(uid: str, password: str):
    retries = 3
    for attempt in range(retries):
        try:
            account = f"uid={uid}&password={password}"
            token_val, open_id = await get_access_token(account)
            body = json.dumps({
                "open_id": open_id,
                "open_id_type": "4",
                "login_token": token_val,
                "orign_platform_type": "4"
            })
            proto_bytes = await json_to_proto(body, FreeFire_pb2.LoginReq())
            payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)
            url = "https://loginbp.ggblueshark.com/MajorLogin"
            headers = {
                'User-Agent': USERAGENT,
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip",
                'Content-Type': "application/octet-stream",
                'Expect': "100-continue",
                'X-Unity-Version': "2022.3.47f1",
                'X-GA': "v1 1",
                'ReleaseVersion': RELEASEVERSION
            }
            async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
                resp = await client.post(url, data=payload, headers=headers)
                
                # Use MessageToJson to create a dict from the protobuf response
                try:
                    # First try to parse as LoginRes
                    login_res = FreeFire_pb2.LoginRes()
                    login_res.ParseFromString(resp.content)
                    msg = json.loads(json_format.MessageToJson(login_res))
                except:
                    # Fallback or error handling
                    if resp.status_code != 200:
                       raise Exception(f"Server returned status {resp.status_code}")
                    raise Exception("Failed to parse protobuf response")

                token = msg.get('token', '0')
                region = msg.get('lockRegion', '0')
                server_url = msg.get('serverUrl', 'https://loginbp.ggblueshark.com')
                return {
                    'uid': uid,
                    'token': f"{token}",
                    'region': region,
                    'server_url': server_url,
                }
        except Exception as e:
            if attempt < retries - 1:
                print(f"{Fore.YELLOW}⚠️ Login attempt {attempt+1} failed ({e}). Retrying...{Style.RESET_ALL}")
                await asyncio.sleep(2)
            else:
                return {'error': str(e), 'uid': uid}

def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
    ██████╗░███████╗██╗░░██╗
    ██╔══██╗██╔════╝╚██╗██╔╝
    ██║░░██║█████╗░░░╚███╔╝░
    ██║░░██║██╔══╝░░░██╔██╗░
    ██████╔╝███████╗██╔╝╚██╗
    ╚═════╝░╚══════╝╚═╝░░╚═╝
    {Style.RESET_ALL}""")
    print(f"{Fore.YELLOW}DEX RECOVER - Token Manager v1.1{Style.RESET_ALL}")
    print(f"{Fore.GREEN}================================={Style.RESET_ALL}")

def save_master_token(token_data):
    try:
        with open(MASTER_TOKEN_FILE, 'w', encoding='utf-8') as f:
            json.dump(token_data, f, indent=4)
        print(f"\n{Fore.GREEN}✅ Master Token saved successfully to {MASTER_TOKEN_FILE}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"\n{Fore.RED}❌ Failed to save token: {e}{Style.RESET_ALL}")
        return False

async def login_with_guest_file():
    display_banner()
    print(f"\n{Fore.YELLOW}Attempting login using guest100067.dat file...{Style.RESET_ALL}")
    
    guest_file = "guest100067.dat"
    # Check current directory and parent directory for the file
    possible_paths = [
        "guest100067.dat",
        "../guest100067.dat",
        "../guest100067",
        "guest100067"
    ]
    
    found_path = None
    for path in possible_paths:
        if os.path.exists(path):
            found_path = path
            break
            
    if not found_path:
        print(f"{Fore.RED}❌ guest100067.dat not found in current or parent directory.{Style.RESET_ALL}")
        return

    try:
        with open(found_path, 'r') as f:
            content = f.read().strip()
            data = json.loads(content)
            
        guest_info = data.get("guest_account_info", {})
        uid = guest_info.get("com.garena.msdk.guest_uid")
        password = guest_info.get("com.garena.msdk.guest_password")
        
        if not uid or not password:
             print(f"{Fore.RED}❌ Invalid guest file format.{Style.RESET_ALL}")
             return

        print(f"{Fore.CYAN}Found Guest Account: {uid}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Logging in...{Style.RESET_ALL}")
        
        result = await create_jwt(uid, password)
        
        if 'error' in result:
            print(f"\n{Fore.RED}❌ Login Failed: {result['error']}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✅ Login Successful!{Style.RESET_ALL}")
            print(f"Region: {result['region']}")
            print(f"Token: {result['token'][:20]}...")
            
            save_master_token(result)
            print(f"\n{Fore.YELLOW}You can now restart your server to use this token for searches.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}❌ Error reading guest file: {e}{Style.RESET_ALL}")

async def main():
    display_banner()
    print(f"\n{Fore.YELLOW}How do you want to login?{Style.RESET_ALL}")
    print("1. Enter UID/Password manually")
    print("2. Use guest100067.dat file (Recommended)")
    
    choice = input(f"\n{Fore.GREEN}Select option (1-2): {Style.RESET_ALL}").strip()
    
    if choice == '2':
        await login_with_guest_file()
        return

    print(f"\n{Fore.YELLOW}Log in with a BOT account to generate a Master Token.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This token will be used by the server to fetch player data.{Style.RESET_ALL}")
    print(f"{Fore.RED}NOTE: Do not use your main account as a bot!{Style.RESET_ALL}\n")

    uid = input(f"{Fore.CYAN}Enter Bot UID: {Style.RESET_ALL}").strip()
    if not uid:
        print(f"{Fore.RED}UID is required.{Style.RESET_ALL}")
        return

    password = input(f"{Fore.CYAN}Enter Box Password: {Style.RESET_ALL}").strip()
    if not password:
        print(f"{Fore.RED}Password is required.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}Logging in...{Style.RESET_ALL}")
    
    result = await create_jwt(uid, password)
    
    if 'error' in result:
        print(f"\n{Fore.RED}❌ Login Failed: {result['error']}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}✅ Login Successful!{Style.RESET_ALL}")
        print(f"Region: {result['region']}")
        print(f"Token: {result['token'][:20]}...")
        
        save_master_token(result)
        print(f"\n{Fore.YELLOW}You can now restart your server to use this token for searches.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
