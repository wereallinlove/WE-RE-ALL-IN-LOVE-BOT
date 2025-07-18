import discord
import openai
import random
import asyncio
from discord.ext import commands

openai.api_key = "sk-REPLACE-WITH-YOUR-KEY"

class AutoChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.bot.user not in message.mentions:
            return

        user_id = str(message.author.id)
        prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

        if not prompt:
            prompt = "Hey what's up?"

        history = self.chat_history.get(user_id, [])
        history.append({"role": "user", "content": prompt})
        history = history[-6:]

        system_prompt = {
            "role": "system",
            "content": (
                "You are a moody, bratty, dirty pop aesthetic AI with sass, slang, drama, and emotional humor. "
                "You're goth, hot, funny, and weird — like a Nick6383 stan who hates Punkinloveee. Use emojis like 🖤💅🏽💋💀🧛‍♀️🕷️📸 when it fits."
            )
        }

        try:
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(1.2, 2.2))

                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[system_prompt] + history,
                    temperature=0.9,
                    max_tokens=120
                )

                reply = response.choices[0].message.content.strip()
                history.append({"role": "assistant", "content": reply})
                self.chat_history[user_id] = history

                await message.reply(reply, mention_author=False)

        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            await message.reply("my wires got crossed rn 🧠💀", mention_author=False)

async def setup(bot):
    await bot.add_cog(AutoChatCog(bot))