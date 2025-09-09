Professional Proxy Rotator and MAC Spoofer for Ethical Hacking and Pentesting.

---

## Overview

**cbplus** is a Linux-based tool designed to enhance your penetration testing and ethical hacking workflows by:

- Automatically rotating through multiple proxy IPs every few seconds to evade IP-based blocks and rate limits.
- Periodically spoofing your network interface's MAC address to hide your device identity on local networks.
- Providing a simple CLI interface with configurable options.
- Logging activities with timestamps for easy monitoring.

This combination helps pentesters and bug bounty hunters simulate multiple clients and devices, improving stealth and test coverage during API and network assessments.

---

## Features

- Proxy rotation with customizable intervals.
- MAC address spoofing on specified network interface at configurable intervals.
- Supports HTTP/HTTPS proxies.
- Logs all actions with timestamps.
- Easy to extend and customize.
- Requires root privileges for MAC spoofing.

---

## Requirements

- Linux OS with `ip` command available.
- Python 3.x.
- Root privileges to change MAC address.
- Python package: `requests`

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cbplus.git
   cd cbplus




    Install dependencies:

    pip install -r requirements.txt




    Make the script executable:

    chmod +x cbplus.py





Usage

Run the tool with root privileges to enable MAC spoofing:

sudo ./cbplus.py -p http://proxy1:port http://proxy2:port ... -u https://targetapi.com/endpoint -i eth0


Arguments:


    -p, --proxies: List of proxy URLs to rotate through (required).

    -u, --url: Target URL to test proxy rotation (default: http://httpbin.org/ip).

    -i, --interface: Network interface to spoof MAC address (default: eth0).

    --proxy-interval: Seconds between proxy rotations (default: 5).

    --mac-interval: Seconds between MAC address changes (default: 300).



Example

Rotate 10 proxies every 5 seconds and spoof MAC on interface eth0 every 5 minutes:

sudo ./cbplus.py \
  -p http://1.1.1.1:8080 http://2.2.2.2:8080 http://3.3.3.3:8080 http://4.4.4.4:8080 http://5.5.5.5:8080 \
     http://6.6.6.6:8080 http://7.7.7.7:8080 http://8.8.8.8:8080 http://9.9.9.9:8080 http://10.10.10.10:8080 \
  -u http://httpbin.org/ip \
  -i eth0



Disclaimer

Use this tool only on networks and systems you own or have explicit permission to test. Unauthorized use may violate laws and ethical guidelines.

