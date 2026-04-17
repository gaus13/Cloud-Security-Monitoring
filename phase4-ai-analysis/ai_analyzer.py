#!/usr/bin/env python3

import re
import os
import json
from groq import Groq
from collections import defaultdict
from datetime import datetime
from colorama import Fore, Style, init
from dotenv import load_dotenv

# ─── Load Environment ─────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

init()

LOG_FILE = "../auth.log"
BRUTE_FORCE_THRESHOLD = 5

failed_attempts = defaultdict(list)
alerts_detected = []

# ─── AI ANALYSIS FUNCTION ─────────────────────────────
def analyze_with_ai(alert_type, details, ip):
    print(f"{Fore.CYAN}🤖 Sending to AI...{Style.RESET_ALL}")

    prompt = f"""
You are a cybersecurity AI.

Analyze this alert and respond ONLY in valid JSON.

Alert:
Type: {alert_type}
Details: {details}
IP: {ip}
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Return JSON:
{{
  "severity": "HIGH/MEDIUM/LOW",
  "attack_type": "string",
  "explanation": "short explanation",
  "risk": "short risk",
  "actions": ["action1", "action2", "action3"]
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        ai_text = response.choices[0].message.content.strip()

        try:
            return json.loads(ai_text)
        except:
            return {"raw": ai_text}

    except Exception as e:
        return {"error": str(e)}


# ─── BEAUTIFUL OUTPUT ─────────────────────────────
def print_alert(ip, details, ai):
    print(f"\n{Fore.RED}{'='*70}")
    print(f"🚨 SECURITY ALERT DETECTED")
    print(f"{'='*70}")

    print(f"🌐 IP Address   : {ip}")
    print(f"📝 Details      : {details}")

    if "error" in ai:
        print(f"\n❌ AI Error: {ai['error']}")
        return

    if "raw" in ai:
        print(f"\n⚠️ Raw AI Output:\n{ai['raw']}")
        return

    print(f"\n🔍 AI ANALYSIS")
    print(f"{'-'*70}")

    print(f"⚠️  Severity     : {ai.get('severity', 'N/A')}")
    print(f"🎯 Attack Type  : {ai.get('attack_type', 'N/A')}")
    print(f"📖 Explanation  : {ai.get('explanation', 'N/A')}")
    print(f"💥 Risk         : {ai.get('risk', 'N/A')}")

    print(f"\n🛡️ Recommended Actions:")
    for i, action in enumerate(ai.get("actions", []), 1):
        print(f"   {i}. {action}")

    print(f"{'='*70}{Style.RESET_ALL}\n")

    # 🔥 JSON output for automation (n8n, agents)
    structured_output = {
        "timestamp": datetime.now().isoformat(),
        "ip": ip,
        "details": details,
        "analysis": ai
    }

    print("📦 JSON OUTPUT (for automation):")
    print(json.dumps(structured_output, indent=2))

    alerts_detected.append(ip)


# ─── DETECTION LOGIC ─────────────────────────────
def detect(line):
    match = re.search(r'Invalid user (\w+) from ([\d.]+)', line)

    if match:
        user = match.group(1)
        ip = match.group(2)

        failed_attempts[ip].append(line)

        if len(failed_attempts[ip]) == BRUTE_FORCE_THRESHOLD:
            details = f"{len(failed_attempts[ip])} failed attempts using '{user}'"

            ai = analyze_with_ai("Brute Force Attack", details, ip)

            print_alert(ip, details, ai)


# ─── MAIN ─────────────────────────────
def main():
    print(f"\n{Fore.CYAN}{'='*70}")
    print("🚀 AI-POWERED SECURITY ANALYZER (GROQ)")
    print(f"{'='*70}{Style.RESET_ALL}\n")

    if not GROQ_API_KEY:
        print(f"{Fore.RED}❌ GROQ_API_KEY missing in .env{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}✅ API Key Loaded{Style.RESET_ALL}")
    print(f"📄 Reading log file: {LOG_FILE}\n")

    try:
        with open(LOG_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Log file not found{Style.RESET_ALL}")
        return

    print(f"📊 Total lines: {len(lines)}")
    print(f"{Fore.YELLOW}🔍 Scanning...{Style.RESET_ALL}\n")

    for line in lines:
        detect(line)

    print(f"\n{Fore.CYAN}{'='*70}")
    print("📊 FINAL SUMMARY")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"🚨 Alerts Generated: {len(alerts_detected)}")

    print("\n🌐 Attacking IPs:")
    for ip, attempts in failed_attempts.items():
        print(f"   {Fore.RED}{ip}{Style.RESET_ALL} → {len(attempts)} attempts")

    print(f"\n{Fore.GREEN}✅ Analysis Complete{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
