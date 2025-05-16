import discord
from datetime import datetime

APPROVER_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648
VERIFY_CHANNEL_ID = 1372762677868498994

class ApproveDenyView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, custom_id="approve_button")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        approver_role = interaction.guild.get_role(APPROVER_ROLE_ID)
        if approver_role not in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to approve members.", ephemeral=True)
            return

        role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        if role:
            await self.member.add_roles(role)
            await interaction.response.send_message(f"{self.member.mention} has been approved and given the role.")

            approved_embed = discord.Embed(
                title="✅ Member Approved",
                description=f"{self.member.mention} has been approved by {interaction.user.mention}.",
                color=discord.Color.green()
            )
            await interaction.channel.send(embed=approved_embed)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, custom_id="deny_button")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        approver_role = interaction.guild.get_role(APPROVER_ROLE_ID)
        if approver_role not in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to deny members.", ephemeral=True)
            return

        await self.member.kick(reason="Denied by approver")
        await interaction.response.send_message(f"{self.member.mention} has been denied and kicked.")

        denied_embed = discord.Embed(
            title="❌ Member Denied",
            description=f"{self.member.mention} was denied access by {interaction.user.mention}.",
            color=discord.Color.red()
        )
        await interaction.channel.send(embed=denied_embed)

def setup(bot):
    @bot.event
    async def on_member_join(member):
        channel = bot.get_channel(VERIFY_CHANNEL_ID)
        guild = member.guild

        if channel:
            current_year = datetime.now().year
            embed = discord.Embed(
                title="New Member Joined",
                description=f"{member.mention} has joined the server.\n\nPlease approve or deny access.",
                color=discord.Color.from_rgb(255, 105, 180)
            )

            if guild.icon:
                embed.set_image(url=guild.icon.url)

            embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

            view = ApproveDenyView(member)
            await channel.send(embed=embed, view=view)
