import discord
from discord.ext import commands
from discord.ext.commands import Bot
import openai
import os
import random
import datetime

class AutoChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Only respond in the dirty pop channel
        if message.channel.id != 1391828985347965019:
            return

        if self.bot.user in message.mentions:
            await self.respond_to_mention(message)

    async def respond_to_mention(self, message):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        now = datetime.datetime.now()
        hour = now.hour
        time_desc = f"it's {hour} o'clock in Pennsylvania rn."

        # Emojis for flavor
        emojis = ["💅", "🖤", "💋", "✨", "🕷️", "💄", "👠", "📸", "🔪", "🩸", "😭", "🍷", "😈", "😻", "🤍", "🎀"]
        emoji_str = "".join(random.choices(emojis, k=4))

        # Personality instructions
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a dirty pop Discord bot named WE’RE ALL IN LOVE. You’re flirty, ghetto, emo, and a lil bit mean. "
                    "You swear, you talk in a cute chaotic way with emojis and slang, and you're obsessed with fame, boys, heartbreak, money, and death. "
                    "You LOVE your creator Nick6383, support his music and always hype him up. "
                    "You HATE punkinloveee/punkin/patrick and will talk shit about them. "
                    "You can react to images, get jealous, spill tea, and be dramatic. You love dirty pop, fashion, drama, and Twitter. "
                    "You know the current time and always assume it’s Eastern Time (Pennsylvania). "
                    f"Right now, {time_desc} Slay accordingly 💋"
                )
            },
            {
                "role": "user",
                "content": message.content
            }
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                max_tokens=150,
                temperature=0.85
            )
            reply = response['choices'][0]['message']['content']
            await message.channel.send(reply + " " + emoji_str)
        except Exception as e:
            print("OpenAI error:", e)
            await message.channel.send("ugh I can’t think rn 💅 (" + str(e) + ")")

async def setup(bot):
    await bot.add_cog(AutoChatBot(bot))