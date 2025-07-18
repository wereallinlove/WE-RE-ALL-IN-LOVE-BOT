import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands, ui, Interaction
import datetime

class VerifyButtons(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, custom_id="verify_approve")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        approver = interaction.user
        if not get(approver.roles, id=1372695389555130420):  # .approve role
            await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)
            return

        role = get(interaction.guild.roles, id=1371885746415341648)  # @Member role
        await self.member.add_roles(role)

        embed = discord.Embed(
            title="✅ Member Approved",
            description=f"{self.member.mention} has been approved by {approver.mention}.",
            color=0x57F287
        )
        await interaction.response.send_message(embed=embed)
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, custom_id="verify_deny")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        denier = interaction.user
        if not get(denier.roles, id=1372695389555130420):  # .approve role
            await interaction.response.send_message("You don't have permission to deny.", ephemeral=True)
            return

        embed = discord.Embed(
            title="❌ Member Denied",
            description=f"{self.member.mention} was denied access by {denier.mention}.",
            color=0xED4245
        )
        await interaction.response.send_message(embed=embed)
        try:
            await self.member.kick(reason="Verification denied")
        except:
            pass
        self.stop()

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(1372762677868498994)  # #verify
        guild_icon_url = member.guild.icon.url if member.guild.icon else None

        embed = discord.Embed(
            title="New Member",
            description=f"{member.mention} has joined the server.\n\nPlease approve or deny access.",
            color=0xFF3AAF
        )
        if guild_icon_url:
            embed.set_image(url=guild_icon_url)

        embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.datetime.now().year}")

        view = VerifyButtons(member)
        await channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(VerifySystem(bot))
