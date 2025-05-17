import discord
from discord.ext import commands
from discord import app_commands, ui, Interaction

VERIFY_CHANNEL_ID = 1372762677868498994
APPROVE_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(VERIFY_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="New Member Joined",
            description=f"{member.mention} has joined the server.\n\nPlease approve or deny access.",
            color=discord.Color.pink()
        )
        embed.set_image(url=member.guild.icon.url if member.guild.icon else discord.Embed.Empty)
        embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")

        view = ApproveDenyButtons(member.id)
        await channel.send(embed=embed, view=view)

class ApproveDenyButtons(ui.View):
    def __init__(self, member_id):
        super().__init__(timeout=None)
        self.member_id = member_id

    @ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve_button(self, interaction: Interaction, button: ui.Button):
        if not interaction.user.get_role(APPROVE_ROLE_ID):
            await interaction.response.send_message("You don’t have permission to approve users.", ephemeral=True)
            return

        member = interaction.guild.get_member(self.member_id)
        role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        if member and role:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"{member.mention} has been approved and given the <@&{VERIFIED_ROLE_ID}> role.",
                ephemeral=False
            )

            embed = discord.Embed(
                title="✅ Member Approved",
                description=f"{member.mention} has been approved by {interaction.user.mention}.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")
            await interaction.channel.send(embed=embed)

    @ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny_button(self, interaction: Interaction, button: ui.Button):
        if not interaction.user.get_role(APPROVE_ROLE_ID):
            await interaction.response.send_message("You don’t have permission to deny users.", ephemeral=True)
            return

        member = interaction.guild.get_member(self.member_id)
        if member:
            try:
                await member.send("Your request to join **WE'RE ALL IN LOVE** has been denied.")
            except:
                pass  # if DMs are off

            await member.kick(reason="Verification denied")
            await interaction.response.send_message(
                f"{member.mention} has been denied and kicked.",
                ephemeral=False
            )

            embed = discord.Embed(
                title="❌ Member Denied",
                description=f"{member.mention} was denied access by {interaction.user.mention}.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")
            await interaction.channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(VerifySystem(bot))
