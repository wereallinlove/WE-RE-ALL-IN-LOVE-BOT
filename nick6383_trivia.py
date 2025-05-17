import discord
from discord import app_commands
from discord.ext import commands
import random

class Nick6383Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_data = [
            {"lyric": "I got it out the dirt like a zombie", "answer": "From the dirt"},
            {"lyric": "I throw my money up, I throw my money up", "answer": "I JUST BOUGHT A NEW NOSE!"},
            {"lyric": "I'm in the club and all I see is paparazzi", "answer": "MAKE ME FAMOUS!"},
            {"lyric": "Slit my wrists and now I'm laughing, Ten racks, got my jeans saggin'", "answer": "10k freestyle"},
            {"lyric": "I'ma slit my fuckin' neck, chop off my arms", "answer": "American beauty"},
            {"lyric": "Starve myself, I can weigh less", "answer": "American psycho"},
            {"lyric": "Hungry, hungry, I feel so ugly", "answer": "Anorexic party"},
            {"lyric": "Can you rip my heart out? Shoot me with the AK", "answer": "backstage"},
            {"lyric": "Welcome to my fuckin' show, I'm throwin' rocks through your window", "answer": "beware of the dog"},
            {"lyric": "I got so rich so quick, your welfare check is coming in", "answer": "Bible school"},
            # ... all other entries ...
        ]

    @app_commands.command(name="nick6383trivia", description="Answer a trivia question with Nick6383 lyrics.")
    @app_commands.checks.has_role(1371885746415341648)
    async def nick6383trivia(self, interaction: discord.Interaction):
        entry = random.choice(self.trivia_data)
        lyric = entry["lyric"]
        correct = entry["answer"]
        all_titles = list(set([d["answer"] for d in self.trivia_data]))
        choices = random.sample([t for t in all_titles if t != correct], 3) + [correct]
        random.shuffle(choices)

        class TriviaView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.answered = False

            @discord.ui.button(label=choices[0], style=discord.ButtonStyle.secondary)
            async def option1(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.process_answer(interaction_button, button.label)

            @discord.ui.button(label=choices[1], style=discord.ButtonStyle.secondary)
            async def option2(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.process_answer(interaction_button, button.label)

            @discord.ui.button(label=choices[2], style=discord.ButtonStyle.secondary)
            async def option3(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.process_answer(interaction_button, button.label)

            @discord.ui.button(label=choices[3], style=discord.ButtonStyle.secondary)
            async def option4(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await self.process_answer(interaction_button, button.label)

            async def process_answer(self, interaction_button, chosen):
                if interaction_button.user.id != interaction.user.id:
                    await interaction_button.response.send_message("Only the original user can answer this trivia.", ephemeral=True)
                    return
                if self.answered:
                    await interaction_button.response.send_message("You already answered.", ephemeral=True)
                    return
                self.answered = True
                color = discord.Color.green() if chosen == correct else discord.Color.red()
                title = "✅ Correct!" if chosen == correct else "❌ Incorrect."
                description = f"The lyric was from **{correct}**." if chosen != correct else f"You got it right!"
                embed = discord.Embed(title=title, description=description, color=color)
                await interaction_button.response.send_message(embed=embed)

        embed = discord.Embed(
            title=f"🎵 Trivia for {interaction.user.display_name}",
            description=f"*{lyric}*",
            color=discord.Color.magenta()
        )
        embed.set_image(url="https://raw.githubusercontent.com/wereallinlove/WE-RE-ALL-IN-LOVE-BOT/main/nick6383.jpg")
        await interaction.response.send_message(content=f"Trivia time for {interaction.user.mention} 🎤", embed=embed, view=TriviaView())

async def setup(bot):
    await bot.add_cog(Nick6383Trivia(bot))
