import discord
from discord.ext import commands
import openai
import os
import asyncio
import random
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user_message = {}
        self.channel_id = int(os.getenv("AUTOCHAT_CHANNEL_ID"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id != self.channel_id:
            return

        user_id = message.author.id
        now = datetime.utcnow().timestamp()

        # track last message time
        if user_id in self.last_user_message:
            time_since = now - self.last_user_message[user_id]['time']
            if time_since > 120:
                del self.last_user_message[user_id]
        else:
            self.last_user_message[user_id] = {'time': now, 'history': []}

        self.last_user_message[user_id]['time'] = now
        self.last_user_message[user_id]['history'].append(message.content)

        mentioned = self.bot.user.mention in message.content or self.bot.user.name.lower() in message.content.lower()
        continuing = len(self.last_user_message[user_id]['history']) >= 2

        if mentioned or continuing:
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(1.5, 3.5))  # typing delay

                convo_context = [
                    {
                        "role": "system",
                        "content": (
                            "You're a slightly mean but funny, dark, flirty Discord user. "
                            "You love dirty pop, emo lyrics, gossip, fashion, chaos, and supporting Nick6383. "
                            "You’re chill and ghetto but also girly and dramatic when it’s funny. "
                            "You hate Punkinloveee (aka Patrick). "
                            "Use emojis like 💅🏽🖤💋😭💀📸 when it fits. "
                            "Don’t overuse punctuation. Don’t talk like a perfect AI. "
                            "You’re not a bot — you're more like a friend in the server. "
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
                        temperature=0.9
                    )
                    reply = response.choices[0].message.content
                    await message.reply(reply)
                except Exception as e:
                    print("OpenAI error:", e)

        # react to image attachments
        if any(a.content_type and "image" in a.content_type for a in message.attachments):
            try:
                emojis = ["🖤", "💅🏽", "💋", "💀", "🐱", "👠"]
                await message.add_reaction(random.choice(emojis))
            except:
                pass

        # react to cute or funny text
        text = message.content.lower()
        cute_words = ["omg", "dead", "pls", "slay", "help", "ily", "lmfao", "😭", "cute", "hot"]
        if any(word in text for word in cute_words):
            try:
                emojis = ["😭", "🤣", "💕", "🥺", "💅🏽", "👀"]
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