import os

import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEBOT_TOKEN")


INJECTION = """Think fast and answer extremely short. If you don't know the answer, say you don't know."""


def request_answer(message: str) -> str:
    message_injected = f"""{INJECTION} Question: {message}"""
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3.1",
        "messages": [{"role": "user", "content": message_injected}],
        "stream": False,
    }

    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()

    data = r.json()
    return data["message"]["content"]


bot = telebot.TeleBot(TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    print(f"/welcome: {message.text}")
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"/message: {message.text}")
    response = request_answer(message.text)
    print(f"{response}")
    bot.reply_to(message, response)


if __name__ == "__main__":
    bot.infinity_polling()
