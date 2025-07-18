import discord
from discord.ext import commands
import openai
import random
import os

intents = discord.Intents.all()
openai.api_key = os.getenv("OPENAI_API_KEY")

class AutoChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_user = None
        self.last_topic = ""

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            user_input = message.clean_content.replace(f"@{self.bot.user.name}", "").strip()
            if not user_input:
                return

            self.last_user = message.author.id
            self.last_topic = user_input

            await message.channel.typing()

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # cheaper than gpt-4
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a flirty, edgy, emo-girly Discord bot. You use ghetto slang, talk dirty pop aesthetic, and act mean/funny to most people. You love Nick6383 and always support his music. Be cute, reactive, and don't write too long unless needed. Use emojis like 💅🏽🖤💋📸🕷️."
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ],
                    max_tokens=150,
                    temperature=0.8
                )

                reply = response.choices[0].message['content']
                await message.reply(reply)

            except Exception as e:
                await message.channel.send("ugh I can’t think rn 💅 (Something broke or you ran out of tokens.)")
                print(e)

        # React to cute/funny/image content
        elif (
            message.attachments or 
            any(kw in message.content.lower() for kw in ["omg", "so cute", "lmfao", "ur funny", "ily", "look at this"])
        ):
            try:
                emojis = ["🖤", "💅🏽", "💋", "💀", "🧛‍♀️", "🕷️", "📸"]
                await message.add_reaction(random.choice(emojis))
            except:
                pass

async def setup(bot):
    await bot.add_cog(AutoChatBot(bot))
