import discord
from discord import app_commands
from discord.ext import commands
import random

DUEL_ROLE_ID = 1371885746415341648
DUEL_CHANNEL_ID = 1373112868249145485  # updated to #games
EMBED_COLOR = discord.Color.from_rgb(231, 84, 128)

class Duel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="duel", description="Challenge someone to a number duel (1-100)")
    @app_commands.checks.has_role(DUEL_ROLE_ID)
    async def duel(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.channel.id != DUEL_CHANNEL_ID:
            await interaction.response.send_message("You can only use this command in the #games channel.", ephemeral=True)
            return

        if user.id == interaction.user.id:
            await interaction.response.send_message("You can’t duel yourself.", ephemeral=True)
            return

        if user.bot:
            await interaction.response.send_message("You can’t duel a bot.", ephemeral=True)
            return

        view = DuelAcceptView(interaction.user, user)
        embed = discord.Embed(
            title=f"{interaction.user.display_name} has challenged {user.display_name} to a duel!",
            description="Click the button below to accept. Both players will draw a number between 1 and 100.",
            color=EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, view=view)

class DuelAcceptView(discord.ui.View):
    def __init__(self, challenger, target):
        super().__init__(timeout=1800)
        self.challenger = challenger
        self.target = target

    @discord.ui.button(label="Accept Duel", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("Only the challenged user can accept.", ephemeral=True)
            return

        await interaction.response.defer()
        view = DuelDrawView(self.challenger, self.target)
        embed = discord.Embed(
            title="🎲 Duel Accepted!",
            description="Both players must now click their button to draw a number between 1 and 100.",
            color=EMBED_COLOR
        )
        await interaction.followup.send(embed=embed, view=view)
        self.stop()

class DuelDrawView(discord.ui.View):
    def __init__(self, challenger, target):
        super().__init__(timeout=300)
        self.challenger = challenger
        self.target = target
        self.draws = {}

        self.add_item(self.DuelButton(self.challenger, self))
        self.add_item(self.DuelButton(self.target, self))

    class DuelButton(discord.ui.Button):
        def __init__(self, player, parent_view):
            super().__init__(label=f"{player.display_name} draw", style=discord.ButtonStyle.primary)
            self.player = player
            self.parent_view = parent_view

        async def callback(self, interaction: discord.Interaction):
            if interaction.user.id != self.player.id:
                await interaction.response.send_message("This isn't your draw button.", ephemeral=True)
                return

            if self.player.id in self.parent_view.draws:
                await interaction.response.send_message("You already drew your number.", ephemeral=True)
                return

            number = random.randint(1, 100)
            self.parent_view.draws[self.player.id] = number
            await interaction.response.send_message(f"🎯 {self.player.display_name} drew **{number}**", ephemeral=False)

            if len(self.parent_view.draws) == 2:
                c_id = self.parent_view.challenger.id
                t_id = self.parent_view.target.id
                c_num = self.parent_view.draws[c_id]
                t_num = self.parent_view.draws[t_id]

                if c_num > t_num:
                    winner = self.parent_view.challenger
                elif t_num > c_num:
                    winner = self.parent_view.target
                else:
                    winner = None

                result_embed = discord.Embed(
                    title="⚔️ Duel Results",
                    description=(
                        f"**{self.parent_view.challenger.display_name}** drew **{c_num}**\n"
                        f"**{self.parent_view.target.display_name}** drew **{t_num}**\n\n"
                        f"{'It’s a tie!' if not winner else f'🏆 Winner: {winner.mention}'}"
                    ),
                    color=discord.Color.green() if winner else discord.Color.greyple()
                )
                await interaction.channel.send(embed=result_embed)
                self.parent_view.stop()

async def setup(bot):
    await bot.add_cog(Duel(bot))
