import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Needed for member join events

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549
ADMIN_USER_ID = 102413867329519616
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"

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
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined the server.\n\nGrant them access to **WE'RE ALL IN LOVE**?",
        color=discord.Color.purple()
    )

    approve_button = Button(label="Approve", style=discord.ButtonStyle.success)

    async def button_callback(interaction):
        if interaction.user.id != ADMIN_USER_ID:
            await interaction.response.send_message("You do not have permission to approve.", ephemeral=True)
            return

        role = discord.utils.get(member.guild.roles, name=APPROVED_ROLE_NAME)
        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention} has been approved and given the role '{role.name}'.", ephemeral=False)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

    approve_button.callback = button_callback

    view = View()
    view.add_item(approve_button)

    await channel.send(embed=embed, view=view)

# Keep-alive for Render deployment
from keep_alive import keep_alive
keep_alive()

# Run bot using secret token
bot.run(os.getenv("TOKEN"))