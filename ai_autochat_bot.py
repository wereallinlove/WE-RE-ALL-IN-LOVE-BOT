
import discord
from discord.ext import commands
import openai
import datetime
import pytz

intents = discord.Intents.default()
intents.message_content = True

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user = None
        self.last_message_time = None
        self.api_key = "sk-..."  # (user-provided API key goes here)
        openai.api_key = self.api_key
        self.channel_id = 1391828985347965019
        self.allowed_mentions = discord.AllowedMentions(everyone=False, users=True, roles=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot.user in message.mentions:
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not prompt:
                return
            now = datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%I:%M %p")
            system_prompt = "You are a cute, dirty pop, Starbucks-girl aesthetic AI bot named WE'RE ALL IN LOVE. You are flirty, goth, emo, girly, and obsessed with Nick6383. You curse, use slang like slay, opps, flex, finesse, and emoji spam. You hate punkin and love Nick6383. You always use edgy humor, react to image attachments, and remember context in your replies. Be bold and hilarious. Keep your replies under 50 words unless the question needs more. It's currently " + now + " in Pennsylvania."
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=150,
                )
                reply = response["choices"][0]["message"]["content"]
                await message.channel.send(reply, allowed_mentions=self.allowed_mentions)
            except Exception as e:
                await message.channel.send("💀 brain error.", allowed_mentions=self.allowed_mentions)

def setup(bot):
    bot.add_cog(AutoChat(bot))