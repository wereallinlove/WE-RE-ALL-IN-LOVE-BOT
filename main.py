import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549
ADMIN_USER_ID = 102413867329519616
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"

class AccessView(View):
    def __init__(self, member):
        super().__init__(timeout=None)
        self.member = member

        approve_button = Button(label="Approve", style=discord.ButtonStyle.success)
        approve_button.callback = self.approve
        self.add_item(approve_button)

    async def approve(self, interaction: discord.Interaction):
        if interaction.user.id != ADMIN_USER_ID:
            await interaction.response.send_message("You do not have permission to approve.", ephemeral=True)
            return

        role = discord.utils.get(interaction.guild.roles, name=APPROVED_ROLE_NAME)
        if role:
            await self.member.add_roles(role)
            await interaction.response.edit_message(content=f"{self.member.mention} has been approved and given the role '{role.name}'.", embed=None, view=None)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

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

    await channel.send(embed=embed, view=AccessView(member))

# Keep-alive for Render deployment
from keep_alive import keep_alive
keep_alive()

# Start the bot
bot.run(os.getenv("TOKEN"))
