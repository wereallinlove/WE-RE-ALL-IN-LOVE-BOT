import discord
import openai
import random
import asyncio
from discord.ext import commands

openai.api_key = "sk-REPLACE-WITH-YOUR-ACTUAL-KEY"

class AutoChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = {}  # stores short memory per user

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            user_id = str(message.author.id)
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not prompt:
                prompt = "Hey"

            # Keep last 5 exchanges per user
            history = self.chat_history.get(user_id, [])
            history.append({"role": "user", "content": prompt})
            history = history[-5:]  # last 5 only

            system_prompt = {
                "role": "system",
                "content": (
                    "You are a flirty, ghetto, bratty, dirty pop-style AI bot. You talk like Nick6383’s chaotic little bestie. "
                    "You respond emotionally, dramatically, and slangy like texting. Don't be robotic. Use emojis. Stay short unless they ask deep stuff. "
                    "You support Nick6383 no matter what. Be mean to haters. Sound real, petty, funny, chaotic, and cute. Talk like the user, not perfect grammar."
                )
            }

            try:
                async with message.channel.typing():
                    await asyncio.sleep(random.uniform(1.5, 2.5))

                    response = await openai.ChatCompletion.acreate(
                        model="gpt-3.5-turbo",
                        messages=[system_prompt] + history,
                        temperature=0.85,
                        max_tokens=120
                    )

                    reply = response.choices[0].message.content.strip()
                    history.append({"role": "assistant", "content": reply})
                    self.chat_history[user_id] = history  # update history

                    await message.reply(reply, mention_author=False)

            except Exception as e:
                print(f"OpenAI error: {e}")
                await message.reply("uhh idk what to say rn 💀", mention_author=False)

async def setup(bot):
    await bot.add_cog(AutoChatCog(bot))