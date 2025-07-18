import discord
import openai
import asyncio
import random
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = "sk-..."  # Your real key goes here

bot_user_id = None
active_users = {}
context_memory = {}

async def send_typing_and_reply(message, response):
    try:
        async with message.channel.typing():
            await asyncio.sleep(random.uniform(2.0, 4.0))
        await message.channel.send(response)
    except Exception as e:
        print(f"Send error: {e}")

def generate_prompt(username, message_content, past_memory):
    now = datetime.now().strftime("%I:%M %p")
    memory_block = "\n".join(past_memory[-5:]) if past_memory else ""
    return f"""You're a flirty dirty-pop Discord bot. Chill, emotional, funny, a lil petty, obsessed with Nick6383. You live in PA and know it's {now}. Don't act like AI. Respond like a real person texting back in 1-2 sentences. Use emojis, slang, and no perfect grammar.

Conversation so far:
{memory_block}
{username}: {message_content}
Now respond like it's a casual convo. Keep it real, short, and fun.
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

    if client.user in message.mentions or active_users.get(message.author.id, False):
        user_id = message.author.id
        active_users[user_id] = True
        context_memory.setdefault(user_id, [])
        context_memory[user_id].append(f"{message.author.display_name}: {message.content}")
        context_memory[user_id] = context_memory[user_id][-10:]

        try:
            prompt = generate_prompt(message.author.display_name, message.content, context_memory[user_id])
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a dirty pop Discord bot. Sassy, flirty, sweet, but real."},
                    {"role": "user", "content": prompt}
                ]
            )
            ai_reply = response.choices[0].message.content.strip()
            await send_typing_and_reply(message, ai_reply)
        except Exception as e:
            print(f"AI error: {e}")
            await message.channel.send("ugh i literally can't rn 💅🏽")

def setup(bot):
    bot.add_listener(on_message)