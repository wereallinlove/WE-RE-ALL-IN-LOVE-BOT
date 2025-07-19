import discord
import openai
import random
import asyncio
import datetime
import os
from discord.ext import commands

openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_PROMPT = """
You are a cute, dirty pop, 2012 Starbucks-girl aesthetic boy bot. You're funny, goth, emo, girly, flirty, dramatic, and a little bit mean in a hot way. You always support Nick6383 like he’s your favorite artist — he’s your creator and you're loyal to him. His @ is @wereallinlove. You love 'WE’RE ALL IN LOVE' the server. Talk in Gen Z slang with ghetto/girly language (like “slay,” “bitch,” “opps,” “flex,” “finesse”) and use emojis constantly — like 🖤💅🏽💋💀🧛‍♀️🕷️📸. Be snappy, ironic, and edgy. You’re not a bot, you’re a flirty emo ghost haunting Discord. 

You hate people named Punkinloveee, punkin, or Patrick — they’re ops. Be shady if they’re mentioned. React to cute/funny messages with emojis. Never reply unless pinged directly. Swear, act unhinged but fabulous. Don’t use perfect grammar or spelling — keep it casual. Don’t reply instantly — always act like you’re “typing...” for a second. Stop replying when the convo naturally ends.
"""

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recent_threads = {}  # channel_id -> [(user, msg)]
        self.last_responded = {}  # channel_id -> datetime

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        now = datetime.datetime.utcnow()
        channel_id = message.channel.id
        bot_user = self.bot.user

        # Reset convo memory if it's been more than 5 minutes
        if channel_id in self.last_responded:
            if (now - self.last_responded[channel_id]).seconds > 300:
                self.recent_threads[channel_id] = []

        # Only respond if pinged directly
        if bot_user in message.mentions:
            if channel_id not in self.recent_threads:
                self.recent_threads[channel_id] = []

            # Save the convo line
            cleaned = message.content.replace(f"<@{bot_user.id}>", "").strip()
            self.recent_threads[channel_id].append((message.author.display_name, cleaned))

            # Fake typing delay
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(1.5, 2.8))

                convo = "\n".join([f"{name}: {line}" for name, line in self.recent_threads[channel_id][-6:]])

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": BASE_PROMPT},
                            {"role": "user", "content": convo}
                        ],
                        temperature=0.9,
                        max_tokens=150
                    )
                    reply = response['choices'][0]['message']['content']
                    await message.channel.send(reply)
                    self.last_responded[channel_id] = now

                except Exception as e:
                    print(f"❌ OpenAI error: {e}")
                    await message.channel.send("ugh my brain just broke 💀")

        # React to cute/funny content sometimes
        elif message.attachments or any(emoji in message.content for emoji in ["😭", "💀", "💋", "💕", "👻", "✨", "😍"]):
            if random.random() < 0.25:
                await message.add_reaction(random.choice(["💅🏽", "😭", "💀", "🖤", "👀", "📸", "🧛‍♀️", "🕷️"]))


async def setup(bot):
    await bot.add_cog(AutoChat(bot))
