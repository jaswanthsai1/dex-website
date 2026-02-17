import httpx
import asyncio
import warnings
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse, parse_qs
from urllib3.exceptions import InsecureRequestWarning
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import json_format, message
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# === Settings ===
MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"
RELEASEVERSION = "OB52"
MASTER_TOKEN_FILE = "master_token.txt"
BIO_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
BIO_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# Configuration for Blacklist checking
TEST_UIDS_CONFIG = {
    "IND": {"uid": "2263549557", "name": "N1L-UXㅤᵉˣᵉ"},
    "BD": {"uid": "5557645875", "name": "B2FㅤNINㅤCOMP"},
    "BR": {"uid": "80737380", "name": "may sz"}
}

# === Import Protobuf Modules ===
try:
    from proto import FreeFire_pb2, main_pb2, AccountPersonalShow_pb2
except ImportError:
    print("Warning: Protobuf modules not found. Real data fetching will be disabled.")
    FreeFire_pb2 = None
    main_pb2 = None
    AccountPersonalShow_pb2 = None
    
# === Bio Protobuf Setup (Inline) ===
Data = None
EmptyMessage = None
try:
    _sym_db = _symbol_database.Default()
    DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndata.proto\"\xbb\x01\n\x04\x44\x61ta\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x1e\n\x07\x66ield_5\x18\x05 \x01(\x0b\x32\r.EmptyMessage\x12\x1e\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\r.EmptyMessage\x12\x0f\n\x07\x66ield_8\x18\x08 \x01(\t\x12\x0f\n\x07\x66ield_9\x18\t \x01(\x05\x12\x1f\n\x08\x66ield_11\x18\x0b \x01(\x0b\x32\r.EmptyMessage\x12\x1f\n\x08\x66ield_12\x18\x0c \x01(\x0b\x32\r.EmptyMessage\"\x0e\n\x0c\x45mptyMessageb\x06proto3')
    _globals = globals()
    _builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
    _builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data1_pb2', _globals)
    if _descriptor._USE_C_DESCRIPTORS == False:
        DESCRIPTOR._options = None
        _globals['_DATA']._serialized_start = 15
        _globals['_DATA']._serialized_end = 202
        _globals['_EMPTYMESSAGE']._serialized_start = 204
        _globals['_EMPTYMESSAGE']._serialized_end = 218
    Data = _sym_db.GetSymbol('Data')
    EmptyMessage = _sym_db.GetSymbol('EmptyMessage')
except Exception as e:
    print(f"Warning: Failed to setup Bio Protobuf: {e}")

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

def decode_protobuf(encoded_data: bytes, message_type: message.Message) -> message.Message:
    instance = message_type()
    instance.ParseFromString(encoded_data)
    instance.ParseFromString(encoded_data)
    return instance

def decode_jwt_payload(token: str):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {"error": "Invalid JWT format"}
        payload = parts[1]
        padding = len(payload) % 4
        if padding:
            payload += '=' * (4 - padding)
        decoded_bytes = base64.urlsafe_b64decode(payload)
        return json.loads(decoded_bytes)
    except Exception as e:
        return {"error": str(e)}

def get_master_token():
    """Retrieve the master token from file if available"""
    if not os.path.exists(MASTER_TOKEN_FILE):
        return None
    try:
        with open(MASTER_TOKEN_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Check if token is expired (implement logic if expiration time is known)
            return data
    except Exception as e:
        print(f"Error reading master token: {e}")
        return None



def get_bio_server_url(lock_region: str):
    """Select Free Fire bio endpoint based on region"""
    region = lock_region.upper()
    if region == "IND":
        return "https://client.ind.freefiremobile.com/UpdateSocialBasicInfo"
    elif region in {"BR", "US", "SAC", "NA"}:
        return "https://client.us.freefiremobile.com/UpdateSocialBasicInfo"
    elif region == "BD":
        return "https://client.bd.freefiremobile.com/UpdateSocialBasicInfo"
    elif region == "SG":
        return "https://client.sg.freefiremobile.com/UpdateSocialBasicInfo"
    else:
        return "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo"

async def fetch_player_personal_show(target_uid: str, token_data: dict):
    """Fetch real player data from Garena using master token"""
    if not main_pb2 or not AccountPersonalShow_pb2:
        return {"error": "Protobuf modules missing"}
        
    try:
        bearer_token = f"Bearer {token_data.get('token')}"
        server_url = token_data.get('server_url', 'https://loginbp.ggblueshark.com')
        
        # 'unk' value is "7" in the original GetAccountInformation
        payload = await json_to_proto(json.dumps({'a': target_uid, 'b': "7"}), main_pb2.GetPlayerPersonalShow())
        data_enc = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, payload)

        headers = {
            'User-Agent': USERAGENT,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'Authorization': bearer_token,
            'X-Unity-Version': "2022.3.47f1",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASEVERSION
        }
        
        async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
            resp = await client.post(server_url + "/GetPlayerPersonalShow", data=data_enc, headers=headers)
            
            if resp.status_code != 200:
                return {"error": f"Garena API returned {resp.status_code}"}
                
            decoded_info = json.loads(json_format.MessageToJson(
                decode_protobuf(resp.content, AccountPersonalShow_pb2.AccountPersonalShowInfo)
            ))
            return decoded_info
            
    except Exception as e:
        return {"error": str(e)}

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (CSS, JS, etc.) from a specific path
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main DEX RECOVER interface"""
    try:
        with open("dex-recover.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading page: {e}</h1>"

@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(content={})

async def get_garena_data(eat_token: str):
    try:
        async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
            callback_url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
            response = await client.get(callback_url, follow_redirects=False)

            if 300 <= response.status_code < 400 and "Location" in response.headers:
                redirect_url = response.headers["Location"]
                parsed_url = urlparse(redirect_url)
                query_params = parse_qs(parsed_url.query)
                print(f"Debug: Garena Redirect Params: {query_params}")

                token_value = query_params.get("access_token", [None])[0]
                account_id = query_params.get("account_id", [None])[0]
                account_nickname = query_params.get("nickname", [None])[0]
                region = query_params.get("region", [None])[0]

                if not token_value or not account_id:
                    return {"error": "Failed to extract data from Garena"}
            else:
                return {"error": "Invalid access token or session expired"}

            openid_url = "https://topup.pk/api/auth/player_id_login"
            openid_headers = { 
            "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-MM,en-US;q=0.9,en;q=0.8",
        "Content-Type": "application/json",
        "Origin": "https://topup.pk",
        "Referer": "https://topup.pk/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; RMX5070 Build/UKQ1.231108.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.157 Mobile Safari/537.36",
        "X-Requested-With": "mark.via.gp",
        "Cookie": "source=mb; region=PK; mspid2=13c49fb51ece78886ebf7108a4907756; _fbp=fb.1.1753985808817.794945392376454660; language=en; datadome=WQaG3HalUB3PsGoSXY3TdcrSQextsSFwkOp1cqZtJ7Ax4YkiERHUgkgHlEAIccQO~w8dzTGM70D9SzaH7vymmEqOrVeX5pIsPVE22Uf3TDu6W3WG7j36ulnTg2DltRO7; session_key=hq02g63z3zjcumm76mafcooitj7nc79y",
        }
            payload = {"app_id": 100067, "login_id": str(account_id)}

            
            openid_res = await client.post(openid_url, headers=openid_headers, json=payload)
            openid_data = openid_res.json()
            open_id = openid_data.get("open_id")
            
            if not open_id:
                return {"error": "Failed to extract open_id"}

            return {
                "status": "success",
                "account_id": account_id,
                "account_nickname": account_nickname,
                "open_id": open_id,
                "access_token": token_value,
                "region": region,
                "credit": "M. JASWANTH SAI",
                "Instagram": "__dexzzz"
            }

    except Exception as e:
        return {"error": "Server error", "details": str(e)}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Return the DEX RECOVER website
    with open("dex-recover.html", "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/Eat")
async def get_token_info(eat_token: str = Query(..., description="Garena Access Token")):
    result = await get_garena_data(eat_token)
    return result

async def get_player_data_by_open_id(open_id: str):
    try:
        async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
            # This is a mock implementation since we don't have the exact API endpoint for player data by Open ID
            # In a real implementation, this would call the appropriate Garena API
            # For now, we'll return sample data structure based on typical player info
            
            # Since we don't have the exact API for retrieving player data by Open ID,
            # we'll return a message indicating this limitation
            return {
                "status": "info",
                "open_id": open_id,
                "message": "Direct player data retrieval by Open ID requires specific Garena API access that may not be publicly available",
                "note": "Open ID is typically used internally by Garena for account identification",
                "credit": "M. JASWANTH SAI",
                "Instagram": "__dexzzz"
            }
    except Exception as e:
        return {"error": "Server error", "details": str(e)}

@app.get("/PlayerInfo")
async def get_player_info(open_id: str = Query(..., description="Garena Open ID")):
    result = await get_player_data_by_open_id(open_id)
    return result

# ===== NEW ADVANCED SEARCH FEATURES =====

@app.get("/generate-jwt")
async def generate_jwt_endpoint(eat_token: str = Query(..., description="Garena Access Token (Hex)")):
    """
    Exchange Garena Access Token (Hex) for a JWT via MajorLogin
    """
    try:
        if not FreeFire_pb2:
             return {"error": "Protobuf modules missing on server"}

        # 1. Get OpenID from Access Token
        garena_data = await get_garena_data(eat_token)
        if "error" in garena_data:
            return {"error": garena_data["error"], "details": garena_data.get("details")}
            
        open_id = garena_data.get("open_id")
        if not open_id:
            return {"error": "Could not retrieve OpenID from token"}

        # 2. Prepare LoginReq
        body_dict = {
            "open_id": open_id,
            "open_id_type": "4",
            "login_token": eat_token,
            "orign_platform_type": "8"
        }
        print(f"Debug: MajorLogin Payload: {body_dict}")
        body = json.dumps(body_dict)
        
        # 3. Encrypt and Send
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
            
            if resp.status_code != 200:
                 return {"error": f"MajorLogin failed with status {resp.status_code}"}
            
            # 4. Parse Response
            msg = json.loads(json_format.MessageToJson(FreeFire_pb2.LoginRes.FromString(resp.content)))
            token = msg.get('token')
            region = msg.get('lockRegion')
            
            if not token:
                return {"error": "No JWT returned from MajorLogin"}
                
            return {
                "success": True,
                "access_token": token, # Returning as 'access_token' to match frontend expectation
                "region": region,
                "original_data": garena_data
            }

    except Exception as e:
        return {"error": f"JWT Generation failed: {str(e)}"}

@app.get("/decode-jwt")
async def decode_jwt_token(token: str = Query(..., description="JWT Token to decode")):
    """
    Decode a JWT token and return the payload information
    """
    result = decode_jwt_payload(token)
    if "error" in result:
        return {"error": result["error"]}
    return {"success": True, "decoded_data": result}

@app.get("/check-ban-uid")
async def check_ban_uid_endpoint(uid: str = Query(..., description="Free Fire UID")):
    """
    Check ban status using only UID (Uses Master Token)
    """
    print(f"DEBUG: Ban Check requested for UID: {uid}")
    try:
        master_token = get_master_token()
        if not master_token:
            print("DEBUG: Master token missing")
            return {"error": "Master token not configured for public checks."}
            
        # Fetch data using master token
        print(f"DEBUG: Fetching profile for {uid} using Master Token...")
        result = await fetch_player_personal_show(uid, master_token)
        
        if "error" in result:
             print(f"DEBUG: Fetch failed: {result['error']}")
             return {"error": f"Lookup failed: {result['error']}"}

        print("DEBUG: Profile fetched successfully, analyzing...")
        # Analyze for ban indicators
        # CS Ranking Ban
        is_cs_ban = result.get("isCsRankingBan", False)
        
        # Credit Score (Lower than 100 often means restrictions)
        credit_info = result.get("creditScoreInfo", {})
        credit_score = credit_info.get("creditScore", 100)
        
        # Profile status (Sometimes 'blacklist' info is here)
        # AccountPersonalShowInfo structure mapping from AccountPersonalShow_pb2
        
        status = "Clean"
        details = "No significant restrictions found."
        is_restricted = False
        
        if is_cs_ban:
            status = "Restricted"
            details = "Account is banned from CS Ranking."
            is_restricted = True
        elif credit_score < 90:
            status = "Suspicious"
            details = f"Low credit score ({credit_score}). Possible shadowban or recent reports."
            is_restricted = True
            
        # Check if the nickname is something like 'Restricted' or similar if garena renames
        basic_info = result.get("basicInfo", {})
        nickname = basic_info.get("nickname", "Unknown")

        return {
            "success": True,
            "uid": uid,
            "nickname": nickname,
            "status": status,
            "is_restricted": is_restricted,
            "details": details,
            "cs_ban": is_cs_ban,
            "credit_score": credit_score
        }

    except Exception as e:
        return {"error": f"Ban check failed: {str(e)}"}

@app.get("/check-blacklist")
async def check_blacklist_endpoint(token: str = Query(..., description="JWT Token")):
    """
    Check if the account is Shadowbanned/Blacklisted using JWT.
    (Kept for backward compatibility but UID-based check is preferred)
    """
    # ... existing implementation logic or just redirect to new one ...
    try:
        payload = decode_jwt_payload(token)
        if "error" in payload: return {"error": "Invalid Token"}
        uid = payload.get("open_id") # JWT often has open_id but maybe not UID
        # For JWT we usually need the region-specific test UID check
        # But user wants UID search. So we'll skip JWT logic for now if they prefer UID card.
        return {"success": False, "message": "Please use the UID-based Ban Status Checker card."}
    except:
        return {"error": "Internal error"}

@app.get("/uid-lookup")
async def uid_lookup(uid: str = Query(..., description="Free Fire UID")):
    """
    Look up player information by UID
    Uses server-side Master Token if available to fetch real data
    """
    try:
        # Try to get master token
        master_token = get_master_token()
        
        real_data = None
        if master_token:
            # Fetch real data
            real_data = await fetch_player_personal_show(uid, master_token)
            
        if real_data and "error" not in real_data:
            # Parse real data
            basic_info = real_data.get("basicInfo", {})
            clan_info = real_data.get("clanBasicInfo", {})
            captain_info = real_data.get("captainBasicInfo", {})
            
            return {
                "success": True,
                "message": "Player found!",
                "uid": uid,
                "data_source": "Live Garena API",
                "demo_structure": {
                    "nickname": basic_info.get("nickname", "Unknown"),
                    "level": basic_info.get("level", 0),
                    "region": basic_info.get("region", "Unknown"),
                    "rank": basic_info.get("rank", 0),
                    "clan_name": clan_info.get("clanName", "No Clan"),
                    "badge_count": basic_info.get("badgeCnt", 0),
                    "liked": basic_info.get("liked", 0),
                    "create_time": basic_info.get("createAt", 0),
                    "last_login": basic_info.get("lastLoginAt", 0)
                }
            }
        
        # Fallback to demo structure if no token or error
        error_msg = real_data.get("error") if real_data else "Server Master Token not configured"
        
        return {
            "success": True,
            "message": f"Showing DEMO data. Real lookup failed: {error_msg}",
            "uid": uid,
            "demo_structure": {
                "nickname": "Player Name (Demo)",
                "level": 75,
                "region": "IND",
                "rank": "Heroic",
                "clan_name": "Clan Name",
                "badge_count": 15,
                "note": "To see REAL data, admin must configure Master Token."
            }
        }
    except Exception as e:
        return {"error": f"UID lookup failed: {str(e)}"}

@app.get("/account-info")
async def get_account_info(uid: str = Query(..., description="Free Fire UID")):
    """
    Get detailed account information
    Uses Master Token to fetch real stats if available
    """
    try:
        master_token = get_master_token()
        real_data = None
        
        if master_token:
            real_data = await fetch_player_personal_show(uid, master_token)
            
        if real_data and "error" not in real_data:
             # Just return the raw data for advanced view
             return {
                 "success": True,
                 "message": "Account Details Fetched Successfully",
                 "uid": uid,
                 "raw_data": real_data
             }

        return {
            "success": True,
            "message": "Detailed account info requires authentication.",
            "uid": uid,
            "available_data": [
                "Basic Info (Nickname, Level, Region, Rank)",
                "Social Info (Bio, Gender, Language, Online Times)",
                "Stats (Ranking Points, Max Rank, Kills, Wins)",
                "Badges & Titles (Leaderboard positions, Achievements)",
                "Clan Info (Clan name, Badge, Frame, Role)",
                "Avatar Profile (Character, Skins, Equipped skills)",
                "Pet Info (Pet name, Level, Skills)",
                "Elite Pass Info (Current season, Badges)",
                "Recent Highlights (Recent wins, MVPs, Achievements)"
            ],
            "note": "Contact DEX RECOVER for full account analysis and recovery services"
        }
    except Exception as e:
        return {"error": f"Account info lookup failed: {str(e)}"}

# Contact Form Model
class ContactForm(BaseModel):
    name: str
    email: str
    service: str
    message: str

@app.post("/contact")
async def submit_contact_form(form: ContactForm):
    """
    Handle contact form submissions and send email notification
    Using FormSubmit.co for reliable email delivery
    """
    try:
        # For simplicity, we'll use FormSubmit.co service
        # The form will be submitted directly from frontend to FormSubmit
        # But we can also log it here for backup
        
        # Log the submission
        print(f"Contact Form Submission:")
        print(f"Name: {form.name}")
        print(f"Email: {form.email}")
        print(f"Service: {form.service}")
        print(f"Message: {form.message}")
        
        # You can also save to a file for backup
        with open("contact_submissions.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Name: {form.name}\n")
            f.write(f"Email: {form.email}\n")
            f.write(f"Service: {form.service}\n")
            f.write(f"Message: {form.message}\n")
            f.write(f"{'='*50}\n")
        
        return {
            "success": True,
            "message": "Message sent successfully! We'll get back to you soon."
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending message: {str(e)}"
        }



class BioUpdateRequest(BaseModel):
    token: str
    bio_text: str

@app.post("/update-bio")
async def update_bio(request: BioUpdateRequest):
    """
    Update player signature/bio using JWT token
    """
    try:
        token = request.token
        bio_text = request.bio_text
        
        # Decode JWT to get region
        parts = token.split('.')
        if len(parts) != 3:
            return {"success": False, "message": "Invalid JWT format"}
            
        payload = parts[1]
        padding = len(payload) % 4
        if padding:
            payload += '=' * (4 - padding)
        
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_json = json.loads(decoded_bytes)
        
        # Default to IND if not found, or maybe try to detect from other fields?
        lock_region = decoded_json.get("lock_region", "IND").upper()
        
        # Get server URL
        url_bio = get_bio_server_url(lock_region)
        
        if not Data or not EmptyMessage:
            return {"success": False, "message": "Bio wrapper unavailable (Protobuf error)"}
            
        # Build protobuf message
        data = Data()
        data.field_2 = 17
        data.field_5.CopyFrom(EmptyMessage())
        data.field_6.CopyFrom(EmptyMessage())
        data.field_8 = bio_text
        data.field_9 = 1
        data.field_11.CopyFrom(EmptyMessage())
        data.field_12.CopyFrom(EmptyMessage())
        
        # Encrypt
        data_bytes = data.SerializeToString()
        aes = AES.new(BIO_KEY, AES.MODE_CBC, BIO_IV)
        padding_length = AES.block_size - (len(data_bytes) % AES.block_size)
        padded_data = data_bytes + bytes([padding_length] * padding_length)
        encrypted_data = aes.encrypt(padded_data)
        
        headers = {
            "Expect": "100-continue",
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": RELEASEVERSION,
            "Content-Type": "application/octet-stream",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        print(f"Debug: Updating bio for region {lock_region} at {url_bio}")
        
        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            res_bio = await client.post(url_bio, headers=headers, data=encrypted_data)
            
            if res_bio.status_code == 200:
                print("Debug: Bio update success")
                return {
                    "success": True, 
                    "message": "Bio updated successfully!",
                    "region": lock_region,
                    "new_bio": bio_text
                }
            else:
                print(f"Debug: Bio update failed {res_bio.status_code}")
                return {
                    "success": False, 
                    "message": f"Server returned {res_bio.status_code}",
                    "details": res_bio.text[:200]
                }
                
    except Exception as e:
        print(f"Debug: Bio update exception {e}")
        return {"success": False, "message": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # Use port 8080 by default to match the previous server configuration
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))