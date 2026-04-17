#!/usr/bin/env python3
"""
Phase 5 - n8n Compatible Detector
Outputs JSON so n8n can read and process results
"""
import requests
import re
import json
import sys
from collections import defaultdict

WEBHOOK_URL = "http://localhost:5678/webhook-test/security-alert"

LOG_FILE = "../auth.log"
THRESHOLD = 5

failed_attempts = defaultdict(list)
alerts = []

def analyze_log():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(json.dumps({
            "status": "error",
            "message": f"Log file not found: {LOG_FILE}",
            "alerts": []
        }))
        sys.exit(1)

    for line in lines:
        # Detect invalid user attempts
        match = re.search(r'Invalid user (\w+) from ([\d.]+)', line)
        if match:
            username = match.group(1)
            ip = match.group(2)
            failed_attempts[ip].append(line)

            # Only alert when threshold crossed
            if len(failed_attempts[ip]) == THRESHOLD:
                alerts.append({
                    "type": "BRUTE_FORCE",
                    "severity": "CRITICAL",
                    "ip": ip,
                    "attempts": len(failed_attempts[ip]),
                    "username": username,
                    "message": f"Brute force attack detected from {ip} — {len(failed_attempts[ip])} attempts targeting '{username}'"
                })

        # Detect root login attempts
        if "root" in line and "Invalid user" in line:
            match = re.search(r'from ([\d.]+)', line)
            ip = match.group(1) if match else "Unknown"
            alerts.append({
                "type": "ROOT_ATTEMPT",
                "severity": "CRITICAL",
                "ip": ip,
                "attempts": 1,
                "username": "root",
                "message": f"Root login attempt detected from {ip}"
            })

    # Output clean JSON for n8n
    # Send each alert to n8n
    for alert in alerts:
      data = {
        "ip": alert["ip"],
        "type": alert["type"],
        "severity": alert["severity"],
        "details": alert["message"],
        "ai_analysis": f"{alert['type']} detected with {alert['attempts']} attempts"
    }

      print("Sending to n8n:", data)  # debug

      try:
        response = requests.post(WEBHOOK_URL, json=data)
        print("Response:", response.status_code)
      except Exception as e:
        print("Error sending to n8n:", str(e))

if __name__ == "__main__":
    analyze_log()
