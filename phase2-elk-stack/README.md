# Phase 2 — ELK Stack SIEM Setup

## 🎯 What this phase does
Sets up a complete SIEM (Security Information and Event Management)
system using the ELK Stack running on Docker. Collects logs from
AWS EC2 and visualizes attack patterns on a real dashboard.

---

## 🧠 Concepts Learned

| Concept | What it means |
|---------|--------------|
| SIEM | Central system that collects and analyzes security logs |
| Elasticsearch | Super fast database built for searching logs |
| Kibana | Visual dashboard for logs — like Google Analytics for security |
| Filebeat | Lightweight agent that ships logs to Elasticsearch |
| Docker | Runs all 3 tools in isolated containers with one command |
| Index Pattern | Tells Kibana which logs to display |

---

## 🏗️ Architecture

```
AWS EC2 (auth.log)
      ↓
Filebeat (log shipper)
      ↓
Elasticsearch (stores + indexes logs)
      ↓
Kibana (visual dashboard)
```

---

## 🛠️ Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| Elasticsearch | 8.12.0 | Log storage and search engine |
| Kibana | 8.12.0 | Visualization dashboard |
| Filebeat | 8.12.0 | Log shipping agent |
| Docker | Latest | Container orchestration |

---

## ⚙️ Configuration

### Docker Compose Setup
All 3 tools launched with single command:
```bash
docker compose up -d
```

### RAM Optimization
Elasticsearch limited to 1GB RAM to prevent system freeze:
```yaml
ES_JAVA_OPTS=-Xms1g -Xmx1g
```

### Filebeat Configuration
Watches auth.log and ships to Elasticsearch:
```yaml
filebeat.inputs:
- type: log
  paths:
    - /usr/share/filebeat/logs/auth.log
output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "security-logs-%{+yyyy.MM.dd}"
```

---

## 🚀 How to Run

### Prerequisites
- Docker Desktop installed
- WSL2 (Windows users)
- Minimum 4GB free RAM

### Start ELK Stack
```bash
cd phase2-elk-stack
docker compose up -d
```

### Verify all containers running
```bash
docker compose ps
```

Expected output:
```
NAME            STATUS
elasticsearch   Up
kibana          Up
filebeat        Up
```

### Check logs are indexed
```bash
curl "http://localhost:9200/security-logs-*/_count"
# Should return count > 0
```

### Open Kibana Dashboard
```
http://localhost:5601
```

### Stop when done (saves RAM)
```bash
docker compose stop
```

---

## 📊 Kibana Setup Steps

1. Open `http://localhost:5601`
2. Click **"Explore on my own"**
3. Go to **Stack Management → Data Views**
4. Create data view:
   - Name: `security-logs`
   - Index pattern: `security-logs-*`
   - Timestamp: `@timestamp`
5. Go to **Discover**
6. Search: `Invalid user`
7. See all brute force attempts visualized ✅

---

## 🔍 What We Can See in Kibana

| Search Query | What it shows |
|-------------|--------------|
| `Invalid user` | All brute force attempts |
| `Failed password` | Password based attacks |
| `Accepted publickey` | Successful logins |
| `sudo` | Privilege escalation attempts |

---

## 📈 Results

After setup we could see:
- **120+ log entries** indexed in Elasticsearch
- **77 hits** for `Invalid user` search
- Attack timeline showing spikes of activity
- Source IP `152.58.116.109` responsible for all attacks

---

## ⚠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| Filebeat exits immediately | Run `sudo chown root:root filebeat.yml` |
| Kibana won't load | Wait 2-3 minutes — it's slow to start |
| No logs in Kibana | Check `curl localhost:9200/security-logs-*/_count` |
| Out of memory | Reduce ES_JAVA_OPTS to `-Xms512m -Xmx512m` |

---

## 📸 Screenshots

### Kibana Discover — Brute Force Attacks Visible
![Kibana Dashboard](../screenshots/phase2-kibana-dashboard.png)

---

## 💡 Key Learnings

- How real companies use ELK as their SIEM platform
- Why Filebeat is preferred over Logstash for simple log shipping
- How to search and filter security events in Kibana
- Docker networking — how containers talk to each other privately
- Index patterns and time-based log organization
