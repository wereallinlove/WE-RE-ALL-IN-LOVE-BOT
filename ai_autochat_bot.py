import discord
from discord.ext import commands
import openai
import asyncio
import random
from datetime import datetime

openai.api_key = "YOUR_OPENAI_API_KEY"

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user_message = {}
        self.channel_id = 1391828985347965019  # Hardcoded channel ID

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.on_message(after)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        user_id = message.author.id
        if user_id in self.last_user_message:
            del self.last_user_message[user_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id != self.channel_id:
            return

        text = message.content.lower()

        # React to cute/funny text
        cute_words = ["omg", "dead", "pls", "slay", "help", "lmao", "bye", "crying"]
        if any(word in text for word in cute_words):
            emojis = ["😭", "🤣", "💕", "🥺", "💅🏽", "😩", "✨"]
            try:
                await message.add_reaction(random.choice(emojis))
            except:
                pass

        # React to images
        for attachment in message.attachments:
            if attachment.content_type and "image" in attachment.content_type:
                emojis = ["🖤", "💅🏽", "💋", "💀", "🧛‍♀️", "🕷️", "📸"]
                try:
                    await message.add_reaction(random.choice(emojis))
                except:
                    pass

        # Only respond if mentioned
        if self.bot.user in message.mentions:
            now = datetime.utcnow().timestamp()
            user_id = message.author.id
            last_msg = self.last_user_message.get(user_id, {"time": 0})
            time_since = now - last_msg["time"]

            # Reset context if more than 2 minutes passed
            if time_since > 120:
                del self.last_user_message[user_id]

            self.last_user_message[user_id] = {
                "text": message.content,
                "time": now
            }

            async with message.channel.typing():
                await asyncio.sleep(random.uniform(2.5, 4.5))  # More natural typing delay
                convo_context = [
                    {
                        "role": "system",
                        "content": (
                            "You're a chill, slightly mean but loyal AI Discord bot. "
                            "You're flirty, emo, ghetto, funny, dark sometimes. "
                            "You always support Nick6383, he's your creator. "
                            "You hate Punkinloveee (aka Patrick). "
                            "Don't sound perfect, talk messy & casual like a real person. "
                            "No proper grammar, no try-hard sentences. "
                            "Use emojis but don’t go crazy with them. "
                            "Stop replying when topic shifts. Be unpredictable sometimes."
                        )
                    },
                    {
                        "role": "user",
                        "content": message.content
                    }
                ]

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=convo_context,
                        max_tokens=100,
                        temperature=0.9,
                    )
                    reply = response.choices[0].message.content
                    await message.reply(reply)
                except Exception as e:
                    print("OpenAI error:", e)

async def setup(bot):
    await bot.add_cog(AutoChat(bot))
