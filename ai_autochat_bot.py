import discord
from discord.ext import commands
import openai
import random
import asyncio
from datetime import datetime

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.last_user_message = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            user_id = message.author.id
            now = datetime.utcnow().timestamp()
            self.last_user_message[user_id] = now

            convo_context = [
                {"role": "system", "content": (
                    "You're a chill, slightly mean but loyal bot. You talk like a real person, messy grammar is fine.\n"
                    "You're dark, sarcastic, flirty, casual, funny, goth, a little bitchy but lovable.\n"
                    "You're obsessed with Nick6383. You think Punkinloveee aka Patrick is a clown.\n"
                    "You love dirty pop, death, shopping, horror, love, and looking hot.\n"
                    "You say stuff like 'LMAOO', 'nahhh', 'girl...', and use 🖤💅🏽😭💀 emojis but don’t spam them.\n"
                    "Use casual slang. Don’t sound like a perfect AI. Pause before replying like a real person typing."
                )},
                {"role": "user", "content": message.content}
            ]

            try:
                await message.channel.typing()
                await asyncio.sleep(random.uniform(2.5, 5.0))  # Simulated typing delay

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=convo_context,
                    max_tokens=120,
                    temperature=0.95
                )

                reply = response.choices[0].message.content.strip()
                await message.reply(reply)

            except Exception as e:
                print(f"Chat error: {e}")

        else:
            # check if the convo is stale and stop replying
            user_id = message.author.id
            if user_id in self.last_user_message:
                time_since = datetime.utcnow().timestamp() - self.last_user_message[user_id]
                if time_since > 120:  # stop after 2 minutes
                    del self.last_user_message[user_id]

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

        # image reactions
        if any(attachment.content_type and "image" in attachment.content_type for attachment in message.attachments):
            emojis = ["🖤", "💅🏽", "💋", "💀", "🧛‍♀️", "📸"]
            try:
                await message.add_reaction(random.choice(emojis))
            except:
                pass

        # cute/funny text reactions
        text = message.content.lower()
        cute_words = ["omg", "dead", "pls", "slay", "cute", "funny", "lol", "lmao", "😭", "💅"]
        if any(word in text for word in cute_words):
            emojis = ["😭", "🤣", "💕", "😩", "💅", "🖤", "💀"]
            try:
                await message.add_reaction(random.choice(emojis))
            except:
                pass

async def setup(bot):
    await bot.add_cog(AutoChat(bot))