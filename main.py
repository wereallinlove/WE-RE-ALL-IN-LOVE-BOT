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

# Stores the most recently joined member to approve
pending_approvals = {}

class ApproveButton(Button):
    def __init__(self):
        super().__init__(label="Approve", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != ADMIN_USER_ID:
            await interaction.response.send_message("You do not have permission to approve.", ephemeral=True)
            return

        member = pending_approvals.get(interaction.message.id)
        if not member:
            await interaction.response.send_message("No pending member found for this message.", ephemeral=True)
            return

        role = discord.utils.get(interaction.guild.roles, name=APPROVED_ROLE_NAME)
        if role:
            await member.add_roles(role)
            await interaction.response.edit_message(
                content=f"{member.mention} has been approved and given the role '{role.name}'.",
                embed=None,
                view=None
            )
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

class ApprovalView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ApproveButton())

@bot.event
async def on_ready():
    bot.add_view(ApprovalView())  # Register the persistent view
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

    message = await channel.send(embed=embed, view=ApprovalView())
    pending_approvals[message.id] = member  # Store member reference for this message

# Keep-alive for Render deployment
from keep_alive import keep_alive
keep_alive()

bot.run(os.getenv("TOKEN"))
