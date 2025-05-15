import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"
ADMIN_ROLE_NAME = ".admin"

# Track which member needs to be approved (by message ID)
pending_approvals = {}

class ApproveButton(Button):
    def __init__(self):
        super().__init__(label="Approve", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        # Check if user has .admin role
        admin_role = discord.utils.get(interaction.user.roles, name=ADMIN_ROLE_NAME)
        if not admin_role:
            await interaction.response.send_message("You must have the `.admin` role to approve members.", ephemeral=True)
            return

        member = pending_approvals.get(interaction.message.id)
        if not member:
            await interaction.response.send_message("Couldn't find the member to approve.", ephemeral=True)
            return

        role = discord.utils.get(interaction.guild.roles, name=APPROVED_ROLE_NAME)
        if not role:
            await interaction.response.send_message("Approved role not found.", ephemeral=True)
            return

        await member.add_roles(role)
        await interaction.response.edit_message(
            content=f"{member.mention} has been approved and given the role '{role.name}'.",
            embed=None,
            view=None
        )

class ApprovalView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ApproveButton())

@bot.event
async def on_ready():
    bot.add_view(ApprovalView())  # Register the button globally
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
    pending_approvals[message.id] = member

# Keep-alive for Render
from keep_alive import keep_alive
keep_alive()

bot.run(os.getenv("TOKEN"))
