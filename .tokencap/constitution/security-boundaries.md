# Security Boundaries

> TokenCap Constitution Engine

## 🔴 CONST-SEC-A2EA57 — CRITICAL

**Environment variable files (.env) must never be committed to version control.**

> **Why:** .env files contain secrets. Committing them exposes credentials to all repository users.

> **What breaks:** All secrets in .env become public. Immediate security incident.

*Files:* `.env`, `.env.example`
