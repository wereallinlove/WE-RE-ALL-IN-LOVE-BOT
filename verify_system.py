import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import datetime

class VerifySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

        # --- SETTINGS ---
        verify_channel_id = 1373111807671945257  # Channel where join message goes
        approve_role_id = 1372695389555130420   # Role that can approve
        verified_role_id = 1371885746415341648  # Role to give on approval
        waiting_room_channel_id = 1381763578977194035  # Waiting Room
        server_icon = guild.icon.url if guild.icon else discord.Embed.Empty
        current_year = datetime.datetime.now().year

        # --- Send DM Welcome Embed ---
        try:
            welcome_embed = discord.Embed(
                title="Welcome to the server ♡",
                description=(
                    f"You're currently in limbo — someone needs to **accept or deny** your application.\n\n"
                    f"In the meantime, feel free to join <#{waiting_room_channel_id}> and wait patiently."
                ),
                color=discord.Color.from_str("#ff9dd9")
            )
            welcome_embed.set_thumbnail(url=server_icon)
            welcome_embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")
            await member.send(embed=welcome_embed)
        except:
            pass  # Ignore if DMs are closed

        # --- Send Server Embed With Buttons ---
        verify_channel = guild.get_channel(verify_channel_id)
        if not verify_channel:
            return

        embed = discord.Embed(
            title="New Member",
            description=(
                f"{member.mention} has joined the server.\n\n"
                f"<@&{approve_role_id}> Please approve or deny access."
            ),
            color=discord.Color.from_str("#ff2f92")
        )
        embed.set_image(url="https://i.imgur.com/Qg7k7Yx.jpeg")  # Your welcome image
        embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

        approve_button = Button(label="Approve", style=discord.ButtonStyle.success)
        deny_button = Button(label="Deny", style=discord.ButtonStyle.danger)

        async def approve_callback(interaction: discord.Interaction):
            if approve_role_id not in [role.id for role in interaction.user.roles]:
                await interaction.response.send_message("You don’t have permission to approve members.", ephemeral=True)
                return

            await member.add_roles(guild.get_role(verified_role_id))

            # DM user upon approval
            try:
                approved_embed = discord.Embed(
                    title="✅ You've Been Approved",
                    description=f"You’ve been accepted into **{guild.name}**. Enjoy your stay!",
                    color=discord.Color.green()
                )
                await member.send(embed=approved_embed)
            except:
                pass

            # Send confirmation in server
            approved_embed = discord.Embed(
                title="✅ Member Approved",
                description=f"{member.mention} has been approved by {interaction.user.mention}.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=approved_embed)

        async def deny_callback(interaction: discord.Interaction):
            if approve_role_id not in [role.id for role in interaction.user.roles]:
                await interaction.response.send_message("You don’t have permission to deny members.", ephemeral=True)
                return

            try:
                denied_embed = discord.Embed(
                    title="❌ You've Been Denied",
                    description=f"You were not accepted into **{guild.name}**. Best of luck elsewhere.",
                    color=discord.Color.red()
                )
                await member.send(embed=denied_embed)
            except:
                pass

            await member.kick(reason="Verification denied.")

            denied_embed = discord.Embed(
                title="❌ Member Denied",
                description=f"{member.mention} has been denied and kicked by {interaction.user.mention}.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=denied_embed)

        approve_button.callback = approve_callback
        deny_button.callback = deny_callback

        view = View()
        view.add_item(approve_button)
        view.add_item(deny_button)

        await verify_channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(VerifySystem(bot))