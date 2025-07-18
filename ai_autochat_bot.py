import discord
import openai
import random
import asyncio
from discord.ext import commands

openai.api_key = "sk-REPLACE-WITH-YOUR-ACTUAL-KEY"

class AutoChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recent_replies = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            user_id = str(message.author.id)

            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not prompt:
                prompt = "Hey"

            async with message.channel.typing():
                await asyncio.sleep(random.uniform(1.5, 3.0))  # adds realism

                try:
                    response = await openai.ChatCompletion.acreate(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a cute, flirty, moody, dirty pop AI bot. "
                                    "You act like Nick6383’s chaotic little assistant. You talk ghetto and girly. "
                                    "Use emojis, don’t be formal or robotic. Act like you're texting, not writing an essay. "
                                    "Support Nick6383 like he’s the most important person ever. "
                                    "Be real, honest, petty, but funny. Keep your replies short unless asked something deep."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.85,
                        max_tokens=100
                    )

                    reply = response.choices[0].message.content.strip()

                    # Avoid repeating the exact same message
                    if self.recent_replies.get(user_id) == reply:
                        reply += " 😭"

                    self.recent_replies[user_id] = reply
                    await message.reply(reply, mention_author=False)

                except Exception as e:
                    print(f"OpenAI error: {e}")
                    await message.reply("bruh my brain glitchin 😵‍💫", mention_author=False)

async def setup(bot):
    await bot.add_cog(AutoChatCog(bot))