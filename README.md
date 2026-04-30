# Cloud-Security-Monitoring

# 🔐 Cloud Security Monitoring + AI Alert System

A real-world cloud security monitoring system that automatically detects threats,
analyzes them using AI, and sends instant alerts via Slack — built to simulate
how modern SOC teams operate. 

---
## 🏗️ Architecture

```mermaid
flowchart TD
    A[🖥️ AWS EC2 Ubuntu Server] -->|Generates SSH logs| B[📄 auth.log]
    B -->|Shipped by Filebeat| C[🔍 Elasticsearch]
    C -->|Visualized by| D[📊 Kibana SIEM Dashboard]
    C -->|Read by| E[🐍 Python Threat Detector]
    
    E -->|Brute Force Detected| F{🚨 Threat Found?}
    E -->|Invalid User Detected| F
    E -->|Root Login Detected| F
    
    F -->|YES| G[🤖 AI Analyzer - Groq Mistral]
    F -->|NO| H[✅ No Action Needed]
    
    G -->|Alert + Explanation| I[⚡ n8n Automation Workflow]
    I -->|Instant Notification| J[💬 Slack Alert]

    style A fill:#FF9900,color:#000
    style C fill:#005571,color:#fff
    style D fill:#005571,color:#fff
    style E fill:#3776AB,color:#fff
    style G fill:#7C3AED,color:#fff
    style I fill:#EA4B71,color:#fff
    style J fill:#4A154B,color:#fff
    style F fill:#DC2626,color:#fff
```

## 📌 Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | AWS Setup (EC2 + CloudTrail) | ✅ Complete |
| Phase 2 | ELK Stack SIEM Setup | ✅ Complete  |
| Phase 3 | Threat Detection (Python) | ✅ Complete  |
| Phase 4 | AI Alert Analysis (Claude API) | ✅ Complete  |
| Phase 5 | Automation with n8n | ✅ Complete |
| Phase 6 | Slack Notifications | ✅ Complete |

---

## 🛠️ Tech Stack

- **AWS** — EC2, CloudTrail, S3, IAM
- **ELK Stack** — Elasticsearch, Kibana, Filebeat
- **Python** — Threat detection logic
- **Claude API** — AI-powered alert explanation
- **n8n** — Workflow automation
- **Slack** — Real-time alerting
- **Docker** — Container orchestration
## 📸 Screenshots

### 🔍 Kibana Logs
<img src="screenshots/kibana-discover.png" width="700"/>

### 🚨 Detection Alerts
<img src="screenshots/phase3-detection-one.png" width="700"/>
<img src="screenshots/phase3-detection-two.png" width="700"/>

### 📩 Slack Alert Integration
<img src="screenshots/slack-alert.png" width="700"/>
---

---

## 🚀 How to Run This Project


### Prerequisites
- AWS Account (free tier)
- Docker Desktop
- Python 3.x
- Groq API key (free)
- Slack workspace

### 1. Clone the repo
```bash
git clone https://github.com/gaus13/Cloud-Security-Monitoring.git
cd Cloud-Security-Monitoring
```

### 2. Setup virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv colorama python-dateutil
```

### 3. Create .env file
```bash
cp .env.example .env
# Add your API keys to .env
```

### 4. Start ELK Stack
```bash
cd phase2-elk-stack
docker compose up -d
```

### 5. Run threat detection
```bash
python3 phase3-detection/detector.py
```

### 6. Run AI analyzer
```bash
python3 phase4-ai-analysis/ai_analyzer.py
```

### 7. Start n8n automation
```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n
# Import workflow from phase5-automation/n8n-workflow.json
```
---

## 👤 Author
Gulam Gaus

