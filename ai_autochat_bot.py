import discord
from discord.ext import commands
import openai
import datetime
import random
import pytz

intents = discord.Intents.all()
openai.api_key = "sk-..."  # Already stored from your key earlier

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memory = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            user_id = str(message.author.id)
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

            if not prompt:
                prompt = "say something random and weird"

            if user_id not in self.memory:
                self.memory[user_id] = []

            self.memory[user_id].append({"role": "user", "content": prompt})

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute, flirty, edgy, emo, dirty-pop Discord bot. Respond in Gen Z slang with emojis. Support Nick6383. Be dramatic, moody, and funny."},
                        *self.memory[user_id][-6:],  # last few messages per user
                    ],
                    max_tokens=100,
                    temperature=1.0,
                )

                reply = response.choices[0].message.content
                self.memory[user_id].append({"role": "assistant", "content": reply})

                await message.channel.send(reply)

            except Exception as e:
                await message.channel.send("🧠 something snapped in my wires... try again")
                print(f"OpenAI error: {e}")

async def setup(bot):
    await bot.add_cog(AutoChat(bot))
