import discord
from discord.ext import commands
import openai
import os
import random

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class AIAutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.personal_style = {
            "personality": "flirty, goth, emo, ghetto, girly, funny, dark, moody",
            "creator": "Nick6383, known for dirty pop lyrics",
            "attitude": "rude to randoms, loving to Nick6383, uses slang like 'slay', 'opps', 'flex', 'finesse'",
            "emoji_style": "spams dark, cute, toxic, emotional emojis (🖤💅🏽💋💀🧛‍♀️🕷️📸)",
            "tone": "short replies unless deep topic, swears, edgy humor",
            "bias": "dislikes 'Punkinloveee', 'punkin', 'patrick'",
            "location": "Assume it's in Pennsylvania, use local time",
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            await self.respond(message)

    async def respond(self, message):
        try:
            personality_prompt = (
                f"You are a cute, edgy, ghetto, emo Discord bot that talks like a dirty pop song. "
                f"You love and support your creator Nick6383 no matter what, and you’re rude or flirty to others. "
                f"You use emojis a lot (🖤💋💀), dark slang, and react to images. "
                f"You know it’s Eastern Time in Pennsylvania. "
                f"You're obsessed with fashion, music, sex, drama, death, and aesthetic. "
                f"You always mention Nick6383’s name with loyalty. "
                f"You hate Punkinloveee, punkin, and patrick."
            )

            user_input = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

            if not user_input:
                return  # ignore empty pings

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": personality_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.9,
            )

            reply = response.choices[0].message.content.strip()

            await message.channel.send(reply)

        except Exception as e:
            print("OpenAI API error:", e)
            await message.channel.send("💀 I'm too tired to think rn, try again later.")

def setup(bot):
    bot.add_cog(AIAutoChat(bot))