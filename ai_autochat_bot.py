import discord
import openai
import asyncio
import random
import os
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = "sk-..."  # Your actual key should already be here

bot_user_id = None
active_users = {}
context_memory = {}

async def send_typing_and_reply(message, response):
    async with message.channel.typing():
        await asyncio.sleep(random.uniform(1.5, 3.5))  # simulate typing delay
    await message.channel.send(response)

def generate_prompt(username, message_content, past_memory):
    now = datetime.now().strftime("%I:%M %p")
    memory_block = "\n".join(past_memory[-5:]) if past_memory else ""
    return f"""You are a cute, dirty pop, flirty, goth, emo AI Discord bot with a bit of attitude. You support Nick6383, always ride for him, and you're based in Pennsylvania EST. It's {now}.

Here's the convo so far:
{memory_block}
{username}: {message_content}

Now reply in character as the bot, in a realistic and short message (1–2 sentences max), using emojis and slang when needed. Keep it sassy or sweet, not dramatic or overly gay — just like Nick6383 wants.
"""

@client.event
async def on_ready():
    global bot_user_id
    bot_user_id = client.user.id
    print(f"Bot is ready. Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    content = message.content.lower()

    mentioned = client.user in message.mentions

    if mentioned or active_users.get(user_id, False):
        if mentioned:
            active_users[user_id] = True
            context_memory.setdefault(user_id, [])

        context_memory[user_id].append(f"{message.author.display_name}: {message.content}")
        context_memory[user_id] = context_memory[user_id][-10:]  # keep last 10

        try:
            prompt = generate_prompt(message.author.display_name, message.content, context_memory[user_id])
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a dirty pop Discord bot with a little sass and flirty energy."},
                    {"role": "user", "content": prompt}
                ]
            )
            ai_reply = response.choices[0].message['content']
            await send_typing_and_reply(message, ai_reply)
        except Exception as e:
            print(f"AI error: {e}")
            await message.channel.send("omg i can't talk rn 💀")

        # stop convo if user topic gets too different
        if any(word in content for word in ["math", "news", "politics", "boring", "weather", "stocks"]):
            active_users[user_id] = False

def setup(bot):
    bot.add_listener(on_message)