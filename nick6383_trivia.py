
# nick6383_trivia.py — WORKING VERSION (confirmed by user)
import discord
from discord import app_commands
from discord.ext import commands
import random
import json
from datetime import datetime

TRIVIA_CHANNEL_ID = 1373112868249145485
VERIFIED_ROLE_ID = 1371885746415341648

class Nick6383Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}
        self.active_users = set()
        self.scores_file = "trivia_scores.json"
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(self.scores_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_scores(self):
        with open(self.scores_file, "w") as f:
            json.dump(self.scores, f)

    trivia_data = [
        {"lyric": "I got it out the dirt like a zombie", "answer": "From the dirt"},
        {"lyric": "I feel ugly, so I bought a new nose", "answer": "I JUST BOUGHT A NEW NOSE!"},
        {"lyric": "Let's go to the mall, spend it all, we'll buy it all", "answer": "MAKE ME FAMOUS!"},
        {"lyric": "Die young, get cake, shoutout Lil Jeep", "answer": "10k freestyle"},
        {"lyric": "American beauty queen, I got blood all on my jeans", "answer": "American beauty"},
    ]

    @app_commands.command(name="nick6383trivia", description="Guess the Nick6383 song based on a lyric.")
    async def nick6383trivia(self, interaction: discord.Interaction):
        if interaction.channel.id != TRIVIA_CHANNEL_ID:
            await interaction.response.send_message("This command can only be used in the trivia channel.", ephemeral=True)
            return

        if VERIFIED_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You must be verified to use this command.", ephemeral=True)
            return

        user_id = str(interaction.user.id)
        now = discord.utils.utcnow().timestamp()

        if user_id in self.cooldowns and now - self.cooldowns[user_id] < 5:
            await interaction.response.send_message("⏳ Please wait a few seconds before using this again.", ephemeral=True)
            return

        if user_id in self.active_users:
            await interaction.response.send_message("You're already answering a question!", ephemeral=True)
            return

        self.cooldowns[user_id] = now
        self.active_users.add(user_id)

        question = random.choice(self.trivia_data)
        correct_answer = question["answer"]
        all_titles = list({entry["answer"] for entry in self.trivia_data})
        options = random.sample([t for t in all_titles if t != correct_answer], k=3)
        options.append(correct_answer)
        random.shuffle(options)

        current_year = datetime.now().year
        embed = discord.Embed(
            title=f"Trivia for {interaction.user.display_name}",
            description=f"*{question['lyric']}*",
            color=discord.Color.from_rgb(255, 100, 180)
        )
        embed.set_image(url="attachment://nick6383.jpg")

        view = discord.ui.View(timeout=30.0)
        for option in options:
            async def callback(interaction_inner: discord.Interaction, selected=option):
                if interaction_inner.user != interaction.user:
                    await interaction_inner.response.send_message("This isn't your trivia question.", ephemeral=True)
                    return

                correct = selected == correct_answer
                color = discord.Color.green() if correct else discord.Color.red()
                result_embed = discord.Embed(
                    title="✅ Correct!" if correct else "❌ Incorrect",
                    description=f"You selected **{selected}**.
The correct answer was **{correct_answer}**.",
                    color=color
                )

                self.scores.setdefault(user_id, {"correct": 0, "incorrect": 0})
                if correct:
                    self.scores[user_id]["correct"] += 1
                else:
                    self.scores[user_id]["incorrect"] += 1

                self.save_scores()

                score = self.scores[user_id]
                result_embed.set_footer(
                    text=f"👑 {score['correct']} correct • ❌ {score['incorrect']} wrong"
                )

                await interaction_inner.response.edit_message(embed=result_embed, view=None)
                self.active_users.discard(user_id)

            button = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary)
            button.callback = callback
            view.add_item(button)

        file = discord.File("nick6383.jpg", filename="nick6383.jpg")
        await interaction.response.send_message(embed=embed, view=view, file=file)

async def setup(bot):
    await bot.add_cog(Nick6383Trivia(bot))
