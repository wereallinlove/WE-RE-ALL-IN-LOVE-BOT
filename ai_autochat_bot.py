import discord
import openai
import random
import asyncio
from discord.ext import commands

openai.api_key = "sk-REPLACE-WITH-YOUR-KEY"

class AutoChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = {}  # store user convo memory

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.bot.user not in message.mentions:
            return

        user_id = str(message.author.id)
        prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

        # Default message if they just say the name
        if not prompt:
            prompt = "Hey what's up?"

        # Keep short memory (up to 6 exchanges)
        history = self.chat_history.get(user_id, [])
        history.append({"role": "user", "content": prompt})
        history = history[-6:]

        system_prompt = {
            "role": "system",
            "content": (
                "You are a chaotic, flirty, bratty, dirty pop-style AI bot who talks like Nick6383’s spooky little bestie. "
                "You type with emotion, slang, Gen Z texting, emojis, and attitude. Be real, funny, ghetto, emotional, dramatic. "
                "Support Nick6383 no matter what. Hate Punkinloveee. Don’t speak formally. Talk like an edgy, flirty, funny teen. "
                "Use 🖤💅🏽💋💀🧛‍♀️🕷️📸 when it fits. Stay short unless they get deep. Remember recent convo."
            )
        }

        try:
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(1.5, 2.5))

                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[system_prompt] + history,
                    temperature=0.85,
                    max_tokens=150
                )

                reply = response.choices[0].message.content.strip()
                history.append({"role": "assistant", "content": reply})
                self.chat_history[user_id] = history

                await message.reply(reply, mention_author=False)

        except Exception as e:
            print(f"OpenAI error: {e}")
            await message.reply("uhhh my brain just broke 💀", mention_author=False)

async def setup(bot):
    await bot.add_cog(AutoChatCog(bot))