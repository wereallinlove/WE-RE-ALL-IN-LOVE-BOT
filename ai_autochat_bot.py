import discord
import openai
import random
import datetime
from discord.ext import commands

intents = discord.Intents.all()
class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = "sk-rz5KBFEXAMPLEKEYEXACTLYASHANDLED"
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user not in message.mentions:
            return

        now = datetime.datetime.now()
        user_id = message.author.id
        if user_id in self.cooldowns:
            if (now - self.cooldowns[user_id]).total_seconds() < 5:
                return

        self.cooldowns[user_id] = now

        prompt = f"This is a dirty pop, goth, emotional AI Discord bot that replies when mentioned. It uses Gen Z slang, is flirty, dramatic, and always supports the artist Nick6383. The user said: {message.content}. Respond in character."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a dirty pop, flirty, ghetto goth bot. Talk like that."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=1.0
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}")
            fallback_responses = [
                "uhh idk what to say rn 