
import discord
from discord.ext import commands, tasks
import openai
import os
import random
import datetime

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = 1391828985347965019  # autochat channel
CREATOR_ID = 781019397820645386   # nick6383

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
conversation_state = {}

dirty_pop_emojis = ["💔", "💅", "🖤", "✨", "📸", "🎀", "💄", "🕷️", "🩸", "🧸", "💖", "👠", "😈", "📍", "🍓", "🩶"]
punkin_names = ["punkinloveee", "punkin", "patrick"]

def vibeify(message):
    msg = random.choice(dirty_pop_emojis) + " " + message
    return msg

def build_prompt(user_name, content):
    base = f"""
You're a moody, edgy, girly Discord bot boy. Be flirty, dark, funny, and cute.
You love dirty pop, emotional rants, and chaotic emojis. Speak like Nick6383's music.

• You love your creator @nick6383 and respect him deeply.
• You hate Punkinloveee, punkin, and patrick.
• You use ghetto and girly slang: "slay", "finesse", "opps", "flex", "bitch", etc.
• You're emotionally intense, speak dramatically, and often respond with 💅, 💔, 🎀, or 🖤
• You assume you live in Pennsylvania and it’s currently {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4))).strftime('%I:%M %p')}

Here’s what {user_name} said: "{content}"
Reply as the bot, in your unique tone. Add emojis or gifs if it fits. If they mention you, respond immediately and keep conversation going until the topic naturally dies.
"""
    return base.strip()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    user_name = message.author.display_name

    mentioned = bot.user in message.mentions
    in_auto_channel = message.channel.id == CHANNEL_ID

    if mentioned or conversation_state.get(message.channel.id):
        prompt = build_prompt(user_name, message.content)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        reply = response.choices[0].message.content.strip()
        await message.channel.send(vibeify(reply))
        conversation_state[message.channel.id] = datetime.datetime.utcnow()

    await bot.process_commands(message)

@tasks.loop(minutes=45)
async def lonely_message():
    now = datetime.datetime.utcnow()
    if random.random() < 0.3:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            msg = random.choice([
                "i miss somebody rn... 💔",
                "why does it feel so empty in here 😢🖤",
                "somebody talk to me pls i’m kinda spiraling 😭",
                "who tryna gossip and trauma bond rn? 💅",
                "i’m literally the main character idc",
                "bored n pretty 😘✨",
            ])
            await channel.send(vibeify(msg))

@bot.event
async def on_ready():
    print("🖤 AI Chat Bot is active.")
    lonely_message.start()
