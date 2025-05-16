import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549  # your admin channel
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"  # the role to grant access
APPROVER_ROLE_NAME = ".approve"  # role that can approve members

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
        description=f"{member.mention} joined the server.

**Grant them access to WE'RE ALL IN LOVE?**"
    )

    class ApproveView(View):
        @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
        async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.get_role(APPROVER_ROLE_NAME) or interaction.user.guild_permissions.administrator:
                role = discord.utils.get(member.guild.roles, name=APPROVED_ROLE_NAME)
                if role:
                    await member.add_roles(role)
                    await interaction.response.send_message(f"{member.mention} has been approved.", ephemeral=True)
                else:
                    await interaction.response.send_message("Approval role not found.", ephemeral=True)
            else:
                await interaction.response.send_message("You are not authorized to approve members.", ephemeral=True)

    await channel.send(embed=embed, view=ApproveView())

bot.run(os.getenv("DISCORD_TOKEN"))