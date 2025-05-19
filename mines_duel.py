# Add missing registration logic with cog_load for guaranteed sync

final_minesduel_code = '''
import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class MinesDuel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.tree.add_command(self.minesduel)
        await self.bot.tree.sync()
        print("Mines Duel command synced.")

    @app_commands.command(name="minesduel", description="Challenge someone to a Mines duel.")
    @app_commands.describe(user="The user to duel", mines="Number of mines to place (1–24)")
    async def minesduel(self, interaction: discord.Interaction, user: discord.User, mines: int):
        allowed_channel = 1373112868249145485
        allowed_role_id = 1371885746415341648

        if interaction.channel.id != allowed_channel:
            return await interaction.response.send_message("Use this in the correct channel.", ephemeral=True)

        if not any(role.id == allowed_role_id for role in interaction.user.roles):
            return await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)

        if user.id == interaction.user.id:
            return await interaction.response.send_message("You can't duel yourself.", ephemeral=True)

        if mines < 1 or mines > 24:
            return await interaction.response.send_message("Choose between 1 and 24 mines.", ephemeral=True)

        challenger = interaction.user
        challenged = user

        class AcceptView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=3600)

            @discord.ui.button(label="Accept Duel", style=discord.ButtonStyle.success)
            async def accept(self, i: discord.Interaction, button: discord.ui.Button):
                if i.user.id != challenged.id:
                    return await i.response.send_message("Only the challenged user can accept.", ephemeral=True)
                self.stop()
                await start_duel(interaction, challenger, challenged, mines)

            async def on_timeout(self):
                await interaction.followup.send(f"{challenged.mention} didn’t accept in time. Duel cancelled.", ephemeral=False)

        embed = discord.Embed(
            title=f"{challenger.display_name} challenged {challenged.display_name} to a Mines Duel!",
            description=f"{challenged.mention}, you have 1 hour to accept.\nEach player will try to uncover as many safe tiles as possible with **{mines}** bombs. First to hit a bomb loses.",
            color=discord.Color.magenta()
        )
        await interaction.response.send_message(embed=embed, view=AcceptView())

async def start_duel(interaction, challenger, challenged, mines):
    grid_size = 25

    class DuelView(discord.ui.View):
        def __init__(self, player, opponent, callback):
            super().__init__(timeout=None)
            self.player = player
            self.opponent = opponent
            self.callback = callback
            self.revealed = set()
            self.bombs = set(random.sample(range(grid_size), mines))
            self.tiles = []
            self.finished = False

            for i in range(grid_size):
                button = self.TileButton(index=i)
                self.tiles.append(button)
                self.add_item(button)

            self.add_item(self.CashOutButton())

        class TileButton(discord.ui.Button):
            def __init__(self, index):
                super().__init__(style=discord.ButtonStyle.secondary, label="⬛", row=index // 5)
                self.index = index

            async def callback(self, interaction):
                if self.disabled or self.view.finished or interaction.user.id != self.view.player.id:
                    return await interaction.response.defer()

                self.view.revealed.add(self.index)
                if self.index in self.view.bombs:
                    self.label = "💥"
                    self.style = discord.ButtonStyle.danger
                    self.view.finished = True
                    for btn in self.view.tiles:
                        btn.disabled = True
                        if btn.index in self.view.bombs:
                            btn.label = "💣"
                        elif btn.index in self.view.revealed:
                            btn.label = "❎"
                    await interaction.response.edit_message(
                        embed=discord.Embed(
                            title=f"{self.view.player.display_name} exploded!",
                            description=f"You hit a bomb after **{len(self.view.revealed) - 1}** safe tiles.",
                            color=discord.Color.red()
                        ),
                        view=self.view
                    )
                    self.view.callback(self.view.player, len(self.view.revealed) - 1, True)
                else:
                    self.label = "❎"
                    self.style = discord.ButtonStyle.secondary
                    self.disabled = True
                    await interaction.response.edit_message(view=self.view)

        class CashOutButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Cash Out", style=discord.ButtonStyle.success, row=5)

            async def callback(self, interaction):
                if interaction.user.id != self.view.player.id or self.view.finished:
                    return await interaction.response.defer()

                self.view.finished = True
                for btn in self.view.tiles:
                    btn.disabled = True
                    if btn.index in self.view.bombs:
                        btn.label = "💣"
                    elif btn.index in self.view.revealed:
                        btn.label = "❎"

                await interaction.response.edit_message(
                    embed=discord.Embed(
                        title=f"{self.view.player.display_name} cashed out!",
                        description=f"You safely uncovered **{len(self.view.revealed)}** tiles.",
                        color=discord.Color.green()
                    ),
                    view=self.view
                )
                self.view.callback(self.view.player, len(self.view.revealed), False)

    result = {}

    async def end_game(player, score, exploded):
        result[player.id] = (player.display_name, score, exploded)
        if len(result) == 2:
            p1, p2 = list(result.values())
            if p1[2] and not p2[2]:
                desc = f"**{p2[0]}** wins! {p1[0]} hit a bomb."
            elif p2[2] and not p1[2]:
                desc = f"**{p1[0]}** wins! {p2[0]} hit a bomb."
            elif p1[1] > p2[1]:
                desc = f"**{p1[0]}** wins by {p1[1]} to {p2[1]}!"
            elif p2[1] > p1[1]:
                desc = f"**{p2[0]}** wins by {p2[1]} to {p1[1]}!"
            else:
                desc = f"Draw! Both uncovered **{p1[1]}** tiles."

            await interaction.followup.send(embed=discord.Embed(
                title="Mines Duel Results",
                description=desc,
                color=discord.Color.magenta()
            ))

    await interaction.followup.send(embed=discord.Embed(
        title=f"{challenger.display_name}'s Game",
        description="Click to reveal safe tiles or cash out.",
        color=discord.Color.magenta()
    ), view=DuelView(challenger, challenged, end_game))

    await interaction.followup.send(embed=discord.Embed(
        title=f"{challenged.display_name}'s Game",
        description="Click to reveal safe tiles or cash out.",
        color=discord.Color.magenta()
    ), view=DuelView(challenged, challenger, end_game))

async def setup(bot):
    await bot.add_cog(MinesDuel(bot))
'''

# Save final fixed file to ensure command registration
file_path = "/mnt/data/mines_duel.py"
with open(file_path, "w") as f:
    f.write(final_minesduel_code)

file_path
