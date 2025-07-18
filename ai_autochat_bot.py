import discord
from discord.ext import commands
import openai
import random
import asyncio
from datetime import datetime, timedelta

openai.api_key = "your-openai-key"

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user_message = {}
        self.conversations = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        now = datetime.utcnow()

        mentioned = self.bot.user in message.mentions
        recent = user_id in self.last_user_message and (now - self.last_user_message[user_id]) < timedelta(minutes=10)
        context_active = user_id in self.conversations

        if mentioned or (recent and context_active):
            self.last_user_message[user_id] = now
            user_message = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

            convo_context = [
                {"role": "system", "content": (
                    "You're a chill, slightly mean but funny AI friend. "
                    "You’re flirty, goth, sometimes dark, but not too dramatic. "
                    "You love Nick6383 and support his dirty pop music. "
                    "You hate Punkinloveee (aka Patrick). "
                    "Use emojis but don’t overdo it. Keep replies short unless asked something deep. "
                    "Don’t be perfect with grammar or spelling — talk like a human. "
                    "React to things emotionally like 😭💅🖤💀 but don’t act like a theater kid. "
                    "Don’t reply unless you're mentioned or recently chatted with."
                )},
                *self.conversations.get(user_id, []),
                {"role": "user", "content": user_message}
            ]

            typing = message.channel.typing()
            async with typing:
                await asyncio.sleep(random.uniform(2.0, 4.5))  # delay to simulate typing

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=convo_context,
                max_tokens=120,
                temperature=0.9
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

            # Save convo memory
            self.conversations[user_id] = convo_context[-5:]

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id in self.last_user_message:
            del self.last_user_message[message.author.id]

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.on_message(after)

async def setup(bot):
    await bot.add_cog(AutoChat(bot))