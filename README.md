# Mailer3000

**Fake Email Generator Telegram Bot + Inbox Checker (Python)**
Automated temp email generation and inbox monitoring controlled via Telegram.

---

## 🚀 Overview

**Mailer3000** is a Python-based Telegram bot that allows users to:

* Generate fake / temporary email addresses
* Monitor inboxes for incoming emails
* Control everything directly from Telegram commands

This project is intended for **testing, automation, and sandboxing email workflows**. It is *not* meant for abuse or spam.

---

## 🧠 Features

* 📧 **Fake / Temporary Email Generation**
  Creates disposable email addresses using supported providers.

* 📥 **Inbox Checking**
  Fetches and displays incoming emails for generated addresses.

* 🤖 **Telegram Bot Interface**
  Simple command-based interaction via Telegram Bot API.

* 🔌 **Modular Design**
  Easy to swap email providers or extend functionality.

---

## 🧰 Tech Stack

| Component          | Technology        |
| ------------------ | ----------------- |
| Language           | Python 3.10+      |
| Bot API            | Telegram Bot API  |
| HTTP               | requests          |
| Async / Scheduling | asyncio / polling |
| Config             | dotenv / env vars |

---

## 🛠 Setup

### ⚡ Prerequisites

* Python 3.10 or higher
* Telegram Bot Token (from @BotFather)
* Temp email provider API (optional, depending on implementation)

---

### 📦 Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

---

## 🔑 Configuration

Create a `.env` file in the root directory:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
EMAIL_API_KEY=your_email_api_key
EMAIL_PROVIDER=provider_name
```

---

## ▶️ Running the Bot

```bash
python bot.py
```

The bot will connect to Telegram and start listening for commands.

---

## 🤖 Telegram Commands

| Command  | Description                |
| -------- | -------------------------- |
| `/start` | Initialize bot & show help |
| `/new`   | Generate a new fake email  |
| `/check` | Check inbox for messages   |
| `/help`  | Show available commands    |

---

## 🧩 How It Works

1. User sends `/new`
2. Bot generates a temporary email address
3. Address is returned via Telegram
4. User sends `/check`
5. Bot polls inbox provider
6. Incoming emails are displayed
---

## 👤 Author

**Nayan**
GitHub: [https://github.com/nayan2723](https://github.com/nayan2723)

If you liked this project, feel free to ⭐ the repo.
