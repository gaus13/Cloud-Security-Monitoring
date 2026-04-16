#!/usr/bin/env python3
"""
Cloud Security Threat Detector
Phase 3 - Detects brute force, invalid users, and root login attempts
"""

import re
from collections import defaultdict
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for colored output
init()

# ─── Configuration ────────────────────────────────────────────────
LOG_FILE = "auth.log"
BRUTE_FORCE_THRESHOLD = 5  # alerts after this many attempts from same IP

# ─── Storage ──────────────────────────────────────────────────────
failed_attempts = defaultdict(list)  # tracks attempts per IP
alerts = []                          # stores all alerts found

# ─── Helper: Print colored alerts ─────────────────────────────────
def print_alert(level, attack_type, message, ip=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if level == "CRITICAL":
        color = Fore.RED
    elif level == "HIGH":
        color = Fore.YELLOW
    else:
        color = Fore.CYAN

    print(f"{color}[{timestamp}] [{level}] {attack_type}{Style.RESET_ALL}")
    print(f"  → {message}")
    if ip:
        print(f"  → Source IP: {ip}")
    print()

    # Store alert for later use (Phase 4 will send these to AI)
    alerts.append({
        "timestamp": timestamp,
        "level": level,
        "type": attack_type,
        "message": message,
        "ip": ip
    })

# ─── Detection Functions ───────────────────────────────────────────

def detect_invalid_user(line):
    """Detects attempts to login with usernames that don't exist"""
    # Example log: Invalid user wronguser from 192.168.1.1 port 22
    match = re.search(
        r'Invalid user (\w+) from ([\d.]+)',
        line
    )
    if match:
        username = match.group(1)
        ip = match.group(2)
        failed_attempts[ip].append(line)

        print_alert(
            level="HIGH",
            attack_type="INVALID USER ATTEMPT",
            message=f"Someone tried to login as non-existent user '{username}'",
            ip=ip
        )
        return True
    return False


def detect_brute_force(line):
    """Detects multiple failed attempts from same IP = brute force"""
    # Example log: Failed password for root from 192.168.1.1
    match = re.search(
        r'Failed password for (\w+) from ([\d.]+)',
        line
    )
    if match:
        username = match.group(1)
        ip = match.group(2)
        failed_attempts[ip].append(line)

        # Check if same IP has crossed threshold
        if len(failed_attempts[ip]) >= BRUTE_FORCE_THRESHOLD:
            print_alert(
                level="CRITICAL",
                attack_type="BRUTE FORCE ATTACK DETECTED",
                message=f"IP {ip} made {len(failed_attempts[ip])} failed attempts. Targeting user: '{username}'",
                ip=ip
            )
        return True
    return False


def detect_root_login(line):
    """Detects anyone trying to login as root — always suspicious"""
    if "root" in line and (
        "Invalid user" in line or
        "Failed password" in line or
        "authentication failure" in line
    ):
        match = re.search(r'from ([\d.]+)', line)
        ip = match.group(1) if match else "Unknown"

        print_alert(
            level="CRITICAL",
            attack_type="ROOT LOGIN ATTEMPT",
            message="Someone attempted to login as ROOT — highest privilege account",
            ip=ip
        )
        return True
    return False


# ─── Main: Read and Analyze Log File ──────────────────────────────
def analyze_log(filepath):
    print(f"\n{Fore.CYAN}{'='*60}")
    print("   CLOUD SECURITY THREAT DETECTOR")
    print(f"   Analyzing: {filepath}")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Log file '{filepath}' not found!{Style.RESET_ALL}")
        return

    print(f"📄 Total log lines to analyze: {len(lines)}\n")
    print(f"{Fore.YELLOW}--- Scanning for threats ---{Style.RESET_ALL}\n")

    threat_count = 0

    for line in lines:
        detected = False
        detected = detect_root_login(line) or detected
        detected = detect_invalid_user(line) or detected
        detected = detect_brute_force(line) or detected
        if detected:
            threat_count += 1

    # ─── Summary Report ───────────────────────────────────────────
    print(f"\n{Fore.CYAN}{'='*60}")
    print("   DETECTION SUMMARY")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"📊 Total lines scanned:     {len(lines)}")
    print(f"⚠️  Total threats detected:  {threat_count}")
    print(f"\n🌐 Attacking IPs found:")

    for ip, attempts in failed_attempts.items():
        print(f"   {Fore.RED}{ip}{Style.RESET_ALL} → {len(attempts)} attempts")

    print(f"\n{Fore.GREEN}✅ Scan complete.{Style.RESET_ALL}\n")
    return alerts


# ─── Run ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    analyze_log(LOG_FILE)
