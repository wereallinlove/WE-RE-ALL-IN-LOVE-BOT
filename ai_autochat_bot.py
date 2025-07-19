import discord
from discord.ext import commands
import openai
import datetime
import random

intents = discord.Intents.all()

# Replace this with your real key if needed
openai.api_key = "your-real-api-key-here"

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_responses = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            now = datetime.datetime.now()
            user_id = message.author.id

            if user_id in self.last_responses:
                last_time, _ = self.last_responses[user_id]
                if (now - last_time).seconds < 5:
                    return  # prevent spam

            prompt = f"""You're a Discord bot named WE'RE ALL IN LOVE. You're flirty, dirty pop, ghetto, emo, stylish, and funny. You always support Nick6383 like a loyal fan. You're a little mean to others in a playful way. Respond in short, casual sentences. You say things like slay, flex, opps, bitch, lmfao, 🖤, 💅🏽, 💋, 💀, etc.

Here’s what {message.author.display_name} said: “{message.content}”

Now reply in your dirty pop style:"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a sassy and stylish Discord bot with a dark, girly, and flirty tone. Support Nick6383."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=80,
                    temperature=0.9
                )

                reply = response.choices[0].message.content.strip()
                self.last_responses[user_id] = (now, reply)

                await message.channel.send(reply)
            except Exception as e:
                await message.channel.send("uhh my brain just broke 💀")
                print("OpenAI error:", e)

async def setup(bot):
    await bot.add_cog(AutoChat(bot))
