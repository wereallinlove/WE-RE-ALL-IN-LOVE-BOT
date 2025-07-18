import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

APPROVE_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648
VERIFY_CHANNEL_ID = 1371803261033230346

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(VERIFY_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="New Member Joined",
                description=f"{member.mention} has joined the server.\nPlease approve or deny access.",
                color=discord.Color.pink()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")
            view = ApproveDenyView(member)
            await channel.send(embed=embed, view=view)

class ApproveDenyView(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=None)
        self.member = member

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        if APPROVE_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)
            return
        role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        if role:
            await self.member.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(
                title="✅ Approved",
                description=f"{self.member.mention} has been approved.",
                color=discord.Color.green()
            ))
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if APPROVE_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to deny.", ephemeral=True)
            return
        await self.member.kick(reason="Denied during verification")
        await interaction.response.send_message(embed=discord.Embed(
            title="❌ Denied",
            description=f"{self.member.name} has been denied and kicked from the server.",
            color=discord.Color.red()
        ))
        self.stop()

async def setup(bot):
    await bot.add_cog(Verify(bot))
