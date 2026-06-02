# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
import requests
import os
import sys
import json
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3

translations = {
    "en": {
        "select_language": f"{Colors.CYAN}Select Language:{Colors.END}",
        "english": "English",
        "arabic": "Arabic",
        "available_options": f"{Colors.YELLOW}Available Options:{Colors.END}",
        "change_bind": f"{Colors.GREEN}CHANGE BIND EMAIL{Colors.END}",
        "unbind": f"{Colors.BLUE}UNBIND EMAIL{Colors.END}",
        "cancel": f"{Colors.RED}CANCEL BIND REQUEST{Colors.END}",
        "bind_info": f"{Colors.MAGENTA}BIND INFO{Colors.END}",
        "exit": f"{Colors.WHITE}EXIT{Colors.END}",
        "choose_option": f"{Colors.YELLOW}Choose option (1-5):{Colors.END}",
        "access_token": f"{Colors.CYAN}Access Token:{Colors.END}",
        "old_email": f"{Colors.BLUE}Old Email:{Colors.END}",
        "new_email": f"{Colors.GREEN}New Email:{Colors.END}",
        "enter_email": f"{Colors.YELLOW}Enter email:{Colors.END}",
        "enter_token": f"{Colors.YELLOW}Enter access token:{Colors.END}",
        "enter_otp": f"{Colors.CYAN}Enter OTP from {Colors.BOLD}{{email}}{Colors.END}{Colors.CYAN}:{Colors.END}",
        "enter_otp_simple": f"{Colors.CYAN}Enter OTP:{Colors.END}",
        "checking_bind": f"{Colors.YELLOW}Checking bind info...{Colors.END}",
        "account_info": f"{Colors.GREEN}Account Information:{Colors.END}",
        "current_email": f"{Colors.CYAN}Current Email:{Colors.END}",
        "pending_email": f"{Colors.YELLOW}Pending Email:{Colors.END}",
        "countdown": f"{Colors.MAGENTA}Countdown:{Colors.END}",
        "result": f"{Colors.BLUE}Result:{Colors.END}",
        "success": f"{Colors.GREEN}SUCCESS{Colors.END}",
        "failed": f"{Colors.RED}FAILED{Colors.END}",
        "summary": f"{Colors.CYAN}Summary:{Colors.END}",
        "status": f"{Colors.YELLOW}Status:{Colors.END}",
        "otp_sent": f"{Colors.GREEN}OTP successfully sent to your email!{Colors.END}",
        "otp_failed": f"{Colors.RED}OTP send failed!{Colors.END}",
        "verified": f"{Colors.GREEN}OTP verified! Identity token received.{Colors.END}",
        "verification_failed": f"{Colors.RED}OTP verification failed!{Colors.END}",
        "identity_token": f"{Colors.CYAN}Identity Token:{Colors.END}",
        "verifier_token": f"{Colors.GREEN}Verifier Token:{Colors.END}",
        "rebind_created": f"{Colors.GREEN}Email change request submitted successfully!{Colors.END}",
        "rebind_failed": f"{Colors.RED}Email change failed!{Colors.END}",
        "unbind_created": f"{Colors.GREEN}Unbind request successfully created!{Colors.END}",
        "unbind_failed": f"{Colors.RED}Unbind request failed!{Colors.END}",
        "cancel_success": f"{Colors.GREEN}Successfully Cancel Bind{Colors.END}",
        "cancel_failed": f"{Colors.RED}Bind cancel failed!{Colors.END}",
        "invalid_option": f"{Colors.RED}Invalid option! Please try again.{Colors.END}",
        "goodbye": f"{Colors.GREEN}Allah Hafez! 👋{Colors.END}",
        "press_enter": f"{Colors.CYAN}Press Enter to continue...{Colors.END}",
        "sending_otp": f"{Colors.YELLOW}Sending OTP to {Colors.BOLD}{{email}}{Colors.END}{Colors.YELLOW}...{Colors.END}",
        "verifying": f"{Colors.YELLOW}Verifying OTP...{Colors.END}",
        "creating_request": f"{Colors.YELLOW}Creating request...{Colors.END}",
        "step": f"{Colors.CYAN}Step{Colors.END}",
        "of": f"{Colors.WHITE}of{Colors.END}",
        "raw_response": f"{Colors.MAGENTA}Raw Response:{Colors.END}",
        "api_response": f"{Colors.BLUE}API Response{Colors.END}",
        "error": f"{Colors.RED}Error:{Colors.END}",
        "no_token": f"{Colors.RED}No identity token received!{Colors.END}",
        "no_verifier": f"{Colors.RED}No verifier token received!{Colors.END}",
        "parse_error": f"{Colors.RED}Failed to parse response!{Colors.END}"
    },
    "ar": {
        "select_language": f"{Colors.CYAN}اختر اللغة:{Colors.END}",
        "english": "الإنجليزية",
        "arabic": f"{Colors.YELLOW}العربية{Colors.END}",
        "available_options": f"{Colors.YELLOW}الخيارات المتاحة:{Colors.END}",
        "change_bind": f"{Colors.GREEN}تغيير البريد الإلكتروني المرتبط{Colors.END}",
        "unbind": f"{Colors.BLUE}فك الارتباط{Colors.END}",
        "cancel": f"{Colors.RED}إلغاء طلب الربط{Colors.END}",
        "bind_info": f"{Colors.MAGENTA}معلومات الربط{Colors.END}",
        "exit": f"{Colors.WHITE}خروج{Colors.END}",
        "choose_option": f"{Colors.YELLOW}اختر خيارًا (1-5):{Colors.END}",
        "access_token": f"{Colors.CYAN}رمز الوصول (Access Token):{Colors.END}",
        "old_email": f"{Colors.BLUE}البريد القديم:{Colors.END}",
        "new_email": f"{Colors.GREEN}البريد الجديد:{Colors.END}",
        "enter_email": f"{Colors.YELLOW}أدخل البريد الإلكتروني:{Colors.END}",
        "enter_token": f"{Colors.YELLOW}أدخل رمز الوصول:{Colors.END}",
        "enter_otp": f"{Colors.CYAN}أدخل OTP المرسل إلى {Colors.BOLD}{{email}}{Colors.END}{Colors.CYAN}:{Colors.END}",
        "enter_otp_simple": f"{Colors.CYAN}أدخل OTP:{Colors.END}",
        "checking_bind": f"{Colors.YELLOW}جاري التحقق من معلومات الربط...{Colors.END}",
        "account_info": f"{Colors.GREEN}معلومات الحساب:{Colors.END}",
        "current_email": f"{Colors.CYAN}البريد الحالي:{Colors.END}",
        "pending_email": f"{Colors.YELLOW}البريد المعلق:{Colors.END}",
        "countdown": f"{Colors.MAGENTA}العد التنازلي:{Colors.END}",
        "result": f"{Colors.BLUE}النتيجة:{Colors.END}",
        "success": f"{Colors.GREEN}نجاح{Colors.END}",
        "failed": f"{Colors.RED}فشل{Colors.END}",
        "summary": f"{Colors.CYAN}ملخص:{Colors.END}",
        "status": f"{Colors.YELLOW}الحالة:{Colors.END}",
        "otp_sent": f"{Colors.GREEN}تم إرسال OTP بنجاح إلى بريدك!{Colors.END}",
        "otp_failed": f"{Colors.RED}فشل إرسال OTP!{Colors.END}",
        "verified": f"{Colors.GREEN}تم التحقق من OTP! تم استلام رمز الهوية.{Colors.END}",
        "verification_failed": f"{Colors.RED}فشل التحقق من OTP!{Colors.END}",
        "identity_token": f"{Colors.CYAN}رمز الهوية (Identity Token):{Colors.END}",
        "verifier_token": f"{Colors.GREEN}رمز التحقق (Verifier Token):{Colors.END}",
        "rebind_created": f"{Colors.GREEN}تم تقديم طلب تغيير البريد بنجاح!{Colors.END}",
        "rebind_failed": f"{Colors.RED}فشل تغيير البريد!{Colors.END}",
        "unbind_created": f"{Colors.GREEN}تم إنشاء طلب فك الارتباط بنجاح!{Colors.END}",
        "unbind_failed": f"{Colors.RED}فشل طلب فك الارتباط!{Colors.END}",
        "cancel_success": f"{Colors.GREEN}تم إلغاء الربط بنجاح{Colors.END}",
        "cancel_failed": f"{Colors.RED}فشل إلغاء الربط!{Colors.END}",
        "invalid_option": f"{Colors.RED}خيار غير صالح! حاول مرة أخرى.{Colors.END}",
        "goodbye": f"{Colors.GREEN}الله حافظ! 👋{Colors.END}",
        "press_enter": f"{Colors.CYAN}اضغط Enter للمتابعة...{Colors.END}",
        "sending_otp": f"{Colors.YELLOW}جاري إرسال OTP إلى {Colors.BOLD}{{email}}{Colors.END}{Colors.YELLOW}...{Colors.END}",
        "verifying": f"{Colors.YELLOW}جاري التحقق من OTP...{Colors.END}",
        "creating_request": f"{Colors.YELLOW}جاري إنشاء الطلب...{Colors.END}",
        "step": f"{Colors.CYAN}خطوة{Colors.END}",
        "of": f"{Colors.WHITE}من{Colors.END}",
        "raw_response": f"{Colors.MAGENTA}الرد الخام:{Colors.END}",
        "api_response": f"{Colors.BLUE}رد API{Colors.END}",
        "error": f"{Colors.RED}خطأ:{Colors.END}",
        "no_token": f"{Colors.RED}لم يتم استلام رمز الهوية!{Colors.END}",
        "no_verifier": f"{Colors.RED}لم يتم استلام رمز التحقق!{Colors.END}",
        "parse_error": f"{Colors.RED}فشل تحليل الرد!{Colors.END}"
    }
}

# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
current_lang = "en"

def set_language():
    global current_lang
    clear_screen()
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}LANGUAGE SELECTION / اختر اللغة{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.END}")
    print(f"{Colors.GREEN}1. English{Colors.END}")
    print(f"{Colors.CYAN}2. العربية (Arabic){Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.END}")
    
    choice = input(f"\n{Colors.WHITE}Select language / اختر اللغة {Colors.YELLOW}(1-2){Colors.WHITE}: {Colors.END}").strip()
    
    if choice == "1":
        current_lang = "en"
    elif choice == "2":
        current_lang = "ar"
    else:
        current_lang = "en"
    
    clear_screen()

def t(key, **kwargs):
    text = translations[current_lang].get(key, translations["en"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    banner = f"""
    ███╗   ███╗  █████╗  ███████╗ ██████╗  ██╗   ██╗
  ████╗ ████║ ██╔══██╗ ██╔════╝ ██╔══██╗ ╚██╗ ██╔╝            ██╔████╔██║ ███████║ ███████╗ ██████╔╝  ╚████╔╝
  ██║╚██╔╝██║ ██╔══██║ ╚════██║ ██╔══██╗   ╚██╔╝
  ██║ ╚═╝ ██║ ██║  ██║ ███████║ ██║  ██║    ██║               ╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚══════╝ ╚═╝  ╚═╝    ╚═╝

                ██████╗   ██████╗  ████████╗                                ██╔══██╗ ██╔═══██╗ ╚══██╔══╝
                ██████╔╝ ██║   ██║    ██║                                   ██╔══██╗ ██║   ██║    ██║
                ██████╔╝ ╚██████╔╝    ██║
                ╚═════╝   ╚═════╝     ╚═╝
{Colors.MAGENTA}{'='*55}{Colors.END}
{Colors.YELLOW}                     Credits: @MC_8G & @S_3_0_3                     {Colors.END}
{Colors.CYAN}                     MaSrY &  H4RDIXX                                  {Colors.END}
{Colors.MAGENTA}{'='*55}{Colors.END}
"""
    print(banner)

def show_menu():
    print(f"\n{Colors.BOLD}{t('available_options')}{Colors.END}")
    print(f"{Colors.GREEN}1. {t('change_bind')}{Colors.END}")
    print(f"{Colors.BLUE}2. {t('unbind')}{Colors.END}")
    print(f"{Colors.RED}3. {t('cancel')}{Colors.END}")
    print(f"{Colors.MAGENTA}4. {t('bind_info')}{Colors.END}")
    print(f"{Colors.WHITE}5. {t('exit')}{Colors.END}")
    print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
def check_bind_info(access_token=None, show_raw=True):
    if not access_token:
        print(f"\n{Colors.BOLD}{t('enter_token')}{Colors.END} ", end="")
        access_token = input()
    
    print(f"\n{Colors.GREEN}[✓]{Colors.END} {t('checking_bind')}")
    
    try:
        info_url = f"https://fiddu-bind-info.vercel.app/bind/info?access={access_token}"
        info_response = requests.get(info_url)
        info_data = info_response.json()
        
        print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
        print(f"{Colors.GREEN}✓ {t('account_info')}{Colors.END}")
        print(f"{Colors.CYAN}{'='*55}{Colors.END}")
        
        if info_data.get("status") == "success":
            data = info_data.get("data", {})
            current_email = data.get("current_email", "N/A")
            pending_email = data.get("pending_email", "")
            countdown_seconds = data.get("countdown_seconds", 0)
            countdown_human = data.get("countdown_human", "0")
            raw_response = data.get("raw_response", {})
            
            print(f"  {Colors.CYAN}{t('current_email')}{Colors.END} {Colors.WHITE}{current_email}{Colors.END}")
            if pending_email:
                print(f"  {Colors.YELLOW}{t('pending_email')}{Colors.END} {Colors.WHITE}{pending_email}{Colors.END}")
            print(f"  {Colors.MAGENTA}{t('countdown')}{Colors.END} {Colors.WHITE}{countdown_human} ({countdown_seconds} seconds){Colors.END}")
            
            if raw_response.get("result") == 0:
                print(f"  {t('result')} {Colors.GREEN}✓ {t('success')}{Colors.END}")
            else:
                print(f"  {t('result')} {Colors.RED}✗ {raw_response.get('result', 'Unknown')}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
            summary = info_data.get("summary", "")
            if summary:
                print(f"\n  {t('summary')} {Colors.WHITE}{summary}{Colors.END}")

            if show_raw:
                print(f"\n  {t('raw_response')}")
                print(f"{Colors.MAGENTA}{'-'*50}{Colors.END}")
                print(f"{Colors.WHITE}{json.dumps(raw_response, indent=2, ensure_ascii=False)}{Colors.END}")
            
            print(f"\n  {t('status')} {Colors.CYAN}{info_data.get('status')}{Colors.END}")
            print(f"  {Colors.YELLOW}Status Code:{Colors.END} {Colors.WHITE}{info_data.get('status_code')}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
        else:
            error_msg = info_data.get('error', 'Unknown error')
            print(f"  {Colors.RED}✗ {t('error')} {error_msg}{Colors.END}")
            if 'response_text' in info_data:
                print(f"  {Colors.YELLOW}Response:{Colors.END} {Colors.WHITE}{info_data['response_text']}{Colors.END}")
        
        print(f"{Colors.CYAN}{'='*55}{Colors.END}")
        return info_data
        
    except Exception as e:
        print(f"  {Colors.RED}✗ {t('error')} {str(e)}{Colors.END}")
        return None
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
def format_response(response_text, title="Response"):
    print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}{title}:{Colors.END}")
    
    try:
        if response_text.strip().startswith('{') or response_text.strip().startswith('['):
            parsed = json.loads(response_text)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            print(f"{Colors.WHITE}{formatted}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3

            if isinstance(parsed, dict):
                if parsed.get("result") == 0:
                    print(f"\n{Colors.GREEN}✓ {t('success')}{Colors.END}{Colors.WHITE}: Result: 0{Colors.END}")
                elif parsed.get("result") != 0 and parsed.get("result") is not None:
                    print(f"\n{Colors.RED}✗ {t('failed')}{Colors.END}{Colors.WHITE}: Result: {parsed.get('result')}{Colors.END}")
                
                print(f"\n{Colors.MAGENTA}{t('raw_response')}{Colors.END}")
                for key, value in parsed.items():
                    if key != "result" and value:
                        print(f"  {Colors.CYAN}{key}:{Colors.END} {Colors.WHITE}{value}{Colors.END}")
        else:
            print(f"{Colors.WHITE}{response_text}{Colors.END}")
            
            if '"result": 0' in response_text:
                print(f"\n{Colors.GREEN}✓ {t('success')}{Colors.END}")
    except:
        print(f"{Colors.WHITE}{response_text}{Colors.END}")
    
    print(f"{Colors.CYAN}{'='*55}{Colors.END}\n")

def change_bind_email():
    print(f"\n{Colors.BOLD}{Colors.GREEN}[ {t('change_bind')} ]{Colors.END}")
    print(f"{Colors.CYAN}{'='*55}{Colors.END}")
    

    print(f"\n{Colors.BOLD}{t('access_token')}{Colors.END} ", end="")
    access_token = input()
    print(f"{Colors.BOLD}{t('old_email')}{Colors.END} ", end="")
    old_email = input()
    print(f"{Colors.BOLD}{t('new_email')}{Colors.END} ", end="")
    new_email = input()
    

    check_bind_info(access_token, show_raw=False)
    
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    

    print(f"\n{Colors.YELLOW}[{t('step')} 1/5] {t('sending_otp', email=old_email)}{Colors.END}")
    url_send = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
    data = {
        "email": old_email,
        "locale": "en_PK",
        "region": "PK",
        "app_id": "100067",
        "access_token": access_token
    }
    
    r = requests.post(url_send, headers=headers, data=data)
    format_response(r.text, f"{t('api_response')} - Old Email")
    
    print(f"\n{Colors.CYAN}{t('enter_otp', email=old_email)}{Colors.END} ", end="")
    otp_old = input()
    
    print(f"\n{Colors.YELLOW}[{t('step')} 2/5] {t('verifying')}{Colors.END}")
    url_verify_identity = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
    data = {
        "email": old_email,
        "app_id": "100067",
        "access_token": access_token,
        "otp": otp_old
    }
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    r = requests.post(url_verify_identity, headers=headers, data=data)
    format_response(r.text, f"{t('api_response')} - Verify Identity")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    try:
        res = r.json()
        identity_token = res.get("identity_token")
        if identity_token:
            print(f"\n{Colors.GREEN}✓ {t('identity_token')}{Colors.END} {Colors.WHITE}{identity_token}{Colors.END}")
        else:
            print(f"\n{Colors.RED}✗ {t('no_token')}{Colors.END}")
            input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
            return
    except:
        print(f"\n{Colors.RED}✗ {t('parse_error')}{Colors.END}")
        input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
        return
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    print(f"\n{Colors.YELLOW}[{t('step')} 3/5] {t('sending_otp', email=new_email)}{Colors.END}")
    data = {
        "email": new_email,
        "locale": "en_PK",
        "region": "PK",
        "app_id": "100067",
        "access_token": access_token
    }
    
    r = requests.post(url_send, headers=headers, data=data)
    format_response(r.text, f"{t('api_response')} - New Email")
    
    print(f"\n{Colors.CYAN}{t('enter_otp', email=new_email)}{Colors.END} ", end="")
    otp_new = input()
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    print(f"\n{Colors.YELLOW}[{t('step')} 4/5] {t('verifying')}{Colors.END}")
    url_verify_otp = "https://100067.connect.garena.com/game/account_security/bind:verify_otp"
    data = {
        "email": new_email,
        "app_id": "100067",
        "access_token": access_token,
        "otp": otp_new
    }
    
    r = requests.post(url_verify_otp, headers=headers, data=data)
    format_response(r.text, f"{t('api_response')} - Verify OTP")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    try:
        res = r.json()
        verifier_token = res.get("verifier_token")
        if verifier_token:
            print(f"\n{Colors.GREEN}✓ {t('verifier_token')}{Colors.END} {Colors.WHITE}{verifier_token}{Colors.END}")
        else:
            print(f"\n{Colors.RED}✗ {t('no_verifier')}{Colors.END}")
            input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
            return
    except:
        print(f"\n{Colors.RED}✗ {t('parse_error')}{Colors.END}")
        input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
        return
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    print(f"\n{Colors.YELLOW}[{t('step')} 5/5] {t('creating_request')}{Colors.END}")
    url_rebind = "https://100067.connect.garena.com/game/account_security/bind:create_rebind_request"
    data = {
        "identity_token": identity_token,
        "email": new_email,
        "app_id": "100067",
        "verifier_token": verifier_token,
        "access_token": access_token
    }
    
    r = requests.post(url_rebind, headers=headers, data=data)
    format_response(r.text, f"{t('api_response')} - Rebind")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    if r.status_code == 200 and '"result": 0' in r.text:
        print(f"\n{Colors.GREEN}✓ {t('rebind_created')}{Colors.END}")
    else:
        print(f"\n{Colors.RED}✗ {t('rebind_failed')}{Colors.END}")
    
    input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")

# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
def unbind_email():
    print(f"\n{Colors.BOLD}{Colors.BLUE}[ {t('unbind')} ]{Colors.END}")
    print(f"{Colors.CYAN}{'='*55}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    
    print(f"\n{Colors.BOLD}{t('enter_email')}{Colors.END} ", end="")
    email = input()
    print(f"{Colors.BOLD}{t('enter_token')}{Colors.END} ", end="")
    access_token = input()
    
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    check_bind_info(access_token, show_raw=False)
    
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    print(f"\n{Colors.YELLOW}[{t('step')} 1/3] {t('sending_otp', email=email)}{Colors.END}")
    send_otp_url = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
    send_otp_data = {
        "email": email,
        "locale": "en_PK",
        "region": "PK",
        "app_id": "100067",
        "access_token": access_token
    }
    
    resp = requests.post(send_otp_url, headers=headers, data=send_otp_data)
    format_response(resp.text, f"{t('api_response')} - Send OTP")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    if resp.status_code == 200:
        try:
            if resp.json().get("result") == 0:
                print(f"\n{Colors.GREEN}✓ {t('otp_sent')}{Colors.END}")
            else:
                print(f"\n{Colors.RED}✗ {t('otp_failed')}{Colors.END}")
                input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
                return
        except:
            pass
    
    print(f"\n{Colors.CYAN}{t('enter_otp_simple')}{Colors.END} ", end="")
    otp = input()
    
    print(f"\n{Colors.YELLOW}[{t('step')} 2/3] {t('verifying')}{Colors.END}")
    verify_url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
    verify_data = {
        "email": email,
        "app_id": "100067",
        "access_token": access_token,
        "otp": otp
    }
    
    resp = requests.post(verify_url, headers=headers, data=verify_data)
    format_response(resp.text, f"{t('api_response')} - Verify Identity")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    identity_token = None
    if resp.status_code == 200:
        try:
            resp_json = resp.json()
            if resp_json.get("result") == 0:
                identity_token = resp_json.get("identity_token")
                print(f"\n{Colors.GREEN}✓ {t('verified')}{Colors.END}")
                print(f"  {t('identity_token')} {Colors.WHITE}{identity_token}{Colors.END}")
            else:
                print(f"\n{Colors.RED}✗ {t('verification_failed')}{Colors.END}")
                input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
                return
        except:
            print(f"\n{Colors.RED}✗ {t('parse_error')}{Colors.END}")
            input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
            return
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    if not identity_token:
        print(f"\n{Colors.RED}✗ {t('no_token')}{Colors.END}")
        input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
        return
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    print(f"\n{Colors.YELLOW}[{t('step')} 3/3] {t('creating_request')}{Colors.END}")
    unbind_url = "https://100067.connect.garena.com/game/account_security/bind:create_unbind_request"
    unbind_data = {
        "app_id": "100067",
        "access_token": access_token,
        "identity_token": identity_token
    }
    
    resp = requests.post(unbind_url, headers=headers, data=unbind_data)
    format_response(resp.text, f"{t('api_response')} - Unbind")
    
    if resp.status_code == 200 and '"result": 0' in resp.text:
        print(f"\n{Colors.GREEN}✓ {t('unbind_created')}{Colors.END}")
    else:
        print(f"\n{Colors.RED}✗ {t('unbind_failed')}{Colors.END}")
    
    input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
def cancel_bind():
    print(f"\n{Colors.BOLD}{Colors.RED}[ {t('cancel')} ]{Colors.END}")
    print(f"{Colors.CYAN}{'='*55}{Colors.END}")
    
    print(f"\n{Colors.BOLD}{t('enter_token')}{Colors.END} ", end="")
    access_token = input()
    
    check_bind_info(access_token, show_raw=False)
    
    print(f"\n{Colors.YELLOW}{t('creating_request')}{Colors.END}")
    
    url = "https://100067.connect.gopapi.io/game/account_security/bind:cancel_request"
    
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    data = {
        "app_id": "100067",
        "access_token": access_token
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    print(f"{Colors.YELLOW}Status Code:{Colors.END} {Colors.WHITE}{response.status_code}{Colors.END}")
    format_response(response.text, f"{t('api_response')} - Cancel")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    if '"result": 0' in response.text:
        print(f"\n{Colors.GREEN}✓ {t('cancel_success')}{Colors.END}")
    else:
        print(f"\n{Colors.RED}✗ {t('cancel_failed')}{Colors.END}")
    
    input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")

def bind_info_only():
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}[ {t('bind_info')} ]{Colors.END}")
    print(f"{Colors.CYAN}{'='*55}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    print(f"\n{Colors.BOLD}{t('enter_token')}{Colors.END} ", end="")
    access_token = input()
    check_bind_info(access_token, show_raw=True)
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
    input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")

def main():
    set_language()
    
    while True:
        clear_screen()
        show_banner()
        show_menu()
        
        print(f"\n{Colors.BOLD}{t('choose_option')}{Colors.END} ", end="")
        choice = input()
        
        if choice == "1":
            clear_screen()
            show_banner()
            change_bind_email()
        elif choice == "2":
            clear_screen()
            show_banner()
            unbind_email()
        elif choice == "3":
            clear_screen()
            show_banner()
            cancel_bind()
        elif choice == "4":
            clear_screen()
            show_banner()
            bind_info_only()
        elif choice == "5":
            print(f"\n{Colors.GREEN}{t('goodbye')}{Colors.END}")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}{t('invalid_option')}{Colors.END}")
            input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}{t('goodbye')}{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
        input(f"\n{Colors.CYAN}{t('press_enter')}{Colors.END}")
# تغيير الحقوق يعني أنك تعرّفني بأنك شخص فاشل / Changing the credits means you admit you are a failure
# TG @MC_8G & @S_3_0_3    