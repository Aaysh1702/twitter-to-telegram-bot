# Twitter to Telegram Bot

A powerful and self-healing Python bot that automatically forwards tweets from selected Twitter (X) accounts to your Telegram channel or chat in real-time.

---

## Features

- Track tweets from up to 5 Twitter accounts per user
- Free plan supports tracking for 1 or 2 accounts
- Premium support for up to 5 accounts per user
- Self-healing: Automatically restarts after failures (rate limit errors, connection issues, etc.)
- Runs 24/7 on free cloud hosting (Render, Railway, Fly.io, etc.)
- User-friendly Telegram bot interaction:
  - Start with `/start`
  - Select between Free or Premium
  - Secure UPI payment for upgrades
- Admin payment verification system:
  - Users send payment screenshot
  - Bot forwards to admin for approval

---

## Requirements

- Python 3.10+
- Twitter API (X API v2)
- Telegram Bot Token
- PostgreSQL or key-value database (free tier supported)
- Free hosting (Render/Fly.io/Deta/FastAPI compatible)

---

## Installation

1. **Clone the Repo**
   ```bash
   git clone https://github.com/Aaysh1702/twitter-telegram-bot.git
   cd twitter-telegram-bot
