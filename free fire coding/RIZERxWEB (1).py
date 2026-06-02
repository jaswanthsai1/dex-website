#!/usr/bin/env python3
"""
RIZER ULTIMATE LOAD TESTER – REAL 10,000+ RPS
Uses pycurl (libcurl) for maximum performance + multiprocessing + threading
Single file – automatic dependency installation
Works on Linux, macOS, Termux (with some setup), VPS
"""

import os
import sys
import time
import random
import threading
import multiprocessing
import signal
import platform
import subprocess
from urllib.parse import urlparse
from datetime import datetime

# ---------- Color setup ----------
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_logo():
    logo = f"""
{Colors.RED}██████╗ ██╗███████╗███████╗██████╗ 
{Colors.YELLOW}██╔══██╗██║╚══███╔╝██╔════╝██╔══██╗
{Colors.GREEN}██████╔╝██║  ███╔╝ █████╗  ██████╔╝
{Colors.BLUE}██╔══██╗██║ ███╔╝  ██╔══╝  ██╔══██╗
{Colors.MAGENTA}██║  ██║██║███████╗███████╗██║  ██║
{Colors.CYAN}╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝{Colors.RESET}
    """
    print(logo)
    print(f"{Colors.WHITE}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}🔥 RIZER ULTIMATE – REAL 10,000+ RPS (PYCURL) 🔥{Colors.RESET}")
    print(f"{Colors.RED}⚠️  ONLY FOR YOUR OWN WEBSITES ⚠️{Colors.RESET}")
    print(f"{Colors.YELLOW}Using pycurl (libcurl) – maximum speed{Colors.RESET}")
    print(f"{Colors.WHITE}{'='*60}{Colors.RESET}\n")

# ---------- Auto install missing packages ----------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def ensure_dependencies():
    """Try to install pycurl; if it fails, fall back to requests and warn."""
    try:
        import pycurl
        print(f"{Colors.GREEN}✓ pycurl already installed{Colors.RESET}")
        return True
    except ImportError:
        print(f"{Colors.YELLOW}Installing pycurl (this may take a moment)...{Colors.RESET}")
        try:
            # On some systems, pycurl requires libcurl development headers.
            # We'll attempt pip install; if it fails, we fall back to requests.
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pycurl"])
            print(f"{Colors.GREEN}✓ pycurl installed successfully{Colors.RESET}")
            return True
        except:
            print(f"{Colors.RED}Failed to install pycurl. Falling back to requests (slower).{Colors.RESET}")
            try:
                import requests
            except:
                install("requests")
            return False

# ---------- Global stats (shared via Manager) ----------
def init_stats():
    manager = multiprocessing.Manager()
    stats = {
        'total': manager.Value('i', 0),
        'success': manager.Value('i', 0),
        'fail': manager.Value('i', 0),
        'start_time': manager.Value('d', time.time())
    }
    return manager, stats

# ---------- Pycurl worker (per thread) ----------
def pycurl_worker(url, stats, stop_event):
    """
    Each thread runs this function. It creates its own pycurl object
    and reuses it for every request to keep connections alive.
    """
    import pycurl
    from io import BytesIO

    parsed = urlparse(url)
    full_url = url  # base URL, we'll add cache buster later

    # Prepare pycurl object
    c = pycurl.Curl()
    c.setopt(pycurl.URL, full_url.encode('utf-8'))
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.CONNECTTIMEOUT, 3)
    c.setopt(pycurl.TIMEOUT, 5)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.FORBID_REUSE, 0)   # keep connection alive
    c.setopt(pycurl.FRESH_CONNECT, 0)  # try to reuse
    c.setopt(pycurl.TCP_KEEPALIVE, 1)
    c.setopt(pycurl.HTTPHEADER, [
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language: en-US,en;q=0.5',
        'Connection: keep-alive',
        'Cache-Control: no-cache',
    ])

    buffer = BytesIO()
    c.setopt(pycurl.WRITEDATA, buffer)

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/86.0'
    ]

    while not stop_event.is_set():
        try:
            # Rotate User-Agent
            c.setopt(pycurl.HTTPHEADER, [
                f'User-Agent: {random.choice(user_agents)}',
                'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language: en-US,en;q=0.5',
                'Connection: keep-alive',
                'Cache-Control: no-cache',
                f'X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
            ])

            # Cache buster
            cache_buster = f"?t={random.randint(1,999999)}"
            c.setopt(pycurl.URL, (full_url + cache_buster).encode('utf-8'))

            buffer.seek(0)
            buffer.truncate(0)
            c.perform()
            status = c.getinfo(pycurl.RESPONSE_CODE)
            if status < 400:
                stats['success'].value += 1
            else:
                stats['fail'].value += 1
        except Exception:
            stats['fail'].value += 1
        finally:
            stats['total'].value += 1

    c.close()

# ---------- Fallback requests worker (slower) ----------
def requests_worker(url, stats, stop_event):
    import requests
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ]
    session = requests.Session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()

    while not stop_event.is_set():
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            }
            cache_buster = f"?r={random.randint(1,999999)}"
            r = session.get(url + cache_buster, headers=headers, timeout=3)
            if r.status_code < 400:
                stats['success'].value += 1
            else:
                stats['fail'].value += 1
        except:
            stats['fail'].value += 1
        finally:
            stats['total'].value += 1

# ---------- Process main: starts threads ----------
def process_main(process_id, url, stats, threads_per_process, use_pycurl, stop_event):
    """Each process runs this function, spawning its threads."""
    worker_func = pycurl_worker if use_pycurl else requests_worker
    threads = []
    for i in range(threads_per_process):
        t = threading.Thread(target=worker_func, args=(url, stats, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
    # Keep threads alive until stop_event is set
    for t in threads:
        t.join()

# ---------- Monitor thread ----------
def monitor(stats, target_rps, duration, num_processes, threads_per_process, use_pycurl):
    start_time = time.time()
    last_total = 0
    while time.time() - start_time < duration + 1:
        time.sleep(1)
        elapsed = time.time() - start_time
        total = stats['total'].value
        success = stats['success'].value
        fail = stats['fail'].value
        current_rps = total - last_total
        last_total = total
        avg_rps = total / elapsed if elapsed > 0 else 0

        os.system('clear' if os.name == 'posix' else 'cls')
        print_logo()
        print(f"{Colors.CYAN}⏱️  Elapsed: {elapsed:.1f}s / {duration}s{Colors.RESET}")
        print(f"{Colors.YELLOW}🎯 Target RPS: {target_rps}{Colors.RESET}")
        print(f"{Colors.WHITE}{'─'*50}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Total Requests: {total:,}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Successful: {success:,}{Colors.RESET}")
        print(f"{Colors.RED}✗ Failed: {fail:,}{Colors.RESET}")
        print(f"{Colors.BLUE}⚡ Current RPS: {current_rps:,}{Colors.RESET}")
        print(f"{Colors.MAGENTA}📊 Average RPS: {avg_rps:.1f}{Colors.RESET}")

        if total > 0:
            success_rate = (success / total) * 100
            print(f"{Colors.CYAN}📈 Success Rate: {success_rate:.1f}%{Colors.RESET}")

        # Progress bar
        if target_rps > 0:
            percentage = min(100, (current_rps / target_rps) * 100)
            bar_len = 30
            filled = int(bar_len * percentage / 100)
            bar = '█' * filled + '░' * (bar_len - filled)
            print(f"\n{Colors.YELLOW}Progress: [{bar}] {percentage:.1f}%{Colors.RESET}")

        if fail > success * 0.5 and total > 100:
            print(f"\n{Colors.RED}⚠️  CRITICAL: High failure rate – server may be blocking!{Colors.RESET}")
        elif fail > success * 0.3 and total > 100:
            print(f"\n{Colors.YELLOW}⚠️  Warning: Many failures, check target{Colors.RESET}")

        print(f"\n{Colors.WHITE}{'='*50}{Colors.RESET}")
        print(f"{Colors.RED}Press Ctrl+C to stop test early{Colors.RESET}")

    # Duration finished
    print(f"\n{Colors.GREEN}Test finished. Finalizing...{Colors.RESET}")

# ---------- Main ----------
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print_logo()

    # Disclaimer
    print(f"{Colors.RED}{'⚠️'*60}{Colors.RESET}")
    print(f"{Colors.RED}⚠️  WARNING: THIS TOOL GENERATES REAL TRAFFIC{Colors.RESET}")
    print(f"{Colors.RED}⚠️  USE ONLY ON WEBSITES YOU OWN OR HAVE PERMISSION TO TEST{Colors.RESET}")
    print(f"{Colors.RED}⚠️  UNAUTHORIZED USE MAY BE ILLEGAL{Colors.RESET}")
    print(f"{Colors.RED}{'⚠️'*60}{Colors.RESET}\n")

    # Ensure dependencies
    use_pycurl = ensure_dependencies()
    if not use_pycurl:
        print(f"{Colors.YELLOW}Using slower requests library – RPS will be lower.{Colors.RESET}")

    # Get target URL
    url = input(f"{Colors.CYAN}Enter your website URL: {Colors.RESET}").strip()
    if not url:
        print(f"{Colors.RED}No URL provided. Exiting.{Colors.RESET}")
        sys.exit(1)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # System info
    cpu_cores = multiprocessing.cpu_count()
    print(f"\n{Colors.BLUE}System: {cpu_cores} CPU cores{Colors.RESET}")

    # Target RPS
    try:
        target_rps = int(input(f"{Colors.CYAN}Target requests per second (minimum 10000): {Colors.RESET}").strip())
        if target_rps < 10000:
            target_rps = 10000
            print(f"{Colors.YELLOW}Setting target to 10000 RPS{Colors.RESET}")
    except:
        target_rps = 10000
        print(f"{Colors.YELLOW}Using default 10000 RPS{Colors.RESET}")

    # Duration
    try:
        duration = int(input(f"{Colors.CYAN}Test duration in seconds (minimum 30): {Colors.RESET}").strip())
        if duration < 30:
            duration = 60
            print(f"{Colors.YELLOW}Setting duration to 60 seconds{Colors.RESET}")
    except:
        duration = 60

    # Processes (use all cores)
    try:
        num_processes = int(input(f"{Colors.CYAN}Number of processes (CPU cores recommended: {cpu_cores}): {Colors.RESET}").strip())
        if num_processes < 1:
            num_processes = cpu_cores
    except:
        num_processes = cpu_cores

    # Threads per process
    # Each thread with pycurl can handle a few hundred RPS. We'll aim high.
    threads_per_process = max(50, int(target_rps / (num_processes * 200)))
    print(f"{Colors.BLUE}Each process will run {threads_per_process} threads.{Colors.RESET}")

    # Final confirmation
    print(f"\n{Colors.RED}{'⚠️'*50}{Colors.RESET}")
    print(f"{Colors.RED}⚠️  FINAL WARNING: REAL TRAFFIC WILL BE SENT{Colors.RESET}")
    print(f"{Colors.RED}⚠️  Target: {url}{Colors.RESET}")
    print(f"{Colors.RED}⚠️  Processes: {num_processes}{Colors.RESET}")
    print(f"{Colors.RED}⚠️  Threads per process: {threads_per_process}{Colors.RESET}")
    print(f"{Colors.RED}⚠️  Total threads: {num_processes * threads_per_process}{Colors.RESET}")
    print(f"{Colors.RED}⚠️  Target RPS: {target_rps}{Colors.RESET}")
    print(f"{Colors.RED}⚠️  Duration: {duration}s{Colors.RESET}")
    if use_pycurl:
        print(f"{Colors.GREEN}✓ Using pycurl (fast){Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠️ Using requests (slow){Colors.RESET}")
    print(f"{Colors.RED}{'⚠️'*50}{Colors.RESET}\n")

    confirm = input(f"{Colors.YELLOW}Type 'I ACCEPT' to start: {Colors.RESET}")
    if confirm != "I ACCEPT":
        print(f"{Colors.RED}Cancelled.{Colors.RESET}")
        sys.exit(1)

    # Increase file descriptor limit on Linux
    if platform.system() == "Linux":
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))
            print(f"{Colors.GREEN}File descriptor limit increased.{Colors.RESET}")
        except:
            pass

    # Initialize shared stats
    manager = multiprocessing.Manager()
    stats = {
        'total': manager.Value('i', 0),
        'success': manager.Value('i', 0),
        'fail': manager.Value('i', 0),
        'start_time': manager.Value('d', time.time())
    }

    # Create a stop event for threads
    stop_event = multiprocessing.Manager().Event()

    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor, args=(stats, target_rps, duration, num_processes, threads_per_process, use_pycurl))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Start processes
    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(
            target=process_main,
            args=(i, url, stats, threads_per_process, use_pycurl, stop_event)
        )
        p.start()
        processes.append(p)
        time.sleep(0.2)

    # Wait for duration or interrupt
    try:
        time.sleep(duration + 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user. Stopping...{Colors.RESET}")

    # Stop all threads
    stop_event.set()

    # Terminate processes
    for p in processes:
        p.terminate()
        p.join()

    # Final stats
    elapsed = time.time() - stats['start_time'].value
    total = stats['total'].value
    success = stats['success'].value
    fail = stats['fail'].value

    print(f"\n{Colors.CYAN}=== FINAL RESULTS ==={Colors.RESET}")
    print(f"Total time: {elapsed:.2f}s")
    print(f"Total requests: {total:,}")
    print(f"Successful: {success:,}")
    print(f"Failed: {fail:,}")
    if elapsed > 0:
        print(f"Average RPS: {total/elapsed:.1f}")
    if fail > success * 0.5:
        print(f"\n{Colors.RED}❌ Your server CRASHED or is blocking traffic!{Colors.RESET}")
    elif fail > success * 0.2:
        print(f"\n{Colors.YELLOW}⚠️ Your server struggled under the load.{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}✅ Your server handled the load well!{Colors.RESET}")

    print(f"\n{Colors.YELLOW}Report saved to rizer_report.txt{Colors.RESET}")
    with open("rizer_report.txt", "w") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Duration: {elapsed:.2f}s\n")
        f.write(f"Total requests: {total}\n")
        f.write(f"Successful: {success}\n")
        f.write(f"Failed: {fail}\n")
        f.write(f"Average RPS: {total/elapsed:.1f}\n")

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    main()