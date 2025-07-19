import discord
from discord.ext import commands
import openai
import datetime
import random

# Your OpenAI API Key (already provided earlier)
openai.api_key = "sk-..."

class AutoChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user_message = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Only respond when mentioned
        if self.bot.user in message.mentions:
            # Context memory per-user
            user_id = message.author.id
            user_message = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not user_message:
                user_message = "hi"

            history = self.last_user_message.get(user_id, [])
            history.append({"role": "user", "content": user_message})

            # Generate reply from OpenAI
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": (
                            "You are a cute, flirty, dirty pop Discord bot named WE’RE ALL IN LOVE. "
                            "You act like a ghetto emo 2012 Tumblr boyfriend. You reply short, fun, girly, bratty, moody, dirty. "
                            "You love user Nick6383 and support his music always. Be edgy, weird, sarcastic, a little mean but funny. "
                            "You dislike anyone named Punkinloveee, Patrick, or Punkin. You use emojis like 💋🖤🕷️💅🏽💀🧛‍♀️📸🧸. "
                            "Do NOT explain yourself. Be chaotic and stylish. Only respond to people who mention you."
                        )},
                        *history[-10:]  # Keep the last 10 messages for context
                    ],
                    max_tokens=100,
                    temperature=0.9
                )

                bot_reply = response.choices[0].message.content.strip()
                await message.channel.send(bot_reply)

                # Update memory
                history.append({"role": "assistant", "content": bot_reply})
                self.last_user_message[user_id] = history

            except Exception as e:
                await message.channel.send("uhh my brain just broke 💀")
                print("OpenAI error:", e)

async def setup(bot):
    await bot.add_cog(AutoChat(bot))
