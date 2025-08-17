from keep_alive import keep_alive
import requests
import logging
import random
import string
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Stores user_id: { email, password, token }
user_data = {}

BASE_URL = "https://api.mail.gw"


def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def start(update: Update, context: CallbackContext):
    update.message.reply_text("📬 Welcome to Mailer3000 powered by Mail.gw!\n"
                              "Use /newmail to generate a temp email.\n"
                              "Use /checkmail to see inbox messages.")


def newmail(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    try:
        # Get domain
        domain_resp = requests.get(f"{BASE_URL}/domains")
        domain_resp.raise_for_status()
        domain = domain_resp.json()['hydra:member'][0]['domain']

        # Create email & password
        email = f"{random_string()}@{domain}"
        password = random_string(12)

        # Register account
        reg_resp = requests.post(f"{BASE_URL}/accounts",
                                 json={
                                     "address": email,
                                     "password": password
                                 })

        if reg_resp.status_code != 201:
            raise Exception("Email creation failed")

        # Get token
        token_resp = requests.post(f"{BASE_URL}/token",
                                   json={
                                       "address": email,
                                       "password": password
                                   })

        token = token_resp.json()["token"]
        user_data[user_id] = {
            "email": email,
            "password": password,
            "token": token
        }

        update.message.reply_text(f"✅ Temp email created:\n`{email}`",
                                  parse_mode="Markdown")

    except Exception as e:
        logging.error(f"newmail error: {e}")
        update.message.reply_text("❌ Failed to create email. Try again later.")


def checkmail(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    creds = user_data.get(user_id)

    if not creds:
        update.message.reply_text(
            "⚠️ No temp email found. Use /newmail first.")
        return

    try:
        headers = {"Authorization": f"Bearer {creds['token']}"}
        mail_resp = requests.get(f"{BASE_URL}/messages", headers=headers)
        mail_resp.raise_for_status()
        messages = mail_resp.json()["hydra:member"]

        if not messages:
            update.message.reply_text("📭 Inbox empty.")
            return

        for msg in messages:
            msg_id = msg["id"]
            full_msg_resp = requests.get(f"{BASE_URL}/messages/{msg_id}",
                                         headers=headers)
            full_msg_resp.raise_for_status()
            full_msg = full_msg_resp.json()

            sender = full_msg['from']['address']
            subject = full_msg.get("subject", "(No subject)")
            body = full_msg.get("text", "(No content)")

            update.message.reply_text(
                f"📩 *New Mail!*\nFrom: `{sender}`\nSubject: `{subject}`\n\n{body[:500]}",
                parse_mode="Markdown")

    except Exception as e:
        logging.error(f"checkmail error: {e}")
        update.message.reply_text("⚠️ Could not fetch inbox. Try again later.")


def main():
    logging.basicConfig(level=logging.INFO)
    keep_alive()

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("newmail", newmail))
    dp.add_handler(CommandHandler("checkmail", checkmail))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()