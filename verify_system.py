import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

APPROVE_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648
VERIFY_CHANNEL_ID = 1371879905548089549
WAITING_ROOM_CHANNEL_ID = 1381763578977194035

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        verify_channel = guild.get_channel(VERIFY_CHANNEL_ID)
        approve_role = guild.get_role(APPROVE_ROLE_ID)

        # Send DM embed when user joins
        try:
            embed_dm = discord.Embed(
                title="Welcome to the server!",
                description=f"You’re currently in limbo while we review your access.\n\nFeel free to join <#{WAITING_ROOM_CHANNEL_ID}> and wait to be approved or denied.",
                color=discord.Color.from_rgb(231, 84, 128)
            )
            embed_dm.set_thumbnail(url=guild.icon.url if guild.icon else None)
            embed_dm.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")
            await member.send(embed=embed_dm)
        except discord.Forbidden:
            pass  # DMs off

        # In-server embed with buttons
        embed = discord.Embed(
            title="New Member Joined",
            description=f"{member.mention} has joined the server.\n\n<@&{APPROVE_ROLE_ID}> Please approve or deny access.",
            color=discord.Color.from_rgb(231, 84, 128)
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1371879905548089549/1371880110439452692/verify-image.gif?ex=6698fcab&is=668687ab&hm=1e8e27c7d997fa1d84a53c1aa7e0cf682e6465ff7207a6cb26a07a5f1122c39e&")
        embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")

        view = discord.ui.View()
        view.add_item(ApproveButton(member))
        view.add_item(DenyButton(member))
        await verify_channel.send(embed=embed, view=view)


class ApproveButton(discord.ui.Button):
    def __init__(self, member):
        super().__init__(label="Approve", style=discord.ButtonStyle.success)
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        if discord.utils.get(interaction.user.roles, id=APPROVE_ROLE_ID) is None:
            await interaction.response.send_message("You do not have permission to approve members.", ephemeral=True)
            return

        role = discord.utils.get(self.member.guild.roles, id=VERIFIED_ROLE_ID)
        await self.member.add_roles(role)

        await interaction.response.send_message(embed=discord.Embed(
            title="✅ Member Approved",
            description=f"{self.member.mention} has been approved by {interaction.user.mention}.",
            color=discord.Color.green()
        ))

        await interaction.channel.send(f"{self.member.mention} has been approved and given the {role.mention} role.")

        # DM the member
        try:
            embed_dm = discord.Embed(
                title="✅ You’ve been accepted!",
                description=f"You’ve been approved and are now a member of **{self.member.guild.name}**.",
                color=discord.Color.green()
            )
            embed_dm.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")
            await self.member.send(embed=embed_dm)
        except discord.Forbidden:
            pass


class DenyButton(discord.ui.Button):
    def __init__(self, member):
        super().__init__(label="Deny", style=discord.ButtonStyle.danger)
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        if discord.utils.get(interaction.user.roles, id=APPROVE_ROLE_ID) is None:
            await interaction.response.send_message("You do not have permission to deny members.", ephemeral=True)
            return

        await interaction.response.send_message(embed=discord.Embed(
            title="❌ Member Denied",
            description=f"{self.member.mention} has been denied by {interaction.user.mention}.",
            color=discord.Color.red()
        ))

        # DM the member
        try:
            embed_dm = discord.Embed(
                title="❌ You’ve been denied.",
                description=f"Unfortunately, you were not approved to join **{self.member.guild.name}**.",
                color=discord.Color.red()
            )
            embed_dm.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")
            await self.member.send(embed=embed_dm)
        except discord.Forbidden:
            pass

        await self.member.kick(reason="Verification Denied")


async def setup(bot):
    await bot.add_cog(Verify(bot))