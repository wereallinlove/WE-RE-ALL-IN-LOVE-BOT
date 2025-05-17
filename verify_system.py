import discord
from discord.ext import commands
from discord import app_commands, Interaction, ui

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1372695389555130420)  # verify channel
        if channel:
            embed = discord.Embed(
                title="Verification Required",
                description=f"{member.mention} just joined.\nAn admin must approve or deny them.",
                color=discord.Color.pink()
            )
            if member.guild.icon:
                embed.set_image(url=member.guild.icon.url)
            embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")
            view = VerificationButtons(member.id)
            await channel.send(embed=embed, view=view)

class VerificationButtons(ui.View):
    def __init__(self, member_id):
        super().__init__(timeout=None)
        self.member_id = member_id

    @ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: Interaction, button: ui.Button):
        if not interaction.user.get_role(1372695389555130420):  # .approve role
            await interaction.response.send_message("You don't have permission to approve users.", ephemeral=True)
            return

        member = interaction.guild.get_member(self.member_id)
        verified_role = interaction.guild.get_role(1371885746415341648)  # Verified role
        if member and verified_role:
            await member.add_roles(verified_role)
            await interaction.response.send_message(f"{member.mention} has been approved ✅", ephemeral=True)
            approved_embed = discord.Embed(
                title="✅ Approved",
                description=f"{member.mention} has been verified by {interaction.user.mention}.",
                color=discord.Color.green()
            )
            approved_embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")
            await interaction.channel.send(embed=approved_embed)

    @ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: Interaction, button: ui.Button):
        if not interaction.user.get_role(1372695389555130420):  # .approve role
            await interaction.response.send_message("You don't have permission to deny users.", ephemeral=True)
            return

        member = interaction.guild.get_member(self.member_id)
        if member:
            await member.kick(reason="Verification Denied")
            await interaction.response.send_message(f"{member.mention} has been denied and kicked ❌", ephemeral=True)
            denied_embed = discord.Embed(
                title="❌ Denied",
                description=f"{member.mention} was denied and kicked by {interaction.user.mention}.",
                color=discord.Color.red()
            )
            denied_embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")
            await interaction.channel.send(embed=denied_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(VerifySystem(bot))
