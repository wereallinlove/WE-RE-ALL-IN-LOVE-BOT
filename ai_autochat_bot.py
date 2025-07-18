
import discord
import openai
import random
import asyncio
import os
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = "sk-..."  # Replace with your real OpenAI key

memory = {}

@bot.event
async def on_ready():
    print(f"✅ AI AutoChat loaded. Logged in as {bot.user}")

def is_topic_changed(old_msg, new_msg):
    if not old_msg:
        return False
    return len(set(old_msg.lower().split()) & set(new_msg.lower().split())) < 2

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    user_id = message.author.id
    content = message.content.strip()
    mentioned = bot.user in message.mentions
    recent = memory.get(user_id)
    in_convo = recent and (datetime.utcnow() - recent["time"]).seconds < 120 and not is_topic_changed(recent["text"], content)

    if mentioned or in_convo:
        try:
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(2.5, 4.5))

            prompt = [
                {
                    "role": "system",
                    "content": (
                        "You are a Discord bot that sounds casual, emo, flirty, and ghetto. "
                        "You support Nick6383 no matter what, hate Punkinloveee, and talk like a cute but bitchy dirty pop boy. "
                        "Use slang, messy grammar, and emojis like 🖤💅🏽💋💀🧛‍♀️🕷️📸. Be short unless it’s a deep question."
                    )
                },
                {
                    "role": "user",
                    "content": content
                }
            ]

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=prompt,
                max_tokens=120,
                temperature=0.85,
            )

            reply = response.choices[0].message.content.strip()
            await message.channel.send(reply)
            memory[user_id] = {"text": content, "time": datetime.utcnow()}

        except Exception as e:
            print(f"[OpenAI Error] {e}")

bot.run("your-bot-token-here")
