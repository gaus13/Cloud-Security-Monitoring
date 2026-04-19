# Phase 1 — AWS Setup & Log Generation

## 🎯 What this phase does
Sets up the cloud infrastructure on AWS that generates
real security logs for our monitoring system to analyze.

---

## 🧠 Concepts Learned
| Concept | What it means |
|---------|--------------|
| EC2 | Virtual server on AWS cloud |
| CloudTrail | Records every AWS account activity |
| IAM | Controls who can access what on AWS |
| auth.log | Linux file that records all login attempts |
| SCP | Secure file copy between computers |

---

## 🏗️ What We Built

```
AWS Account
├── IAM User (security-project-user)
│   └── Safe access — not using root account
├── EC2 Instance (security-monitor)
│   ├── Ubuntu 22.04 LTS
│   ├── t2.micro (free tier)
│   ├── nginx installed
│   └── Generates auth.log with SSH attempts
└── CloudTrail (security-project-trail)
    ├── Multi-region logging enabled
    └── Logs stored in S3 bucket
```

---

## ⚙️ AWS Services Used

| Service | Purpose | Free Tier |
|---------|---------|-----------|
| EC2 t2.micro | Target server generating logs | 750 hrs/month ✅ |
| CloudTrail | AWS API activity logging | 1 trail free ✅ |
| S3 | Stores CloudTrail logs | 5GB free ✅ |
| IAM | User + permission management | Always free ✅ |

---

## 🔐 Security Best Practices Applied
- Never used root AWS account
- Created dedicated IAM user with scoped permissions
- Used SSH key pair instead of password for EC2
- Enabled CloudTrail for full audit logging

---

## 🚨 Attack Simulation

To generate real security logs we simulated brute force attacks:

```bash
# From local machine — simulate 6 failed SSH attempts
for i in {1..6}; do
  ssh wronguser@EC2_IP
done
```

This generated log entries like:
```
Invalid user wronguser from 152.58.116.*** port 6521*
Invalid user wronguser from 152.58.116.*** port 6522*
Invalid user fakeuser  from 152.58.116.*** port 6520*
```

---

## 📋 Setup Steps

### 1. Launch EC2 Instance
- OS: Ubuntu 22.04 LTS
- Type: t2.micro (free tier)
- Key pair: RSA .pem file
- Security group: SSH port 22 open

### 2. Enable CloudTrail
- Trail name: `security-project-trail`
- Multi-region: enabled
- S3 bucket: `security-logs-{account-id}`

### 3. Install nginx on EC2
```bash
sudo apt update && sudo apt install nginx -y
sudo systemctl start nginx
```

### 4. Simulate Attacks + Verify Logs
```bash
# On EC2 — verify logs captured
sudo tail -50 /var/log/auth.log | grep "Invalid user"
```

### 5. Copy Logs Locally
```bash
scp -i ~/.ssh/security-project-key.pem \
  ubuntu@EC2_IP:/var/log/auth.log \
  ./auth.log
```

---

## ⚠️ Free Tier Warning
Always **stop EC2** when not working:
- Stop = paused, no billing ✅
- Terminate = deleted forever ❌

AWS Console → EC2 → Instances → Instance State → **Stop**

---
