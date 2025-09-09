#!/usr/bin/env python3
import argparse
import requests
import time
import threading
import random
import subprocess
import sys
from itertools import cycle
from datetime import datetime

# ========== Configuration ==========

DEFAULT_INTERFACE = "eth0"
DEFAULT_PROXY_ROTATE_INTERVAL = 5       # seconds
DEFAULT_MAC_ROTATE_INTERVAL = 300       # seconds (5 minutes)

# ========== Utility Functions ==========

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def random_mac():
    mac = [0x02, 0x00, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(f"{x:02x}" for x in mac)

def change_mac(interface):
    new_mac = random_mac()
    log(f"Changing MAC of {interface} to {new_mac}")
    try:
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["ip", "link", "set", interface, "address", new_mac], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        log("MAC address changed successfully.")
    except subprocess.CalledProcessError as e:
        log(f"Failed to change MAC address: {e}")

def mac_rotator(interface, interval):
    while True:
        change_mac(interface)
        time.sleep(interval)

def proxy_request(session, proxy, url):
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        log(f"Using proxy {proxy} to request {url}")
        resp = session.get(url, proxies=proxies, timeout=10)
        log(f"Response Status: {resp.status_code}")
        return resp.text
    except Exception as e:
        log(f"Proxy {proxy} failed: {e}")
        return None

def proxy_rotator(proxies, url, interval):
    session = requests.Session()
    proxy_cycle = cycle(proxies)
    while True:
        proxy = next(proxy_cycle)
        proxy_request(session, proxy, url)
        time.sleep(interval)

# ========== CLI ==========

def parse_args():
    parser = argparse.ArgumentParser(
        description="cbplus - Professional Proxy Rotator + MAC Spoofer for Pentesting"
    )
    parser.add_argument(
        "-p", "--proxies", required=True, nargs="+",
        help="List of proxy URLs (http://ip:port or socks5://ip:port)"
    )
    parser.add_argument(
        "-u", "--url", default="http://httpbin.org/ip",
        help="Target URL to test proxy rotation (default: http://httpbin.org/ip)"
    )
    parser.add_argument(
        "-i", "--interface", default=DEFAULT_INTERFACE,
        help=f"Network interface to spoof MAC address (default: {DEFAULT_INTERFACE})"
    )
    parser.add_argument(
        "--proxy-interval", type=int, default=DEFAULT_PROXY_ROTATE_INTERVAL,
        help=f"Seconds between proxy rotations (default: {DEFAULT_PROXY_ROTATE_INTERVAL})"
    )
    parser.add_argument(
        "--mac-interval", type=int, default=DEFAULT_MAC_ROTATE_INTERVAL,
        help=f"Seconds between MAC address changes (default: {DEFAULT_MAC_ROTATE_INTERVAL})"
    )
    return parser.parse_args()

# ========== Main ==========

def main():
    args = parse_args()

    if len(args.proxies) < 1:
        log("Error: Provide at least one proxy.")
        sys.exit(1)

    log(f"Starting cbplus with {len(args.proxies)} proxies.")
    log(f"Target URL: {args.url}")
    log(f"MAC spoofing interface: {args.interface}")
    log(f"Proxy rotation interval: {args.proxy_interval}s")
    log(f"MAC rotation interval: {args.mac_interval}s")

    # Start MAC spoofing thread
    mac_thread = threading.Thread(target=mac_rotator, args=(args.interface, args.mac_interval), daemon=True)
    mac_thread.start()

    # Start proxy rotation (main thread)
    try:
        proxy_rotator(args.proxies, args.url, args.proxy_interval)
    except KeyboardInterrupt:
        log("Exiting cbplus...")

if __name__ == "__main__":
    main()