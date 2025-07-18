import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

        # Roles and channel
        verify_channel = guild.get_channel(1372762677868498994)
        approve_role = guild.get_role(1372695389555130420)
        member_role = guild.get_role(1371885746415341648)
        waiting_room = guild.get_channel(1381763578977194035)

        # Server icon
        server_icon_url = guild.icon.url if guild.icon else None

        # Embed in server channel
        embed = discord.Embed(
            title="New Member",
            description=f"{member.mention} has joined the server.\n\nPlease approve or deny access.",
            color=discord.Color.from_str("#ff4dd2")  # pink color
        )
        if server_icon_url:
            embed.set_image(url=server_icon_url)
        embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")
        view = VerificationButtons(member, member_role)
        await verify_channel.send(embed=embed, view=view)

        # DM to member (pink welcome)
        try:
            dm_embed = discord.Embed(
                title=f"Welcome to {guild.name.upper()}",
                description=(
                    f"Hey {member.mention}, you’re currently awaiting access approval. "
                    f"In the meantime, you can join the {waiting_room.mention} channel to patiently wait to be moved."
                ),
                color=discord.Color.from_str("#ff4dd2")
            )
            if server_icon_url:
                dm_embed.set_image(url=server_icon_url)
            dm_embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            pass

class VerificationButtons(discord.ui.View):
    def __init__(self, member, member_role):
        super().__init__(timeout=None)
        self.member = member
        self.member_role = member_role

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.get_role(1372695389555130420):
            await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)
            return

        await self.member.add_roles(self.member_role)

        approve_embed = discord.Embed(
            title="✅ Access Granted",
            description=f"You’ve been approved and are now a member of **WE'RE ALL IN LOVE!**",
            color=discord.Color.green()
        )
        try:
            await self.member.send(embed=approve_embed)
        except discord.Forbidden:
            pass

        confirm_embed = discord.Embed(
            title="✅ Member Approved",
            description=f"{self.member.mention} has been approved by {interaction.user.mention}.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=confirm_embed)

        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.get_role(1372695389555130420):
            await interaction.response.send_message("You don't have permission to deny.", ephemeral=True)
            return

        deny_embed = discord.Embed(
            title="❌ Application Denied",
            description=f"Your application to join **WE'RE ALL IN LOVE** has been denied.",
            color=discord.Color.red()
        )
        try:
            await self.member.send(embed=deny_embed)
        except discord.Forbidden:
            pass

        confirm_embed = discord.Embed(
            title="❌ Member Denied",
            description=f"{self.member.mention} was denied access by {interaction.user.mention}.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=confirm_embed)

        await self.member.kick(reason="Verification Denied")
        self.stop()

async def setup(bot):
    await bot.add_cog(VerifySystem(bot))
