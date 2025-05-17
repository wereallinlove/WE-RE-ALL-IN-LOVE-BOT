
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
import random
import asyncio
import datetime

TRIVIA_CHANNEL_ID = 1373112868249145485
VERIFIED_ROLE_ID = 1371885746415341648
TRIVIA_COOLDOWN = 10
TRIVIA_TIMEOUT = 900  # 15 minutes

SONG_DATA = {
    # Replace this comment with your full original SONG_DATA block
}

used_recently = set()
active_trivia = {}

class TriviaView(View):
    def __init__(self, correct_title, user_id):
        super().__init__(timeout=TRIVIA_TIMEOUT)
        self.correct = correct_title
        self.user_id = user_id
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your trivia!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.reply(f"<@{self.user_id}> your trivia request expired.")
            except:
                pass
        active_trivia.pop(self.user_id, None)

    async def check_answer(self, interaction, choice):
        if self.user_id in active_trivia:
            active_trivia.pop(self.user_id, None)
        used_recently.add(self.user_id)
        await interaction.response.defer()
        await asyncio.sleep(TRIVIA_COOLDOWN)
        used_recently.discard(self.user_id)

        if choice == self.correct:
            embed = discord.Embed(title="✅ Correct!", description=f"You chose **{choice}**.

You got it right!", color=0x2ecc71)
        else:
            embed = discord.Embed(title="❌ Incorrect.", description=f"You chose **{choice}**.

The correct answer was **{self.correct}**.", color=0xe74c3c)
        await interaction.followup.send(embed=embed)
        self.stop()

    @discord.ui.button(label="Option A", style=discord.ButtonStyle.secondary)
    async def a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_answer(interaction, button.label)

    @discord.ui.button(label="Option B", style=discord.ButtonStyle.secondary)
    async def b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_answer(interaction, button.label)

    @discord.ui.button(label="Option C", style=discord.ButtonStyle.secondary)
    async def c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_answer(interaction, button.label)

    @discord.ui.button(label="Option D", style=discord.ButtonStyle.secondary)
    async def d(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_answer(interaction, button.label)

class Nick6383Trivia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="nick6383trivia", description="Start a Nick6383 lyric trivia question.")
    async def nick6383trivia(self, interaction: discord.Interaction):
        if interaction.channel.id != TRIVIA_CHANNEL_ID:
            return await interaction.response.send_message("This command only works in the trivia channel.", ephemeral=True)
        if VERIFIED_ROLE_ID not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("You need the Verified role to play.", ephemeral=True)
        if interaction.user.id in used_recently:
            return await interaction.response.send_message("Please wait before using this command again.", ephemeral=True)
        if interaction.user.id in active_trivia:
            return await interaction.response.send_message("You already have an active trivia!", ephemeral=True)

        song_title = random.choice(list(SONG_DATA.keys()))
        lyric = random.choice(SONG_DATA[song_title])
        other_titles = list(SONG_DATA.keys())
        other_titles.remove(song_title)
        options = random.sample(other_titles, 3) + [song_title]
        random.shuffle(options)

        embed = discord.Embed(
            title=f"Trivia for {interaction.user.display_name}",
            description=f"*{lyric}*",
            color=0xff69b4
        )
        file = discord.File("nick6383.jpg", filename="nick6383.jpg")
        embed.set_image(url="attachment://nick6383.jpg")

        view = TriviaView(song_title, interaction.user.id)
        view.children[0].label = options[0]
        view.children[1].label = options[1]
        view.children[2].label = options[2]
        view.children[3].label = options[3]

        msg = await interaction.response.send_message(embed=embed, file=file, view=view)
        sent_msg = await interaction.original_response()
        view.message = sent_msg
        active_trivia[interaction.user.id] = sent_msg

async def setup(bot: commands.Bot):
    await bot.add_cog(Nick6383Trivia(bot))
