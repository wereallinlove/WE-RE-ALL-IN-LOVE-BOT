
import discord
from discord.ext import commands
from discord import app_commands
import random

class MinesGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name="mines")
    @app_commands.describe(mines="Number of mines to place (1–24)")
    async def mines(self, interaction: discord.Interaction, mines: int):
        allowed_channel = 1373112868249145485
        allowed_role_id = 1371885746415341648

        if interaction.channel.id != allowed_channel:
            return await interaction.response.send_message("Use this in the correct channel.", ephemeral=True)

        if not any(role.id == allowed_role_id for role in interaction.user.roles):
            return await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

        if mines < 1 or mines > 24:
            return await interaction.response.send_message("Choose between 1 and 24 mines.", ephemeral=True)

        grid_size = 25
        bomb_positions = random.sample(range(grid_size), mines)
        revealed = set()

        class TileView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.revealed = set()
                self.stopped = False

                for i in range(grid_size):
                    row = i // 5
                    col = i % 5
                    self.add_item(self.TileButton(index=i, row=row, col=col))

                self.add_item(self.CashOutButton())

            class TileButton(discord.ui.Button):
                def __init__(self, index, row, col):
                    super().__init__(style=discord.ButtonStyle.secondary, label="⬛", row=row)
                    self.index = index
                    self.row_pos = row
                    self.col_pos = col

                async def callback(self, interaction: discord.Interaction):
                    if self.index in self.view.revealed or self.view.stopped:
                        return await interaction.response.defer()

                    self.view.revealed.add(self.index)

                    if self.index in bomb_positions:
                        self.label = "💥"
                        self.style = discord.ButtonStyle.danger
                        self.disabled = True
                        for child in self.view.children:
                            if isinstance(child, discord.ui.Button):
                                child.disabled = True
                                if hasattr(child, 'index') and child.index in bomb_positions:
                                    child.label = "💣"
                        await interaction.response.edit_message(
                            content=None,
                            embed=discord.Embed(
                                title="BOOM!",
                                description=f"You hit a bomb after **{len(self.view.revealed)-1}** safe clicks.",
                                color=discord.Color.red()
                            ),
                            view=self.view
                        )
                        self.view.stopped = True
                    else:
                        self.label = "❎"
                        self.style = discord.ButtonStyle.secondary
                        self.disabled = True
                        await interaction.response.edit_message(view=self.view)

            class CashOutButton(discord.ui.Button):
                def __init__(self):
                    super().__init__(label="Cash Out", style=discord.ButtonStyle.success, row=5)

                async def callback(self, interaction: discord.Interaction):
                    if self.view.stopped:
                        return await interaction.response.defer()

                    for child in self.view.children:
                        if isinstance(child, discord.ui.Button):
                            child.disabled = True
                            if hasattr(child, 'index') and child.index in bomb_positions:
                                child.label = "💣"

                    await interaction.response.edit_message(
                        content=None,
                        embed=discord.Embed(
                            title="You Cashed Out!",
                            description=f"You safely clicked **{len(self.view.revealed)}** tiles.",
                            color=discord.Color.green()
                        ),
                        view=self.view
                    )
                    self.view.stopped = True

        embed = discord.Embed(
            title=f"{interaction.user.display_name} started a Mines game",
            description=f"Click to reveal safe tiles. Avoid the bombs!
You placed **{mines}** bombs. Click **Cash Out** to stop early.",
            color=discord.Color.magenta()
        )

        await interaction.response.send_message(embed=embed, view=TileView())

async def setup(bot):
    await bot.add_cog(MinesGame(bot))
