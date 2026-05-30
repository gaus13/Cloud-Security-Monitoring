#!/usr/bin/env python3
"""
Phase 3 Extended — Threat Detector with Prometheus Metrics
Exposes metrics at localhost:8000/metrics for Grafana dashboards
"""

import re
import time
from collections import defaultdict
from datetime import datetime
from colorama import Fore, Style, init

# Prometheus metrics library
from prometheus_client import (
    start_http_server,
    Counter,
    Gauge,
    Histogram
)

init()

# ─── Prometheus Metrics Definition ────────────────────────────
# Counter = only goes up (total count)
# Gauge = can go up or down (current value)

attacks_total = Counter(
    'security_attacks_total',
    'Total number of attacks detected',
    ['attack_type']  # label — lets us filter by type in Grafana
)

attacking_ips = Gauge(
    'security_attacking_ips_total',
    'Number of unique attacking IPs detected'
)

log_lines_processed = Counter(
    'security_log_lines_total',
    'Total log lines processed'
)

last_attack_timestamp = Gauge(
    'security_last_attack_timestamp',
    'Timestamp of most recent attack detected'
)

# ─── Configuration ─────────────────────────────────────────────
LOG_FILE = "auth.log"
BRUTE_FORCE_THRESHOLD = 5
WATCH_INTERVAL = 10  # check for new logs every 10 seconds

# ─── Storage ───────────────────────────────────────────────────
failed_attempts = defaultdict(list)
alerted_ips = set()  # track which IPs we already alerted on

# ─── Alert Printer ─────────────────────────────────────────────
def print_alert(level, attack_type, message, ip=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = Fore.RED if level == "CRITICAL" else Fore.YELLOW

    print(f"\n{color}{'='*60}{Style.RESET_ALL}")
    print(f"{color}[{timestamp}] [{level}] {attack_type}{Style.RESET_ALL}")
    print(f"  → {message}")
    if ip:
        print(f"  → Source IP: {ip}")
    print(f"{color}{'='*60}{Style.RESET_ALL}")

    # Update Prometheus metrics
    attacks_total.labels(attack_type=attack_type).inc()
    last_attack_timestamp.set(time.time())
    attacking_ips.set(len(failed_attempts))

# ─── Detection Functions ───────────────────────────────────────
def detect_invalid_user(line):
    match = re.search(r'Invalid user (\w+) from ([\d.]+)', line)
    if match:
        username = match.group(1)
        ip = match.group(2)
        failed_attempts[ip].append(line)

        # Only alert on brute force threshold
        if len(failed_attempts[ip]) == BRUTE_FORCE_THRESHOLD:
            if ip not in alerted_ips:
                alerted_ips.add(ip)
                print_alert(
                    level="CRITICAL",
                    attack_type="BRUTE_FORCE",
                    message=f"IP {ip} made {len(failed_attempts[ip])} attempts targeting '{username}'",
                    ip=ip
                )
        return True
    return False


def detect_root_login(line):
    if "root" in line and "Invalid user" in line:
        match = re.search(r'from ([\d.]+)', line)
        ip = match.group(1) if match else "Unknown"
        print_alert(
            level="CRITICAL",
            attack_type="ROOT_ATTEMPT",
            message="Root login attempted via SSH",
            ip=ip
        )
        return True
    return False


# ─── Real-Time Log Watcher ─────────────────────────────────────
def watch_log_realtime(filepath):
    """
    Watches log file continuously — detects new attacks as they happen
    Like 'tail -f' but with threat detection built in
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print("   REAL-TIME SECURITY MONITOR")
    print("   Metrics available at: http://localhost:8000/metrics")
    print("   Grafana dashboard at: http://localhost:3000")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    try:
        with open(filepath, "r") as f:
            # First pass — process existing logs
            print(f"{Fore.YELLOW}📄 Processing existing logs...{Style.RESET_ALL}")
            for line in f:
                log_lines_processed.inc()
                detect_root_login(line)
                detect_invalid_user(line)

            print(f"{Fore.GREEN}✅ Existing logs processed{Style.RESET_ALL}")
            print(f"{Fore.CYAN}👁️  Watching for new attacks...{Style.RESET_ALL}\n")

            # Second pass — watch for new lines
            while True:
                line = f.readline()
                if line:
                    log_lines_processed.inc()
                    detect_root_login(line)
                    detect_invalid_user(line)
                else:
                    # No new lines — wait and try again
                    time.sleep(WATCH_INTERVAL)

    except FileNotFoundError:
        print(f"{Fore.RED}❌ Log file not found: {filepath}{Style.RESET_ALL}")
        return
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Monitor stopped by user{Style.RESET_ALL}")


# ─── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    print(f"{Fore.CYAN}🚀 Starting metrics server on port 8000...{Style.RESET_ALL}")
    start_http_server(8000)
    print(f"{Fore.GREEN}✅ Metrics server running{Style.RESET_ALL}")

    # Start real-time log monitoring
    watch_log_realtime(LOG_FILE)
