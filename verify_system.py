import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

APPROVE_ROLE_ID = 1372695389555130420
VERIFIED_ROLE_ID = 1371885746415341648
VERIFY_CHANNEL_ID = 1371803261033230346
WAITING_ROOM_CHANNEL_ID = 1381763578977194035

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Send a DM to the new member
        try:
            welcome_embed = discord.Embed(
                title="🌀 Welcome to the server",
                description=(
                    f"You're currently in limbo while we review your access.\n\n"
                    f"For now, feel free to join <#{WAITING_ROOM_CHANNEL_ID}> and patiently wait to be moved.\n\n"
                    f"Someone will review your application soon."
                ),
                color=discord.Color.pink()
            )
            welcome_embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else discord.Embed.Empty)
            welcome_embed.set_footer(text=f"WE'RE ALL IN LOVE {datetime.now().year}")
            await member.send(embed=welcome_embed)
        except:
            pass  # Ignore if DMs are closed

        # Send the embed in the verification channel
        channel = member.guild.get_channel(VERIFY_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="New Member",
                description=f"{member.mention} has joined the server.\n<@{APPROVE_ROLE_ID}> — Please approve or deny access.",
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

        # Send DM to the user
        try:
            approved_embed = discord.Embed(
                title="✅ You’ve Been Approved!",
                description=f"You’ve been accepted into **{interaction.guild.name}**. Welcome aboard!",
                color=discord.Color.green()
            )
            await self.member.send(embed=approved_embed)
        except:
            pass

        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if APPROVE_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to deny.", ephemeral=True)
            return

        try:
            denied_embed = discord.Embed(
                title="❌ You’ve Been Denied",
                description=f"Your request to join **{interaction.guild.name}** was denied. Better luck next time.",
                color=discord.Color.red()
            )
            await self.member.send(embed=denied_embed)
        except:
            pass

        await self.member.kick(reason="Denied during verification")
        await interaction.response.send_message(embed=discord.Embed(
            title="❌ Denied",
            description=f"{self.member.name} has been denied and kicked from the server.",
            color=discord.Color.red()
        ))

        self.stop()

async def setup(bot):
    await bot.add_cog(Verify(bot))