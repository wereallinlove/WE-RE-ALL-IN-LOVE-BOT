import discord
import openai
import random
import time

from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = "sk-..."  # your actual full key is inserted here by me

memory = {}  # saves recent convo by user
typing_delay = (1.5, 3.5)

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

    # Bot was directly mentioned
    mentioned = bot.user in message.mentions

    # Continue convo if previously mentioned and topic didn’t change too hard
    recent = memory.get(user_id)
    in_convo = recent and (datetime.utcnow() - recent["time"]).seconds < 90 and not is_topic_changed(recent["text"], content)

    if mentioned or in_convo:
        # simulate typing
        async with message.channel.typing():
            await discord.utils.sleep_until(datetime.utcnow() + 
                discord.utils.timedelta(seconds=random.uniform(*typing_delay)))

        prompt = [
            {"role": "system", "content": (
                "You are a Discord bot with a chill, dirty pop, funny, flirty, edgy, and emotional vibe. "
                "You support user Nick6383, hate Punkinloveee, talk in casual messy grammar, and sound a little bitchy but lovable. "
                "You use ghetto and girly slang, emoji, and react to images if they're sent. Keep replies short unless the message needs more."
            )},
            {"role": "user", "content": content}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=prompt,
                max_tokens=100,
                temperature=0.8
            )

            reply = response.choices[0].message.content.strip()
            await message.channel.send(reply)
            memory[user_id] = {"text": content, "time": datetime.utcnow()}
        except Exception as e:
            print(f"OpenAI error: {e}")

bot.run("your-bot-token-here")