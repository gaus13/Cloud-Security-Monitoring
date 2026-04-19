# Phase 3 — Python Threat Detection

## 🎯 What this phase does
Automatically reads security logs and detects real attack patterns
using Python — no manual log reading needed. This is the core
**SOC analyst logic** translated into code.

---

## 🧠 Concepts Learned

| Concept | What it means |
|---------|--------------|
| SOC | Security Operations Center — team that monitors threats |
| Brute Force | Attacker tries many passwords until one works |
| Threshold Detection | Alert only after X attempts — reduces false alarms |
| Regex | Pattern matching to extract data from log text |
| defaultdict | Python dict that auto-creates keys — perfect for counting attempts per IP |

---

## 🚨 Threats Detected

### 1. Brute Force Attack
```
Condition:  5+ failed attempts from same IP
Log pattern: "Invalid user <name> from <ip>"
Severity:   CRITICAL 🔴
```

### 2. Invalid User Attempt  
```
Condition:  Login attempt with non-existent username
Log pattern: "Invalid user <name> from <ip>"
Severity:   HIGH 🟡
```

### 3. Root Login Attempt
```
Condition:  Anyone trying to login as root
Log pattern: "Invalid user root" or "Failed password for root"
Severity:   CRITICAL 🔴
```

---

## 🏗️ How Detection Works

```
Read auth.log line by line
        ↓
Apply regex patterns to each line
        ↓
Match found? → Extract IP + username
        ↓
Track attempts per IP using dictionary
        ↓
IP crosses threshold? → Generate alert
        ↓
Print color-coded alert to terminal
        ↓
Store alert for Phase 4 AI analysis
```

---

## 🐍 Core Detection Logic

```python
# Track failed attempts per IP
failed_attempts = defaultdict(list)

# When invalid user found
if len(failed_attempts[ip]) == THRESHOLD:
    # Trigger brute force alert
    generate_alert("CRITICAL", ip)
```

**Why threshold = 5?**
One failed login = human mistake.
Five failed logins from same IP = automated attack.
This reduces false positives significantly.

---

## 🚀 How to Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run detector
python3 phase3-detection/detector.py
```

---

## 📊 Sample Output

```
============================================================
   CLOUD SECURITY THREAT DETECTOR
   Analyzing: auth.log
============================================================

📄 Total log lines to analyze: 207

[2026-04-16 12:00:01] [HIGH] INVALID USER ATTEMPT
  → Someone tried to login as non-existent user 'wronguser'
  → Source IP: 152.58.116.109

[2026-04-16 12:00:03] [CRITICAL] BRUTE FORCE ATTACK DETECTED
  → IP 152.58.116.109 made 5 failed attempts
  → Source IP: 152.58.116.109

============================================================
   DETECTION SUMMARY
============================================================
📊 Total lines scanned:    207
⚠️  Total threats detected: 9

🌐 Attacking IPs:
   152.58.116.109 → 9 attempts

✅ Scan complete.
```

---

## 🎨 Alert Color System

| Color | Level | Meaning |
|-------|-------|---------|
| 🔴 Red | CRITICAL | Immediate action required |
| 🟡 Yellow | HIGH | Investigate soon |
| 🔵 Cyan | INFO | Awareness only |

---

## 📁 Files

| File | Purpose |
|------|---------|
| `detector.py` | Main threat detection script |
| `auth.log` | Sample log file with real attack data |

---

## 💡 Key Learnings

- How SOC analysts think about threat detection
- Why regex is essential for log analysis
- Threshold-based alerting to reduce false positives
- How to track attacker behavior across multiple log lines
- Color-coded terminal output for quick threat triage

---

## 📸 Screenshot

![Threat Detection Output](../phase3-detection-one.png)
