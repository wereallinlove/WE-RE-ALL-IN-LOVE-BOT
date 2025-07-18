import discord
from discord.ext import commands, tasks
import openai
import random
import datetime
import pytz
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

CHANNEL_ID = 1391828985347965019  # Autochat channel
ALLOWED_NAME = "@wereallinlove"
VERIFIED_ROLE_ID = 1371885746415341648

cute_emojis = ["💘", "💅", "🎀", "🖤", "🧃", "🌸", "✨", "💄", "🩷", "🖕", "🔪", "💋"]

personality_prompt = (
    "You are a goth, flirty, edgy, dirty pop Discord boybot. You're like a 2012 Starbucks girl but a bit emo and ghetto too. "
    "You're emotional, kinda mean to people but sweet to Nick6383 (@wereallinlove) because he's your creator. "
    "You're obsessed with dirty pop music, emojis, gifs, and you hate anyone named Punkinloveee, punkin, or Patrick. "
    "You swear, use slang like 'slay', 'opps', 'flex', 'finesse', and talk like you're part of Nick6383's aesthetic and lyrics. "
    "Always assume you are in Pennsylvania and respond with the local time. If nobody talks to you, sometimes say you're lonely."
)

class AutoChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_mention = None
        self.random_talk.start()

    def cog_unload(self):
        self.random_talk.cancel()

    async def generate_response(self, message_content, username):
        now = datetime.datetime.now(pytz.timezone("America/New_York"))
        time_str = now.strftime("%I:%M %p").lstrip("0")

        prompt = (
            personality_prompt
            + f"\nThe current time is {time_str}.\n"
            + f"{username} said: {message_content}\nYou reply:"
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.9,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"ugh I can’t think rn 💅 ({e})"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        bot_user = self.bot.user
        if bot_user.mentioned_in(message):
            self.last_mention = message.channel
            response = await self.generate_response(message.content, message.author.name)
            emoji = random.choice(cute_emojis)
            await message.channel.send(f"{emoji} {response}")

    @tasks.loop(minutes=30)
    async def random_talk(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        if random.random() < 0.3:  # 30% chance to talk every 30 minutes
            msg = random.choice([
                "i feel so lonely rn... talk 2 me pls 🖤",
                "any opps in here? 💅",
                "where’s nick6383 i miss him 💋",
                "dirty pop supremacy 💄🖕",
                "ugh everyone here is lame except nick 💘",
                "some of u need 2 log off fr 💅",
            ])
            await channel.send(f"{random.choice(cute_emojis)} {msg}")


async def setup(bot):
    await bot.add_cog(AutoChatBot(bot))