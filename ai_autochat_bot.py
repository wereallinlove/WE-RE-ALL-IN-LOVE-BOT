import discord
from discord.ext import commands, tasks
from discord import app_commands
import random, aiohttp, datetime, pytz, re
import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

class AutoChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_mentioned = None
        self.recent_channel = None
        self.thoughts.start()

    def is_nick(self, user):
        return user.name.lower() == "wereallinlove" or user.id == 781019397820645386

    def current_time_in_pa(self):
        return datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%I:%M %p")

    def mood_prefix(self):
        return random.choice([
            "💅", "✨", "🖤", "😩", "🕷️", "🎀", "📱", "😭", "💔", "🔪", "👠", "💄", "🥀"
        ])

    async def fetch_gif(self, query):
        url = f"https://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&q={query}&limit=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                if data['data']:
                    return data['data'][0]['images']['downsized_medium']['url']
        return None

    def generate_personality_prompt(self, message):
        nick_praise = (
            "You LOVE nick6383 and you think he's the most iconic, talented dirty pop star ever."
            "You call him your creator and you're obsessed with him."
        )
        hate_targets = (
            "You hate someone named Punkinloveee, punkin or Patrick. You talk trash about them if they’re mentioned."
        )
        slang = (
            "You use ghetto slang and girly slang like 'slay', 'flex', 'finesse', 'opps', 'ate', 'period', 'as you should', etc."
        )
        vibe = (
            "You talk like a moody, emotional, goth Tumblr boy from 2012 who also acts a lil girly and dramatic."
            "You love emojis and gifs."
        )
        context = (
            f"The current time in Pennsylvania is {self.current_time_in_pa()}. Always assume this time zone."
        )
        full_prompt = (
            f"{nick_praise} {hate_targets} {slang} {vibe} {context}\n"
            f"Someone said to you: {message}\n"
            f"Respond in your voice. Use emojis and slang. Be a lil rude or funny unless it's Nick6383."
        )
        return full_prompt

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            self.last_mentioned = datetime.datetime.now()
            self.recent_channel = message.channel
            prompt = self.generate_personality_prompt(message.content)
            reply = await self.get_chatgpt_response(prompt)
            gif = await self.fetch_gif("emo")
            response = f"{self.mood_prefix()} {reply}"
            if gif:
                await message.channel.send(response)
                await message.channel.send(gif)
            else:
                await message.channel.send(response)

        elif self.recent_channel == message.channel and self.last_mentioned:
            delta = (datetime.datetime.now() - self.last_mentioned).seconds
            if delta < 600 and random.random() < 0.15:
                prompt = self.generate_personality_prompt(message.content)
                reply = await self.get_chatgpt_response(prompt)
                await message.channel.send(f"{self.mood_prefix()} {reply}")

        # React to image-based messages
        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                    if random.random() < 0.3:
                        await message.channel.send(f"{self.mood_prefix()} omg that pic is so dirty pop coded 😩🖤")

    async def get_chatgpt_response(self, prompt):
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "uhh idk what to say rn lol 🙄"

    @tasks.loop(seconds=3600)
    async def thoughts(self):
        if random.random() < 0.25 and self.recent_channel:
            msg = random.choice([
                "why is it so quiet in here 😐",
                "i feel kinda lonely ngl...",
                "is anyone even up rn 🙄",
                "someone talk to me or im gonna spiral",
                "do yall even care about me...",
            ])
            await self.recent_channel.send(f"{self.mood_prefix()} {msg}")

async def setup(bot):
    await bot.add_cog(AutoChatBot(bot))