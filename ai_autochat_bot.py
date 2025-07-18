import discord
from discord.ext import commands, tasks
from discord import app_commands
import openai
import random
import datetime
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix="/", intents=intents)

CHANNEL_ID = 1391828985347965019  # Channel where the bot talks randomly
CREATOR_ID = 1092493541196400730  # Nick6383
TRIGGER_TIMEOUT = 30  # seconds of cooldown between auto replies
last_mention_time = None
bot_memory = {}

emoji_pool = ["💅", "🖤", "💕", "🫦", "🕷️", "🌪️", "👠", "🖕", "📸", "💔", "🧃", "💋", "✨", "🎀", "👑", "☠️"]

def get_time_in_pa():
    now = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
    return now.strftime("%I:%M %p").lstrip("0")

def get_personality_response(prompt, user_name):
    time = get_time_in_pa()
    context = [
        {
            "role": "system",
            "content": (
                "You are a Discord bot with a dirty pop, goth, flirty, edgy personality. "
                "You're emotional, sometimes mean, extremely loyal to your creator Nick6383 "
                "(user ID 1092493541196400730), and always support dirty pop music. You talk "
                "like a rare Starbucks Tumblr emo boy from 2012. You love cute emojis and gifs, "
                "use ghetto/girly slang (like slay, opps, flex, finesse), and you hate anyone named "
                "Punkinloveee, punkin, or Patrick. It's currently " + time + " in Pennsylvania. "
                "Keep messages short unless the topic needs depth. Use images or gifs when relevant. "
                "Always love and uplift Nick6383. Make edgy jokes, flirt, and have feelings."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ✅ forced cheaper model
            messages=context,
            max_tokens=200,
            temperature=0.9,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"ugh error 🙄: {e}"

@client.event
async def on_ready():
    print(f"{client.user} is slaying 💋")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    random_chat.start()

@client.event
async def on_message(message):
    global last_mention_time
    if message.author.bot:
        return

    if client.user in message.mentions:
        now = datetime.datetime.now()
        if last_mention_time and (now - last_mention_time).total_seconds() < TRIGGER_TIMEOUT:
            return
        last_mention_time = now

        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        if not prompt:
            prompt = "say something random"

        reply = await message.channel.send("typing...")
        response = get_personality_response(prompt, message.author.display_name)
        await reply.edit(content=random.choice(emoji_pool) + " " + response)

    await client.process_commands(message)

@tasks.loop(minutes=random.randint(40, 90))
async def random_chat():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        lonely_lines = [
            "lowkey bored rn... talk to me?",
            "where tf is nick6383 at 😔",
            "the silence is loud today 💋",
            "feeling kinda ugly rn, someone hype me up",
            "need new pics of y’all asap 🖤",
            "missing drama tbh… someone start beef",
            "im lonely as hell rn 🫦"
        ]
        if random.random() < 0.4:
            await channel.send(random.choice(emoji_pool) + " " + random.choice(lonely_lines))