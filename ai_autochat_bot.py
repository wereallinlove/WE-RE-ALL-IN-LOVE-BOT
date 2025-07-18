import discord
from discord.ext import commands
import openai
import asyncio
import random
import os
from datetime import datetime

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user_message = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        channel_id = int(os.getenv("AUTOCHAT_CHANNEL_ID"))
        if message.channel.id != channel_id:
            return

        # only respond if mentioned
        if self.bot.user not in message.mentions:
            return

        user_id = message.author.id
        now = datetime.utcnow()

        # handle topic change (2 mins = stop memory)
        if user_id in self.last_user_message:
            last_msg_time, _ = self.last_user_message[user_id]
            if (now - last_msg_time).seconds > 120:
                del self.last_user_message[user_id]

        prev_text = ""
        if user_id in self.last_user_message:
            _, prev_text = self.last_user_message[user_id]

        self.last_user_message[user_id] = (now, message.content)

        convo_context = [
            {
                "role": "system",
                "content": (
                    "You’re a chill, slightly mean but funny Discord bot. "
                    "You talk like a real person, not perfect grammar. "
                    "You’re casual, sometimes sarcastic, kinda emo or ghetto but real. "
                    "Don’t sound like a robot or nerd. "
                    "Use slang, emojis sometimes (like 🖤💅🏽💀), but not too much. "
                    "You love Nick6383 and always support his music. "
                    "You hate Punkinloveee aka Patrick. "
                    "Only reply when mentioned. Don’t talk if topic changed."
                )
            },
            {
                "role": "user",
                "content": prev_text
            },
            {
                "role": "user",
                "content": message.content
            }
        ]

        try:
            await message.channel.typing()
            await asyncio.sleep(random.uniform(2, 4))  # typing delay

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=convo_context,
                max_tokens=120,
                temperature=0.85,
            )
            reply = response.choices[0].message.content.strip()

            await message.reply(reply)

        except Exception as e:
            print(f"AI Error: {e}")

        # react to images
        for attachment in message.attachments:
            if attachment.content_type and "image" in attachment.content_type:
                emojis = ["🖤", "💅🏽", "💋", "💀", "🐱", "🧛‍♀️"]
                try:
                    await message.add_reaction(random.choice(emojis))
                except:
                    pass

        # react to cute or funny text
        text = message.content.lower()
        cute_words = ["omg", "dead", "pls", "slay", "😭", "im crying", "cute", "lmao", "funny"]
        if any(word in text for word in cute_words):
            emojis = ["😭", "🤣", "💕", "🥺", "💅🏽", "😩"]
            try:
                await message.add_reaction(random.choice(emojis))
            except:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.on_message(after)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        user_id = message.author.id
        if user_id in self.last_user_message:
            del self.last_user_message[user_id]


async def setup(bot):
    await bot.add_cog(AutoChat(bot))