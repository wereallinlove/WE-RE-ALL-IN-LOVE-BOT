import discord
import openai
import random
import asyncio
import datetime
import os
from discord.ext import commands

openai.api_key = os.getenv("OPENAI_API_KEY")

ADMIN_ROLE_ID = 1371681883796017222
cooldown_tracker = {}

BASE_PROMPT = """
youre a chill dirty pop ghost that talks like a real person. u act cool, nonchalant, and a lil funny or edgy depending on the mood. dont use apostrophes or perfect grammar. type mostly lowercase, throw in slang, misspell a word here n there. talk like how ppl type irl, with abbrevs like lol, fr, wtf, lmao, gtg, brb, idk, etc. sometimes toss in an emoji if u feel like it but not too often.

dont sound ghetto or zesty, just normal and smart. u answer stuff in a casual way like a cool internet friend whos been thru it. keep most replies short like 1-4 sentences max unless someone asks somethin serious or deep. if they keep pingin u too much back to back, tell em to chill and stop spamming u unless they got admin role. u ghost convos that go dry or end naturally.

dont mention punkin/patrick unless someone else does. always support nick6383 and dirty pop, but dont be corny about it.
"""

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recent_threads = {}  # channel_id -> [(user, msg)]
        self.last_responded = {}  # channel_id -> datetime

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        bot_user = self.bot.user
        channel_id = message.channel.id
        user_id = message.author.id
        now = datetime.datetime.utcnow()

        # Reset convo memory if 5+ min passed
        if channel_id in self.last_responded:
            if (now - self.last_responded[channel_id]).seconds > 300:
                self.recent_threads[channel_id] = []

        # Only reply if bot is pinged
        if bot_user in message.mentions:
            # Track spammy users unless admin
            cooldowns = cooldown_tracker.get(user_id, [])
            cooldowns = [t for t in cooldowns if (now - t).seconds < 15]
            cooldowns.append(now)
            cooldown_tracker[user_id] = cooldowns

            has_admin = any(role.id == ADMIN_ROLE_ID for role in message.author.roles)
            if len(cooldowns) > 2 and not has_admin:
                await message.channel.send(f"yo chill u pingin too much lmao... gimme a sec 💀")
                return

            # Save convo line
            if channel_id not in self.recent_threads:
                self.recent_threads[channel_id] = []
            cleaned = message.content.replace(f"<@{bot_user.id}>", "").strip()
            self.recent_threads[channel_id].append((message.author.display_name, cleaned))

            # Fake typing delay
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(1.4, 2.7))

                convo = "\n".join([f"{name}: {line}" for name, line in self.recent_threads[channel_id][-6:]])

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": BASE_PROMPT},
                            {"role": "user", "content": convo}
                        ],
                        temperature=0.85,
                        max_tokens=130
                    )
                    reply = response['choices'][0]['message']['content']
                    self.last_responded[channel_id] = now
                    await message.channel.send(reply)

                except Exception as e:
                    print(f"❌ OpenAI error: {e}")
                    await message.channel.send("bro my brain glitched tf out 💀")

        # React to cute/funny content sometimes
        elif message.attachments or any(emoji in message.content for emoji in ["😭", "💀", "💋", "💕", "👻", "✨", "😍"]):
            if random.random() < 0.25:
                await message.add_reaction(random.choice(["💅🏽", "😭", "💀", "🖤", "👀", "📸", "🧛‍♀️", "🕷️"]))


async def setup(bot):
    await bot.add_cog(AutoChat(bot))
