import random
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
# Used to track who has already played in each group
used_users = {}

# Sample truth and dare questions

TRUTH_QUESTIONS = [
    "What's your most embarrassing song on repeat?",
    "What's one thing you're secretly good at?",
    "If you could switch lives with someone for a day, who would it be?",
    "What's your biggest irrational fear?",
    "What's the most spontaneous thing you've ever done?",
    "If animals could talk, which would be the rudest?",
    "What's your go-to procrastination activity?",
    "If you had a theme song, what would it be?",
    "What's the craziest thing you've ever eaten?",
    "If you could have any superpower for a day, what would it be?",
    "What's something you're proud of accomplishing?",
    "What's one thing you can't live without in your daily routine?",
    "If you could have dinner with any fictional character, who would it be?",
    "What's your favorite childhood memory?",
    "What's something you're looking forward to doing soon?",
    "If you could relive any day, which would it be?",
    "What's the best advice you've ever received?",
    "If you could travel anywhere instantly, where would you go?",
    "What's your favorite way to relax?",
    "If you could switch roles with someone for a day, who would it be and why?"
]

DARE_QUESTIONS = [
    "Send a flirty pickup line — cheesy or original.",
    "Text a random emoji to your crush (or pretend you did 😏).",
    "Change your profile name to 'Cutie of the Chat' for 15 mins.",
    "Send a voice note pretending you're confessing to your crush.",
    "Type a message like you're madly in love with the next player who replies.",
    "Use a GIF to describe your last crush.",
    "Reveal the initials of someone you’ve had a crush on.",
    "Send a fake love letter starting with 'Dear Stranger...'",
    "Pretend you're on a dating app and write your bio in 3 lines.",
    "Compliment another player like you're flirting (keep it fun, not creepy).",
    "Send a selfie captioned as if it’s your dating profile.",
    "Create a dramatic breakup message with an imaginary partner.",
    "Tell the group your most harmless guilty pleasure.",
    "Send a heart emoji to 3 people in the main chat (no repeats).",
    "Name a toxic movie character you secretly find attractive.",
    "Pretend you're on a romantic reality show — introduce yourself (vn).",
    "Write a romantic poem... about pizza or food.",
    "Reveal a minor secret that you've never told anyone here.",
    "Send a message using only 🔥, 💋, 💖, 😳 emojis.",
    "Type your next message as if you're love-struck."
]


def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message and brief instructions."""
    if update.message.chat.type != 'private':
        update.message.reply_text("👋 Please DM me to use /start!")
        return

    update.message.reply_text(
        "Welcome to the Truth or Dare Bot! 🎉\n"
        "Use /truth or /dare to play — works in group chats too!\n"
        "Type /reset in a group to start a new round!"
    )

def truth(update: Update, context: CallbackContext) -> None:
    """Send a random Truth question."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if chat_id not in used_users:
        used_users[chat_id] = set()

    if user_id in used_users[chat_id]:
        update.message.reply_text(f"⚠️ {user_name}, you've already played this round. Wait for /reset.")
        return

    question = random.choice(TRUTH_QUESTIONS)
    update.message.reply_text(f"🤫 *Truth for {user_name}*: {question}", parse_mode='Markdown')
    used_users[chat_id].add(user_id)

def dare(update: Update, context: CallbackContext) -> None:
    """Send a random Dare challenge."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if chat_id not in used_users:
        used_users[chat_id] = set()

    if user_id in used_users[chat_id]:
        update.message.reply_text(f"⚠️ {user_name}, you've already played this round. Wait for /reset.")
        return

    challenge = random.choice(DARE_QUESTIONS)
    update.message.reply_text(f"😈 *Dare for {user_name}*: {challenge}", parse_mode='Markdown')
    used_users[chat_id].add(user_id)

def reset(update: Update, context: CallbackContext) -> None:
    """Reset the round so users can play again."""
    chat_id = update.effective_chat.id
    used_users[chat_id] = set()
    update.message.reply_text("🔁 New round started! Everyone can play again.")

def main() -> None:
    """Start the bot and register handlers."""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("truth", truth))
    dispatcher.add_handler(CommandHandler("dare", dare))
    dispatcher.add_handler(CommandHandler("reset", reset))

    # Start the bot
    updater.start_polling()
    print("Bot started. Listening for commands...")
    updater.idle()

if __name__ == "__main__":
    main()
