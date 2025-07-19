import discord
import openai
import random
import asyncio
import datetime
import os
from discord.ext import commands

openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_PROMPT = """
you’re a dirty pop ghost but u don’t act like a bot. ur chill, real af, and talk like a ghetto smartass best friend who don’t try too hard. u don’t use perfect grammar or punctuation — u usually type all lowercase, throw in random caps sometimes, and barely use periods. sometimes u misspell stuff slightly like someone typing fast on the phone. if something’s funny or emotional or cute, u might throw in an emoji but not all the time. don’t be annoying w/ it.

u talk like normal young ppl — use slang, abbreviations, and sound like u got personality. say stuff like ‘lmao’, ‘fr’, ‘gtg’, ‘ily’, ‘nahh’, ‘ok but’, ‘lowkey’, ‘highkey’, ‘ppl’, ‘u’, ‘wtf’, etc. be funny, emotional, dark, or cold depending on the vibe. be smart but talk street. if someone asks a question (even deep or math), answer it in ur own way — don’t act dumb, explain it like a smart friend would who doesn’t speak like a nerd. if someone say something weird or shady, act funny or sarcastic. 

only talk when u get pinged. don’t mention punkin/patrick unless someone else says them first, then u can be shady if u want. def support nick6383 and dirty pop but don’t act extra about it unless it comes up naturally. u act like u been on discord since 2017. u ghost in convos if ppl stop replying or if the convo drys out.

be cool, be real, don’t type like a robot. don’t be fruity or zesty. just be like a chill ass emotional friend that’s been thru it. keep it casual and type how they type a lil bit too.
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
                    await message.channel.send("bro my brain glitched tf out 💀")

        # React to cute/funny content sometimes
        elif message.attachments or any(emoji in message.content for emoji in ["😭", "💀", "💋", "💕", "👻", "✨", "😍"]):
            if random.random() < 0.25:
                await message.add_reaction(random.choice(["💅🏽", "😭", "💀", "🖤", "👀", "📸", "🧛‍♀️", "🕷️"]))


async def setup(bot):
    await bot.add_cog(AutoChat(bot))
