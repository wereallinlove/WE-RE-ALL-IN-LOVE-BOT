import discord
from discord.ext import commands
from discord import app_commands, Interaction, ui

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1372695389555130420)  # #verify
        if not channel:
            return

        embed = discord.Embed(
            title="Verification Needed",
            description=f"{member.mention} just joined.\nPlease approve or deny them.",
            color=discord.Color.pink()
        )
        embed.set_image(url=member.guild.icon.url if member.guild.icon else None)
        embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")

        view = VerifyButtons(member.id)
        await channel.send(embed=embed, view=view)

class VerifyButtons(ui.View):
    def __init__(self, member_id):
        super().__init__(timeout=None)
        self.member_id = member_id

    @ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve_button(self, interaction: Interaction, button: ui.Button):
        if not interaction.user.get_role(1372695389555130420):  # .approve role ID
            await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(self.member_id)
        role = guild.get_role(1371885746415341648)  # @Verified role

        if member and role:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention} has been approved ✅", ephemeral=False)

            embed = discord.Embed(
                title="✅ Approved",
                description=f"{member.mention} has been verified by {interaction.user.mention}",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")
            await interaction.channel.send(embed=embed)
        else:
            await interaction.response.send_message("Failed to approve. Member or role not found.", ephemeral=True)

    @ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny_button(self, interaction: Interaction, button: ui.Button):
        if not interaction.user.get_role(1372695389555130420):
            await interaction.response.send_message("You don't have permission to deny.", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(self.member_id)

        if member:
            await member.kick(reason="Denied by verification system")
            await interaction.response.send_message(f"{member.mention} has been denied ❌", ephemeral=False)

            embed = discord.Embed(
                title="❌ Denied",
                description=f"{member.name} was denied and kicked by {interaction.user.mention}",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")
            await interaction.channel.send(embed=embed)
        else:
            await interaction.response.send_message("Failed to deny. Member not found.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(VerifySystem(bot))
