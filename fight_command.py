import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import random

FIGHT_ROLE_ID = 1371885746415341648
FIGHT_CHANNEL_ID = 1318298515948048549
ADMIN_ROLE_ID = 1371681883796017222
EMBED_COLOR = discord.Color.from_rgb(231, 84, 128)

class Fight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pending_fights = {}

    @app_commands.command(name="fight", description="Challenge someone to a dramatic battle.")
    @app_commands.checks.has_role(FIGHT_ROLE_ID)
    async def fight(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.channel.id != FIGHT_CHANNEL_ID:
            await interaction.response.send_message("You can only use this command in the fight channel.", ephemeral=True)
            return

        if user.id == interaction.user.id:
            await interaction.response.send_message("You can’t fight yourself... yet.", ephemeral=True)
            return

        if user.bot:
            await interaction.response.send_message("You can’t fight a bot.", ephemeral=True)
            return

        view = FightAcceptView(interaction.user, user)
        embed = discord.Embed(
            title=f"{interaction.user.display_name} has challenged {user.display_name} to a fight!",
            description="Click the button below to accept. You have 30 minutes...",
            color=EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, view=view)

class FightAcceptView(discord.ui.View):
    def __init__(self, challenger, target):
        super().__init__(timeout=1800)
        self.challenger = challenger
        self.target = target

    @discord.ui.button(label="Accept Fight", style=discord.ButtonStyle.danger)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("Only the challenged user can accept.", ephemeral=True)
            return

        await interaction.response.defer()
        loading_messages = [
            "they’re circling each other in silence…",
            "a chair just got thrown across the room",
            "one of them is crying but still throwing punches",
            "they're fighting like it's 3AM in a groupchat",
            "someone pulled hair. this is getting brutal",
            "they started quoting Lana mid-fight",
            "this is messier than their last relationship",
        ]

        loading_embed = discord.Embed(
            title="⚔️ The fight has begun...",
            description=random.choice(loading_messages),
            color=discord.Color.dark_red()
        )
        await interaction.followup.send(embed=loading_embed)

        await asyncio.sleep(6)

        # Check for admin bias
        challenger_is_admin = any(role.id == ADMIN_ROLE_ID for role in self.challenger.roles)
        target_is_admin = any(role.id == ADMIN_ROLE_ID for role in self.target.roles)

        if challenger_is_admin and not target_is_admin:
            winner = self.challenger if random.random() < 0.75 else self.target
        elif target_is_admin and not challenger_is_admin:
            winner = self.target if random.random() < 0.75 else self.challenger
        else:
            winner = random.choice([self.challenger, self.target])

        loser = self.target if winner == self.challenger else self.challenger

        final_embed = discord.Embed(
            title="🏆 The results are in...",
            description=f"**{winner.display_name}** has defeated **{loser.display_name}** in a dramatic battle.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=final_embed)
        self.stop()

    async def on_timeout(self):
        try:
            channel = self.children[0].view.message.channel
            embed = discord.Embed(
                title="⌛ Challenge Expired",
                description="No response was given. The fight never happened.",
                color=discord.Color.greyple()
            )
            await channel.send(embed=embed)
        except:
            pass

async def setup(bot):
    await bot.add_cog(Fight(bot))
