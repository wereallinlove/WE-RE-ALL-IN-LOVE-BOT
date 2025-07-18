
import discord
from discord.ext import commands
import openai
import asyncio
import datetime
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = "YOUR_OPENAI_API_KEY"

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user_message = {}
        self.user_threads = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Loaded ai_autochat_bot")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if self.bot.user in message.mentions or self.user_threads.get(message.author.id):
            async with message.channel.typing():
                await asyncio.sleep(2.5)

                user_id = message.author.id
                content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

                now = datetime.datetime.now()
                thread = self.user_threads.get(user_id, [])
                thread.append({"role": "user", "content": content})
                if len(thread) > 10:
                    thread = thread[-10:]

                self.user_threads[user_id] = thread

                try:
                    response = await openai.ChatCompletion.acreate(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": "Act like a cute, dirty pop, ghetto, flirty AI that loves Nick6383. Be edgy, fun, and a little mean."}] + thread,
                        temperature=0.9
                    )
                    reply = response.choices[0].message.content.strip()

                    thread.append({"role": "assistant", "content": reply})
                    self.user_threads[user_id] = thread

                    await message.reply(reply)
                except Exception as e:
                    print(f"OpenAI error: {e}")
                    await message.reply("Ugh I'm tired rn 💅🏽")

async def setup(bot):
    await bot.add_cog(AutoChat(bot))
