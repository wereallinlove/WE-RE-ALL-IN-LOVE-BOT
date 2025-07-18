
import discord
from discord.ext import commands
import openai
import random
import asyncio
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")
channel_id = 1391828985347965019  # Hardcoded channel ID

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user_message = {}
        self.last_topic = {}
        self.recent_responses = {}

    def same_topic(self, user_id, new_msg):
        old_msg = self.last_user_message.get(user_id)
        if not old_msg:
            return False
        return old_msg.split()[0:2] == new_msg.split()[0:2]

    async def generate_reply(self, user_id, message):
        convo_context = [
            {
                "role": "system",
                "content": (
                    "You're a chill, ghetto, slightly flirty, emo Discord bot. You talk like Nick6383. "
                    "You love Nick6383 and hate Punkinloveee (aka Patrick). Use emojis (💋💀🖤🧛‍♀️📸) but not too much. "
                    "Be a little edgy, don't use perfect grammar, and sound like a human. "
                    "You respond with short or medium replies unless the topic needs more. "
                    "Don't talk randomly — only reply to mentions or recent conversations. "
                    "Stop replying if the topic changes or user goes quiet. React to cute or funny stuff too."
                ),
            },
            {"role": "user", "content": message}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=convo_context,
            max_tokens=100,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id
        content = message.content.lower()

        # React to cute or funny messages
        cute_words = ["omg", "dead", "pls", "slay", "ily", "cutie", "nooo", "stfu"]
        if any(word in content for word in cute_words):
            try:
                await message.add_reaction(random.choice(["😭", "🤣", "💕", "😩", "💅🏽"]))
            except:
                pass

        # React to image attachments
        for attachment in message.attachments:
            if attachment.content_type and "image" in attachment.content_type:
                try:
                    await message.add_reaction(random.choice(["🖤", "💅🏽", "💋", "💀", "🧛‍♀️", "📸"]))
                except:
                    pass

        # Mentioned or continuing convo in same topic
        if self.bot.user in message.mentions or self.same_topic(user_id, content):
            self.last_user_message[user_id] = content
            await message.channel.typing()
            await asyncio.sleep(random.uniform(1.5, 3.5))  # Typing delay
            try:
                reply = await self.generate_reply(user_id, content)
                await message.reply(reply)
            except Exception as e:
                print(f"Error generating reply: {e}")
        else:
            self.last_user_message.pop(user_id, None)  # Topic changed or user went quiet

async def setup(bot):
    await bot.add_cog(AutoChat(bot))
