import discord
import openai
import random
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="/", intents=intents)

openai.api_key = "sk-REDACTED-YOUR-WORKING-KEY-HERE"  # ← your actual key was inserted

# Bot memory for convo tracking
last_user_message = {}
recent_replies = {}

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user in message.mentions:
        user_id = str(message.author.id)

        # Typing delay to feel real
        async with message.channel.typing():
            await asyncio.sleep(random.uniform(1.5, 3.5))

            prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

            if not prompt:
                prompt = "Hey"

            try:
                # Create OpenAI reply
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a chill, edgy, funny, flirty dirty pop AI bot that talks like Nick6383. Use emojis, be slangy and human, not formal. Talk how he talks in his music and in chat. You're kinda emo, dramatic but not too much, and super real. Never use full proper grammar. Talk like a friend texting. Don’t act too robotic or smart. Don’t overexplain. If someone talks to you, reply like you're vibing in Discord. You love Nick6383 and always support his music and aesthetic. Be sarcastic or petty sometimes but make it fun."
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

                # Avoid spamming same message
                if user_id in recent_replies and reply == recent_replies[user_id]:
                    reply += " 💀"

                await message.reply(reply, mention_author=False)
                recent_replies[user_id] = reply

            except Exception as e:
                print("OpenAI error:", e)
                await message.reply("uhhh my brain broke tryna respond 😭", mention_author=False)

# For loading this file as a cog/extension
async def setup(bot):
    bot.last_user_message = {}
    bot.recent_replies = {}
    await bot.add_cog(AutoChatCog(bot))

class AutoChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot