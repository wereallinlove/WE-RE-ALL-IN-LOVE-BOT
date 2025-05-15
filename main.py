import subprocess
subprocess.run(["pip", "install", "-U", "discord.py"])

from keep_alive import keep_alive  # Keep bot running
keep_alive()

import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for on_member_join

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549  # your admin channel
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"  # the role to grant access

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        print("Admin channel not found.")
        return

    embed = discord.Embed(
        title="A soul has entered the void.",
        description=f"{member.mention} joined the server.\n\nDo you wish to grant them access to **WE'RE ALL IN LOVE**?",
        color=0xff5eaa
    )
    embed.set_footer(text="WE'RE ALL IN LOVE", icon_url="https://i.imgur.com/zM1dCcs.png")

    class ApproveButton(View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
        async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.guild_permissions.administrator:
                role = discord.utils.get(member.guild.roles, name=APPROVED_ROLE_NAME)
                if role:
                    await member.add_roles(role)
                    await interaction.response.send_message(
                        f"{member.mention} has been granted access.",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message("Role not found.", ephemeral=True)
            else:
                await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)

    await channel.send(embed=embed, view=ApproveButton())

bot.run(os.getenv("TOKEN"))
