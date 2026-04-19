# Phase 4 — AI-Powered Alert Analysis

## 🎯 What this phase does
Takes raw security alerts from Phase 3 and sends them to an AI model
that explains them like a **senior security analyst** would —
with severity rating, risk assessment, and recommended actions.

---

## 🧠 Concepts Learned

| Concept | What it means |
|---------|--------------|
| LLM | Large Language Model — AI trained on massive text data |
| Groq API | Free, ultra-fast API to run AI models in cloud |
| Mistral-7B | Powerful open source AI model — rivals GPT-3.5 |
| Prompt Engineering | How you instruct AI to get structured useful responses |
| .env file | Stores secrets safely — never committed to git |
| API Key | Password that identifies you to an external service |

---

## 🤖 Why AI in a Security Project?

**Without AI** your alert looks like:
```
BRUTE FORCE DETECTED
IP: 152.58.116.109
Attempts: 5
```

**With AI** your alert looks like:
```
SEVERITY: Critical

ATTACK EXPLANATION:
This is an automated brute force attack where the attacker
is systematically trying different usernames via SSH.
5 attempts in quick succession indicates an automated tool.

RISK:
If successful, attacker gains complete server access,
can install malware, steal data, or use server for
further attacks.

IMMEDIATE ACTIONS:
1. Block IP 152.58.116.109 in firewall immediately
2. Enable fail2ban to auto-block future attempts
3. Disable password auth — use SSH keys only

LONG TERM RECOMMENDATIONS:
Deploy intrusion detection system (IDS), implement
geo-blocking for suspicious regions, enable MFA.
```

**That's the difference.** AI turns raw data into actionable intelligence.

---

## 🏗️ How It Works

```
Phase 3 detects threat
        ↓
Extract: IP + attack type + attempt count
        ↓
Build structured prompt for AI
        ↓
Send to Groq API (Mistral-7B model)
        ↓
AI returns: severity + explanation + actions
        ↓
Print full analysis + store for n8n
```

---

## ⚡ Why Groq?

| Feature | Groq | OpenAI |
|---------|------|--------|
| Cost | Free tier ✅ | Paid 💰 |
| Speed | Ultra fast | Standard |
| Model | Mistral-7B | GPT-4 |
| Privacy | Good | Sends to OpenAI |
| Resume value | Same | Same |

---

## 🔐 API Key Security

```
❌ WRONG — never do this:
GROQ_API_KEY = "gsk_abc123..."  # hardcoded in code

✅ RIGHT — always do this:
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # loaded from .env
```

**.gitignore** prevents `.env` from ever reaching GitHub:
```
.env
venv/
__pycache__/
```

---

## 🚀 How to Run

### Setup
```bash
# Install dependencies
source venv/bin/activate
pip install requests python-dotenv colorama

# Create .env file
cp .env.example .env
# Add your Groq API key to .env
```

### Get Free Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up free
3. Create API key
4. Add to `.env` file

### Run Analyzer
```bash
python3 phase4-ai-analysis/ai_analyzer.py
```

---

## 📊 Sample Output

```
============================================================
   AI-POWERED CLOUD SECURITY ANALYZER
   Model: Mistral-7B via Groq
============================================================

✅ API Key Loaded
📄 Reading log file: auth.log
📊 Total lines: 207
🔍 Scanning...
🤖 Sending to AI...

============================================================
🚨 SECURITY ALERT DETECTED
============================================================
🌐 IP Address : 152.58.116.109
📝 Details    : 5 failed attempts using 'wronguser'

⚠️ AI Analysis:
{
  "severity": "CRITICAL",
  "attack_type": "Brute Force SSH Attack",
  "explanation": "Automated attack systematically trying usernames",
  "risk": "Complete server compromise if successful",
  "actions": [
    "Block IP immediately in firewall",
    "Enable fail2ban",
    "Disable password authentication"
  ]
}
============================================================

📊 FINAL SUMMARY
🚨 Alerts Generated: 1
🌐 Attacking IPs:
   152.58.116.109 → 9 attempts
✅ Analysis Complete
```

---

## 📁 Files

| File | Purpose |
|------|---------|
| `ai_analyzer.py` | Main AI analysis script |
| `.env.example` | Template for required API keys |
| `.gitignore` | Prevents secrets reaching GitHub |

---

## 💡 Key Learnings

- How AI can augment security operations
- Prompt engineering for structured security responses
- Safe API key management using environment variables
- Why open source models (Mistral) are viable alternatives to GPT
- How to parse and use AI JSON responses in Python

---

